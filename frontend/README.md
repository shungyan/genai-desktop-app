## Install dependencies
```
  sudo apt update
  sudo apt install -y \
    libgtk-3-dev \
    libwebkit2gtk-4.1-dev \
    build-essential \
    curl \
    wget \
    file \
    libssl-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev
  ```

 ## 🧩 1. Create and Set Up React + Vite App
  
  ```
  npm create vite@latest my-tauri-app -- --template react
  cd my-tauri-app
  npm install
  ```
  
  ✅ You now have a working **React + Vite** frontend.
  
  You can test it by running:
  
  ```
  npm run dev
  ```
  
  (You should see: `Local: http://localhost:5173/`)
  
  Press **Ctrl + C** to stop it.
  
  ---
 ## 🦀 2. Install Rust (for Tauri backend)
  
  If you don’t have it yet, install Rust:
  
  ```
  curl https://sh.rustup.rs -sSf | sh
  source ~/.cargo/env
  ```
  
  Check:
  
  ```
  cargo --version
  ```
  
  If it prints a version (e.g., `cargo 1.81.0`), you’re good.
  
  ---
 ## ⚙️ 3. Add Tauri
  
  Now, still inside your `my-tauri-app` folder:
  
  ```
  npm install --save-dev @tauri-apps/cli
  npx tauri init
  ```
  
  🟢 During `tauri init`, just press **Enter** for all prompts — defaults are fine.
  
  This will create a folder:
  
  ```
  src-tauri/
  ┣ Cargo.toml
  ┣ tauri.conf.json
  ┗ icons/
  ```
  
  ---
 ## 🧰 4. Verify  `package.json`  Scripts
  
  Open your `package.json`, and make sure the `"scripts"` section looks like this:
  
  ```
  "scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "tauri": "tauri"
  }
  ```
  
  If `"tauri": "tauri"` is missing, add it manually.
  
  ---
 ## 🪟 5. Run Your Tauri App in Dev Mode
  
  Now start Tauri:
  
  ```
  npm run tauri dev
  ```
  
  ✅ This should:
- Launch your **React app** served by Vite
- Open it in a **native Tauri window**
  
  ---
 ## 🧠 6. Folder Structure (for reference)
  
  Your project now looks like this:
  
  ```
  my-tauri-app/
  ┣ src/               # React code
  ┣ src-tauri/         # Tauri backend (Rust)
  ┣ dist/              # Build output
  ┣ package.json
  ┗ vite.config.js
  ```
  
  ---
 ## ✅ 7. Build Native Executable (Optional)
  
  When you’re ready to make a standalone Linux app:
  
  ```
  npm run tauri build
  ```
  
  The executable will appear in:
  
  ```
  src-tauri/target/release/
  ```
  
  ---
  
  Now you have a **clean, working React + Vite + Tauri app** 🎉
