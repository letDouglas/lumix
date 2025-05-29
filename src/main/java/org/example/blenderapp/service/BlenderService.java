package org.example.blenderapp.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.*;
import java.util.Objects;

@Service
public class BlenderService {

    private final Path uploadDir = Paths.get("uploads").toAbsolutePath().normalize();
    private final Path processedDir = Paths.get("processed").toAbsolutePath().normalize();
    private final Path blenderScriptPath = Paths.get("src", "blender", "process_fbx.py").toAbsolutePath();

    public BlenderService() throws IOException {
        Files.createDirectories(uploadDir);
        Files.createDirectories(processedDir);

        // Verify Blender is available
        try {
            ProcessBuilder checkPb = new ProcessBuilder("blender", "--version");
            Process checkProcess = checkPb.start();
            if (checkProcess.waitFor() != 0) {
                throw new IllegalStateException("Blender not found or not working properly");
            }
        } catch (Exception e) {
            throw new IllegalStateException("Blender not installed or not in PATH", e);
        }
    }

    public String handleFbxFile(MultipartFile file) throws IOException, InterruptedException {
        String originalFilename = Objects.requireNonNull(file.getOriginalFilename());
        if (!originalFilename.toLowerCase().endsWith(".fbx")) {
            throw new IllegalArgumentException("Only .fbx files are supported");
        }

        Path inputPath = uploadDir.resolve(originalFilename);
        Path outputPath = processedDir.resolve("processed_" + originalFilename);

        // Clean up existing files if they exist
        Files.deleteIfExists(inputPath);
        Files.deleteIfExists(outputPath);

        Files.copy(file.getInputStream(), inputPath);

        ProcessBuilder pb = new ProcessBuilder(
                "blender",
                "--background",
                "--python-expr",
                "import bpy; print('Available importers:', [op for op in dir(bpy.ops.import_scene) if not op.startswith('_')])",
                "--python",
                blenderScriptPath.toString(),
                "--",
                inputPath.toString(),
                outputPath.toString()
        );
        pb.inheritIO();

        pb.redirectErrorStream(true);
        Process process = pb.start();

        // Read output for debugging
        String output = new String(process.getInputStream().readAllBytes());
        System.out.println("Blender output: " + output);

        int exitCode = process.waitFor();

        if (exitCode != 0) {
            throw new RuntimeException("Blender processing failed with exit code " + exitCode + ". Output: " + output);
        }

        if (!Files.exists(outputPath)) {
            throw new IOException("Output file was not created by Blender");
        }

        return outputPath.getFileName().toString();
    }
}
