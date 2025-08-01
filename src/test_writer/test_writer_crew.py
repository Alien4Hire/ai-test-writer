from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from test_writer.tools.test_tracker import mark_as_tested, is_tested, get_logged_coverage
from test_writer.tools.file_scanner import find_target_files
from test_writer.tools.test_runner import run_tests_and_get_coverage
from test_writer.tools.test_writer import write_test_file
from test_writer.tools.test_repair import repair_tests
from pathlib import Path

@CrewBase
class TestWriterCrew():
    """Agentic system to write and verify tests for JavaScript/TypeScript files."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # === AGENTS ===

    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            verbose=True
        )

    @agent
    def repair_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['repair_agent'],
            verbose=True
        )

    # === TASK WRAPPER ===

    @task
    def generate_tests_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_tests_task']
        )

    # === CREW ===

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=[self.generate_tests_task()],
            process=Process.sequential,
            verbose=True
        )

    # === CORE LOGIC ===

    def should_generate_tests(self, path: str) -> bool:
        logged_uncovered = get_logged_coverage(path)
        uncovered_lines, test_passed = run_tests_and_get_coverage(path)

        if not test_passed:
            print("🔁 Existing tests failed. Need regeneration.")
            return True

        if logged_uncovered is None:
            print("📈 No previous coverage logged, generating tests...")
            return True

        if uncovered_lines > logged_uncovered:
            print(f"🟨 Uncovered lines increased from {logged_uncovered} to {uncovered_lines}")
            return True

        print("✅ Coverage unchanged and tests pass. Skipping generation.")
        return False

    def process_file(self, path: str, test_command: str | None = None):
        print(f"\n🚀 Processing: {path}")
        code = Path(path).read_text()

        ext = Path(path).suffix
        test_path = str(Path(path).with_name(Path(path).stem + f'.test{ext}'))

        test_code = ""
        retries = 0

        should_generate = self.should_generate_tests(path)

        if should_generate:
            print("🧠 Calling GPT to generate test file...")
            test_code = write_test_file(code, path)
            print(f"✅ GPT generated test code [Attempt 1]")
            Path(test_path).write_text(test_code)
            print(f"📄 Test file written to: {test_path}")
        else:
            print("ℹ️ Test already written and coverage is good.")
            if Path(test_path).exists():
                test_code = Path(test_path).read_text()
            else:
                print(f"⚠️ Warning: {test_path} marked as tested but file is missing.")

        print("🧪 Running test suite...")
        while retries < 5:
            uncovered_lines, passed = run_tests_and_get_coverage(path)

            if passed:
                print(f"✅ All tests passed for {path}")
                mark_as_tested({"path": path, "status": "passed", "uncovered_lines": uncovered_lines})
                return
            else:
                print(f"❌ Test failed for {path} [Attempt {retries + 1}/5]")
                print("⚠️ Cannot extract specific error because we're using `run_tests_and_get_coverage`")

                if not test_code:
                    print("❌ No test code available to repair. Exiting retry loop.")
                    break

                print("🔁 Asking GPT to repair the test file...")
                test_code = repair_tests(code, test_code, "")
                Path(test_path).write_text(test_code)
                retries += 1

        print(f"⚠️ Gave up on {path} after {retries} retries.")
        mark_as_tested({"path": path, "status": "failed", "uncovered_lines": uncovered_lines})

    def run_file(self, file_path: str, test_command: str | None = None):
        print(f"\n🔍 Running test writer on single file: {file_path}")
        self.process_file(file_path, test_command)

    def run_folder(self, folder_path: str, test_command: str | None = None):
        print(f"\n🔎 Scanning folder: {folder_path}")
        files = find_target_files(folder_path)
        print(f"📂 Found {len(files)} file(s) to process.")
        for file_path in files:
            self.process_file(file_path, test_command)
