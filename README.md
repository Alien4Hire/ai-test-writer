# 🧪 AI Test Writer for JavaScript/TypeScript

Automatically write and maintain unit tests for your JavaScript and TypeScript files using GPT-4 and Jest/Vitest.

This tool runs test coverage, identifies missing coverage in source files, and uses OpenAI to generate test files — only when new tests are actually needed.

---

## ✨ Features

- ✅ Detects uncovered lines of code via `jest --coverage`
- 🧠 Uses GPT-4 to write high-quality test files (Jest or Vitest)
- 🔁 Skips files that are already fully covered
- ♻️ Rewrites or appends tests only if code changes introduce uncovered logic
- 📦 Automatically finds and runs inside the nearest `package.json` directory

---

## 🚀 Installation

1. **Clone this repo:**

   ```bash
   git clone https://github.com/your-username/test-writing-agent.git
   cd test-writing-agent
   ```

2. **Install Python dependencies (requires Python 3.10+):**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies in your JavaScript project:**

   Inside the directory with your `package.json`:

   ```bash
   npm install --save-dev jest
   ```

   (or Vitest if you're using that)

4. **Add this to your `package.json` if not present:**

   ```json
   "scripts": {
     "test": "jest",
     "coverage": "jest --no-cache --coverage --coverageReporters=json"
   }
   ```

---

## 🔧 Configuration

Make sure your project is using **relative imports** like:

```js
const { myFn } = require('./my-module');
```

The generated test files will be named like `example.test.js` and saved alongside the source file.

---

## 🏃 Usage

You can run the script in **single file mode**:

```bash
python -m test_writer.main path/to/your/source/file.js
```

Or extend the logic to run across multiple files (batch mode coming soon).

---

## 📊 What It Does

1. **Runs coverage** on the target file using `npm run coverage`.
2. **Parses the coverage-final.json** file to find uncovered statements.
3. **If any uncovered lines are found**, it:
   - Runs existing tests to see if they still pass.
   - Generates new test code using GPT-4 via OpenAI API.
   - Saves the `.test.js` file in the same directory.
   - Re-runs tests and verifies coverage again.

4. **If no uncovered lines are found**, it skips writing any new tests.

---

## 🧠 GPT Setup

This uses the `openai` Python library to call GPT-4.

Make sure your environment has your OpenAI key set:

```bash
export OPENAI_API_KEY=your-api-key
```

Or define it in your environment config file or `.env`.

---

## 🛠 Example

Suppose you have a file:

```txt
src/utils/math.js
```

Run:

```bash
python -m test_writer.main src/utils/math.js
```

If there are uncovered lines, the script will:

- Generate `src/utils/math.test.js`
- Run `npm test`
- Verify the coverage again

---

## 🧼 Notes

- Files are only re-tested if:
  - New uncovered lines appear
  - Previous test runs failed
- `npx`, `npm`, and Jest must be available on your system
- The test file is **overwritten each time** unless logic is added to merge tests

---

## 💡 Future Features

- [ ] Multi-file or full-project test writing
- [ ] Vitest / Mocha support
- [ ] Merge with existing tests instead of overwrite
- [ ] Git diff analysis for smarter test regeneration

---

## 🧙 Author

Created by Jason Maynard  
[LinkedIn](https://www.linkedin.com/in/jason-maynard-54b538ba)  
[GitHub](https://github.com/Alien4Hire)

---

## 📄 License

MIT License
