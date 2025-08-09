package org.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@org.springframework.stereotype.Controller
public class Controller {

    @Autowired
    private ImageService imageService;

    @Autowired
    private Evaluer evaluer;

    @Autowired
    private ResponseLogic responseLogic;

    @Autowired
    private InMemoryBucketService inMemoryBucketService;

    @GetMapping("/")
    public String index() {
        return "upload";
    }

    @PostMapping("/upload")
    public String uploadImage(@RequestParam("file") MultipartFile file, Model model) {
        if (file.isEmpty()) {
            model.addAttribute("error", "ERROR: No file selected");
            return "upload";
        }

        try {
            ImageDTO imageDTO = imageService.processImage(file);
            boolean evaluationResult = evaluer.evaluate(imageDTO);
            responseLogic.setMeetsCriteria(evaluationResult);

            if (!evaluationResult) {
                model.addAttribute("error", "ERROR: Image too big or wrong file type");
                return "upload";
            }

            // Upload the file to the in-memory bucket only if it meets the criteria
            boolean uploadSuccess = inMemoryBucketService.uploadFile(imageDTO.getFileName(), file.getBytes());
            if (!uploadSuccess) {
                model.addAttribute("error", "ERROR: Failed to upload the file");
                return "upload";
            }

            model.addAttribute("imageDTO", imageDTO);
            model.addAttribute("meetsCriteria", responseLogic.isMeetsCriteria());
            model.addAttribute("uploadSuccess", uploadSuccess);
        } catch (Exception e) {
            e.printStackTrace();
            model.addAttribute("error", "ERROR: An unexpected error occurred");
            return "upload";
        }

        return "result";
    }

    @GetMapping("/download/{fileName:.+}")
    public ResponseEntity<byte[]> downloadFile(@PathVariable String fileName) {
        byte[] fileContent = inMemoryBucketService.downloadFile(fileName);

        if (fileContent == null) {
            return ResponseEntity.notFound().build();
        }

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        headers.setContentDispositionFormData(fileName, fileName);

        return ResponseEntity.ok()
                .headers(headers)
                .body(fileContent);
    }
}
