import asyncio
from nexusai.services.project_synthesizer import project_synthesizer

async def main():
    print("\n---------------- LIVE TRACE TEST 1: FLASK ----------------")
    await project_synthesizer.synthesize_full_project("FlaskWeatherAPI", "Build a Flask Weather API using SQLite")

    print("\n---------------- LIVE TRACE TEST 2: REACT ----------------")
    await project_synthesizer.synthesize_full_project("ReactTodoApp", "Build a React Todo App")

    print("\n---------------- LIVE TRACE TEST 3: FASTAPI --------------")
    await project_synthesizer.synthesize_full_project("FastAPICRM", "Build a FastAPI CRM Backend with PostgreSQL")

if __name__ == "__main__":
    asyncio.run(main())
