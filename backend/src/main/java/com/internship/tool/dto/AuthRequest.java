package com.internship.tool.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class AuthRequest {

    @NotBlank(message = "Username is required")
    private String username;

    @NotBlank(message = "Password is required")
    private String password;

    // 🔐 Optional (but validate if provided)
    private String role; // USER or ADMIN
}