package org.example;

import org.springframework.stereotype.Component;

@Component
public class Evaluer {

    public boolean evaluate(ImageDTO imageDTO) {
        long maxFileSize = 2 * 1024 * 1024; // 2MB in bytes
        if (imageDTO.getFileSize() > maxFileSize) {
            return false;
        }

        String fileType = imageDTO.getFileType().toLowerCase();
        if (!fileType.equals("image/png") && !fileType.equals("image/jpeg") && !fileType.equals("image/jpg")) {
            return false;
        }

        return true;
    }
}
