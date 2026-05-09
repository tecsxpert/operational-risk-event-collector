package com.internship.tool.dto;

import lombok.*;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RiskEventResponse {

    private Long id;
    private String title;
    private String description;
    private String category;
    private String severity;
    private String status;

    // 🔥 NEW FIELD (Day 12)
    private String aiDescription;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}