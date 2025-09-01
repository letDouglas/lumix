package H2DB;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class DatabaseCleanupService {

    @Autowired
    private ImageRepository imageRepository;

    //5 min (300000 ms)
    @Scheduled(fixedRate = 300000)
    @Transactional
    public void clearDatabase() {
        imageRepository.deleteAll();
        System.out.println("H2 database pulito: " + new java.util.Date());
    }
}
