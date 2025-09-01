package imgMain;

import H2DB.ImageEntity;
import H2DB.ImageRepository;
import amazon.AmazonS3Service;
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
import org.springframework.stereotype.Controller;

@Controller
public class ImgController {

    @Autowired
    private ImageService imageService;

    @Autowired
    private Evaluer evaluer;

    @Autowired
    private ResponseLogic responseLogic;

    @Autowired
    private AmazonS3Service amazonS3Service;

    @Autowired
    private ImageRepository imageRepository;

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
            String s3ObjectKey = amazonS3Service.uploadFile(imageDTO.getFileName(), file.getBytes());
            if (s3ObjectKey == null) {
                model.addAttribute("error", "ERROR: Failed to upload the file to S3");
                return "upload";
            }
            ImageEntity imageEntity = new ImageEntity(
                    imageDTO.getFileName(),
                    imageDTO.getFileType(),
                    imageDTO.getFileSize(),
                    imageDTO.getHeight(),
                    imageDTO.getWidth(),
                    s3ObjectKey, // Save the S3 object key
                    file.getBytes() // Save the image binary to H2
            );
            imageRepository.save(imageEntity);
            model.addAttribute("imageDTO", imageDTO);
            model.addAttribute("meetsCriteria", responseLogic.isMeetsCriteria());
            model.addAttribute("uploadSuccess", true);
        } catch (Exception e) {
            e.printStackTrace();
            model.addAttribute("error", "ERROR: An unexpected error occurred");
            return "upload";
        }
        return "result";
    }

    @GetMapping("/download-from-h2/{id}")
    public ResponseEntity<byte[]> downloadFromH2(@PathVariable Long id) {
        ImageEntity imageEntity = imageRepository.findById(id).orElse(null);
        if (imageEntity == null || imageEntity.getImageData() == null) {
            return ResponseEntity.notFound().build();
        }
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType(imageEntity.getFileType()));
        headers.setContentDispositionFormData("attachment", imageEntity.getFileName());
        return ResponseEntity.ok()
                .headers(headers)
                .body(imageEntity.getImageData());
    }

    @GetMapping("/download/{fileName:.+}")
    public ResponseEntity<byte[]> downloadFile(@PathVariable String fileName) {
        byte[] fileContent = amazonS3Service.downloadFile(fileName);
        if (fileContent == null) {
            return ResponseEntity.notFound().build();
        }
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        headers.setContentDispositionFormData("attachment", fileName);
        return ResponseEntity.ok()
                .headers(headers)
                .body(fileContent);
    }
}
