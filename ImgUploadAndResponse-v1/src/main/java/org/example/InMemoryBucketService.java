package org.example;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class InMemoryBucketService {

    private final Map<String, byte[]> bucket = new ConcurrentHashMap<>();

    public boolean uploadFile(String fileName, byte[] fileContent) {
        if (fileName == null || fileContent == null) {
            return false;
        }
        bucket.put(fileName, fileContent);
        return true;
    }

    public byte[] downloadFile(String fileName) {
        return bucket.get(fileName);
    }
}
