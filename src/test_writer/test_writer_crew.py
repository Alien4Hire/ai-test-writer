from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from test_writer.tools.test_tracker import mark_as_tested
from test_writer.tools.file_scanner import find_target_files
from test_writer.tools.test_runner import run_tests
from test_writer.tools.test_writer import write_test_file
from test_writer.tools.test_repair import repair_tests
from pathlib import Path
import subprocess

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

    def process_file(self, path: str, test_command: str | None = None):
        print(f"\n🚀 Processing: {path}")
        code = Path(path).read_text()

        ext = Path(path).suffix
        test_path = str(Path(path).with_name(Path(path).stem + f'.test{ext}'))

        retries = 0
        test_code = ""

        print("🧠 Calling GPT to generate test file...")
        while retries < 5:
            test_code = write_test_file(code, path)
            print(f"✅ GPT generated test code [Attempt {retries + 1}]")

            Path(test_path).write_text(test_code)
            print(f"📄 Test file written to: {test_path}")

            print("🧪 Running test suite...")
            status, _, err = run_tests(path)

            if status == 0:
                print(f"✅ All tests passed for {path}")
                mark_as_tested({"path": path, "status": "passed"})
                return
            else:
                print(f"❌ Test failed for {path} [Attempt {retries + 1}/5]")
                print("📋 Error excerpt:\n" + err[:400] + "...\n")
                print("🔁 Asking GPT to repair the test file...")
                test_code = repair_tests(code, test_code, err)
                retries += 1

        print(f"⚠️ Gave up on {path} after 5 retries.")
        mark_as_tested({"path": path, "status": "failed"})

    def run_file(self, file_path: str, test_command: str | None = None):
        print(f"\n🔍 Running test writer on single file: {file_path}")
        self.process_file(file_path, test_command)

    def run_folder(self, folder_path: str, test_command: str | None = None):
        print(f"\n🔎 Scanning folder: {folder_path}")
        files = find_target_files(folder_path)
        print(f"📂 Found {len(files)} file(s) to process.")
        for file_path in files:
            self.process_file(file_path, test_command)
