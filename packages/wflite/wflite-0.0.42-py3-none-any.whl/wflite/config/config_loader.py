import os
import yaml
import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional

# Add dotenv import
try:
    from dotenv import load_dotenv
    has_dotenv = True
except ImportError:
    has_dotenv = False

logger = logging.getLogger(__name__)

class ConfigLoader:
    """
    Loads configuration from config.yml with support for environment variables
    and Azure Key Vault integration
    """
    
    def __init__(self, config_path: Optional[str] = None, env_file: Optional[str] = None):
        """
        Initialize the configuration loader
        
        Args:
            config_path: Optional path to the config YAML file
            env_file: Optional path to the .env file
        """
        # Load environment variables from .env file if available
        if has_dotenv:
            self._load_dotenv(env_file)
        else:
            logger.warning("python-dotenv not installed. Environment variables from .env file won't be loaded.")
            logger.warning("Install with: pip install python-dotenv")
        
        # Debug what environment variables are available
        logger.debug(f"PERSISTENCE_PROVIDER: {os.environ.get('PERSISTENCE_PROVIDER', 'not set')}")
        logger.debug(f"MONGODB_CONNECTION_STRING: {'set (hidden)' if 'MONGODB_CONNECTION_STRING' in os.environ else 'not set'}")
        
        if config_path is None:
            # Try to find config in standard locations
            base_dir = Path(__file__).parent
            
            # Look in these locations in order
            possible_paths = [
                # Same directory as this file
                base_dir / "config.yml",
                # Project root
                base_dir.parent.parent / "config.yml",
                # Current working directory
                Path.cwd() / "config.yml",
            ]
            
            # Use the first config file found
            for path in possible_paths:
                if path.exists():
                    config_path = str(path)
                    logger.info(f"Found configuration file: {config_path}")
                    break
            
            # If no config file found, use default path
            if config_path is None:
                config_path = str(base_dir / "config.yml")
                logger.warning(f"No config file found, using default path: {config_path}")
        
        logger.info(f"Loading configuration from {config_path}")
        self._config = self._load_config(config_path)
        
        # Debug what final provider was selected
        provider = self._config.get('persistence', {}).get('provider', 'unknown')
        logger.info(f"Selected persistence provider: {provider}")
    
    def _load_dotenv(self, env_file: Optional[str] = None) -> None:
        """
        Load environment variables from .env file
        
        Args:
            env_file: Path to the .env file
        """
        try:
            # If no env_file provided, look in standard locations
            if env_file is None:
                # Check project root first
                project_root = Path(__file__).parent.parent.parent
                env_paths = [
                    project_root / ".env",                # Project root
                    project_root / ".env.local",          # Local override
                    project_root / f".env.{os.environ.get('WFLITE_ENV', 'development')}",  # Environment-specific
                    Path.cwd() / ".env",                  # Current working directory
                ]
                
                # Use the first .env file found
                for path in env_paths:
                    if path.exists():
                        env_file = str(path)
                        logger.info(f"Found .env file: {env_file}")
                        break
            
            # If found an env file, load it
            if env_file and Path(env_file).exists():
                # Use override=True to ensure variables in .env override system environment variables
                load_dotenv(env_file, override=True)
                logger.info(f"Loaded environment variables from {env_file}")
                
                # Debug which variables were loaded
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key = line.split('=')[0].strip()
                            if key in os.environ:
                                # Don't log sensitive values
                                if 'PASSWORD' in key or 'SECRET' in key or 'CONNECTION' in key:
                                    logger.debug(f"Loaded from .env: {key}=***")
                                else:
                                    logger.debug(f"Loaded from .env: {key}={os.environ.get(key)}")
            else:
                logger.info("No .env file found, using existing environment variables")
                
        except Exception as e:
            logger.warning(f"Error loading .env file: {e}")
            
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from the specified YAML file
        and interpolate environment variables
        
        Args:
            config_path: Path to the config YAML file
            
        Returns:
            Dictionary containing the configuration
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            # Process environment variables in the configuration
            return self._process_env_vars(config)
            
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error loading config: {e}")
            return {}
    
    def _process_env_vars(self, config: Any) -> Any:
        """
        Recursively process all items in the configuration,
        interpolating environment variables where needed
        
        Args:
            config: Configuration item to process
            
        Returns:
            Processed configuration with environment variables interpolated
        """
        if isinstance(config, dict):
            return {k: self._process_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._process_env_vars(item) for item in config]
        elif isinstance(config, str):
            return self._interpolate_env_vars(config)
        else:
            return config
    
    def _interpolate_env_vars(self, value: str) -> Any:
        """
        Interpolate environment variables in the string.
        Format: ${ENV_VAR:default_value}
        
        Args:
            value: String to interpolate
        
        Returns:
            Interpolated string with environment variables replaced
        """
        if not isinstance(value, str):
            return value
            
        # Skip if no environment variable pattern found
        if "${" not in value:
            return value
            
        # Match environment variable patterns like ${ENV_VAR:default}
        pattern = r'\${([A-Za-z0-9_]+)(?::([^}]*))?}'
        
        def replace_var(match):
            env_var = match.group(1)
            default = match.group(2) if match.group(2) is not None else ""
            
            # Get from environment or use default
            result = os.environ.get(env_var, default)
            logger.debug(f"Environment variable interpolation: {env_var} = {result if 'PASSWORD' not in env_var and 'SECRET' not in env_var and 'CONNECTION' not in env_var else '***'}")
            
            # Try to convert to appropriate type
            if isinstance(result, str):
                if result.lower() == 'true':
                    return True
                elif result.lower() == 'false':
                    return False
                elif result.isdigit():
                    return int(result)
                elif result.replace(".", "", 1).isdigit() and result.count(".") == 1:
                    return float(result)
            
            return result
            
        result = re.sub(pattern, lambda m: str(replace_var(m)), value)
        
        # If entire string is an environment variable reference, try to parse it properly
        if re.fullmatch(pattern, value):
            match = re.fullmatch(pattern, value)
            env_var = match.group(1)
            default = match.group(2) if match.group(2) is not None else ""
            
            # Get value from environment or use default
            env_value = os.environ.get(env_var, default)
            logger.debug(f"Direct environment variable reference: {env_var} = {env_value if 'PASSWORD' not in env_var and 'SECRET' not in env_var and 'CONNECTION' not in env_var else '***'}")
            
            # Try to parse as YAML for more complex defaults
            if isinstance(env_value, str) and env_value and (env_value.startswith('{') or env_value.startswith('[')):
                try:
                    return yaml.safe_load(env_value)
                except yaml.YAMLError:
                    pass
                
            # Convert to appropriate type if possible
            if isinstance(env_value, str):
                if env_value.lower() == 'true':
                    return True
                elif env_value.lower() == 'false':
                    return False
                elif env_value.isdigit():
                    return int(env_value)
                elif env_value.replace(".", "", 1).isdigit() and env_value.count(".") == 1:
                    return float(env_value)
            
            # Return as string or original value
            return env_value
            
        return result
        
    def get_config(self) -> Dict[str, Any]:
        """
        Get the loaded configuration
        
        Returns:
            Dictionary containing the configuration
        """
        return self._config
