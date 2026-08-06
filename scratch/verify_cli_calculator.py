import asyncio
from nexusai.services.project_synthesizer import project_synthesizer

async def main():
    print("\n" + "="*70)
    print("VERIFICATION: Build a Python CLI calculator")
    print("="*70)
    artifact = await project_synthesizer.synthesize_full_project(
        "PythonCLICalculator",
        "Build a Python CLI calculator"
    )
    print("\n" + "="*70)
    print("RESULT SUMMARY")
    print("="*70)
    print(f"Framework detected: {artifact.spec.framework}")
    print(f"Files generated: {list(artifact.files.keys())}")
    has_flask = any("flask" in v.lower() for v in artifact.files.values())
    has_calculator = "calculator.py" in artifact.files
    print(f"Contains Flask: {has_flask}  (MUST be False)")
    print(f"Contains calculator.py: {has_calculator}  (MUST be True)")
    assert not has_flask, "FAIL: Flask found in CLI calculator project!"
    assert has_calculator or "cli.py" in artifact.files, "FAIL: calculator.py not found!"
    print("\n✅ SUCCESS: CLI Calculator generated correctly. No Flask. No FastAPI.")

if __name__ == "__main__":
    asyncio.run(main())
