package imgMain;

import H2DB.DatabaseCleanupService;
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
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.List;

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

    @Autowired
    private RenderedImagePoller renderedImagePoller;

    @GetMapping("/sse-rendered-image")
    public SseEmitter streamRenderedImage() {
        return renderedImagePoller.addEmitter();
    }

    @GetMapping("/")
    public String index() {
        return "upload";
    }

    @Autowired
    private DatabaseCleanupService databaseCleanupService;

    @PostMapping("/clear-database")
    public String clearDatabase() {
        databaseCleanupService.clearDatabase();
        return "redirect:/";
    }

    @GetMapping("/images")
    public String showAllImages(Model model) {
        List<ImageEntity> images = imageRepository.findAll();
        model.addAttribute("images", images);
        return "images";
    }


    @PostMapping("/upload")
    public String uploadImage(@RequestParam("file") MultipartFile file, Model model) {
        if (file.isEmpty()) {
            model.addAttribute("error", "ERROR: Nessun file selezionato");
            return "upload";
        }
        try {
            ImageDTO imageDTO = imageService.processImage(file);
            boolean evaluationResult = evaluer.evaluate(imageDTO);
            responseLogic.setMeetsCriteria(evaluationResult);
            if (!evaluationResult) {
                model.addAttribute("error", "ERROR: Immagine troppo grossa o formato sbagliato");
                return "upload";
            }
            String s3ObjectKey = amazonS3Service.uploadFile(imageDTO.getFileName(), file.getBytes());
            if (s3ObjectKey == null) {
                model.addAttribute("error", "ERROR: Failed to upload the file to Bucket");
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
