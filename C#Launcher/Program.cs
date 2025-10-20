using System;
using System.Diagnostics;
using System.IO;

namespace BackendLauncher
{
    class Program
    {
        static void Main(string[] args)
        {
            string exeName = "launcher.exe"; 
            string baseDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, @"..\..\..\.."));
            string exePath = Path.Combine(baseDir, exeName);
            string logDir = Path.Combine(baseDir, "logs");
            string logFile = Path.Combine(logDir, "launcher.log");


            if (!File.Exists(exePath))
            {
                Console.WriteLine($"Error: {exePath} not found.");
                return;
            }

            Console.WriteLine($"Starting backend: {exePath}");

            try
            {
                var process = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = exePath,
                        WorkingDirectory = Path.GetDirectoryName(exePath),
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true
                    }
                };

                process.OutputDataReceived += (s, e) =>
                {
                    if (!string.IsNullOrEmpty(e.Data))
                        File.AppendAllText(logFile, e.Data + Environment.NewLine);
                };
                process.ErrorDataReceived += (s, e) =>
                {
                    if (!string.IsNullOrEmpty(e.Data))
                        File.AppendAllText(logFile, "[ERR] " + e.Data + Environment.NewLine);
                };

                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                Console.WriteLine("Launcher is running. Press Ctrl+C to stop.");
                process.WaitForExit();
            }
            catch (Exception ex)
            {
                File.AppendAllText(logFile, $"Launcher failed: {ex.Message}\n");
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}
