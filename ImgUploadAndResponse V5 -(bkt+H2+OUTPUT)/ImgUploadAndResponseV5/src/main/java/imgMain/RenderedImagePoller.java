package imgMain;

import H2DB.ImageEntity;
import H2DB.ImageRepository;
import amazon.AmazonS3Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
public class RenderedImagePoller {

    @Autowired
    private ImageRepository imageRepository;

    @Autowired
    private AmazonS3Service amazonS3Service;

    private final List<SseEmitter> emitters = new CopyOnWriteArrayList<>();

    // 15 secondi
    @Scheduled(fixedRate = 15000)
    public void pollForRenderedImage() {
        // Get the last uploaded image from H2
        List<ImageEntity> images = imageRepository.findAll();
        if (images.isEmpty()) return;

        ImageEntity lastImage = images.get(images.size() - 1);
        String originalFileName = lastImage.getFileName();
        String renderedFileName = originalFileName.replace(".", "_rendered.");

        // Check if rendered image exists in bkt
        byte[] renderedImage = amazonS3Service.downloadFile(renderedFileName);
        if (renderedImage != null) {
            for (SseEmitter emitter : emitters) {
                try {
                    emitter.send(SseEmitter.event()
                            .name("renderedImageFound")
                            .data(renderedFileName));
                } catch (IOException e) {
                    emitter.complete();
                    emitters.remove(emitter);
                }
            }
        }
    }

    public SseEmitter addEmitter() {
        SseEmitter emitter = new SseEmitter(300000L); // 5 minutes timeout
        emitters.add(emitter);
        emitter.onCompletion(() -> emitters.remove(emitter));
        emitter.onTimeout(() -> emitters.remove(emitter));
        return emitter;
    }
}
