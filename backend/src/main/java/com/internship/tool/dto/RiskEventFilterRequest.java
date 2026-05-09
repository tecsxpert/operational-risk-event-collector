package com.internship.tool.dto;

import lombok.Data;

@Data
public class RiskEventFilterRequest {

    private String keyword;
    private String category;
    private String severity;
    private String status;
}