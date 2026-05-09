package com.internship.tool.service;

import org.springframework.stereotype.Service;

@Service
public class AiService {

    public String generateRiskDescription(String title, String description) {

        // 🔥 Dummy logic (replace later with real API)
        return "AI Analysis: " + title + " - This event indicates potential risk and requires attention.";
    }
}