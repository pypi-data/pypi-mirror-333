from sqlalchemy import create_engine, text

def migrate_table_name(db_url="sqlite:///statemachines.db"):
    engine = create_engine(db_url)
    with engine.connect() as conn:
        # Rename the table if it exists (handles both old names)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS statemachine_templates AS 
            SELECT * FROM sm_templates;
        """))
        conn.execute(text("DROP TABLE IF EXISTS sm_templates;"))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS statemachine_templates AS 
            SELECT * FROM statemachines;
        """))
        conn.execute(text("DROP TABLE IF EXISTS statemachines;"))
        
        conn.commit()

if __name__ == '__main__':
    migrate_table_name()
    print("Migration completed successfully")
