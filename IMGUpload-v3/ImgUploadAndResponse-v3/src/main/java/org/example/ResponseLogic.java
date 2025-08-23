package org.example;

import org.springframework.stereotype.Component;

@Component
public class ResponseLogic {

    private boolean meetsCriteria;

    public void setMeetsCriteria(boolean meetsCriteria) {
        this.meetsCriteria = meetsCriteria;
    }

    public boolean isMeetsCriteria() {
        return meetsCriteria;
    }
}
