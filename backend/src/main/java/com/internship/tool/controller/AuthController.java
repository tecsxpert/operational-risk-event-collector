package com.internship.tool.controller;

import com.internship.tool.dto.AuthRequest;
import com.internship.tool.dto.AuthResponse;
import com.internship.tool.service.AuthService;

import jakarta.validation.Valid;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

// 🔥 Swagger Imports
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;

@RestController
@RequestMapping("/api/auth")
@Tag(name = "Authentication", description = "APIs for user registration and login")
public class AuthController {

    private final AuthService service;

    public AuthController(AuthService service) {
        this.service = service;
    }

    // ✅ REGISTER
    @Operation(
            summary = "Register a new user",
            description = "Creates a new user with USER or ADMIN role"
    )
    @ApiResponse(responseCode = "200", description = "User registered successfully")
    @PostMapping("/register")
    public ResponseEntity<Map<String, String>> register(
            @Valid @RequestBody AuthRequest request) {

        service.register(request);

        return ResponseEntity.ok(
                Map.of("message", "User registered successfully")
        );
    }

    // ✅ LOGIN
    @Operation(
            summary = "Login user",
            description = "Authenticates user and returns JWT token"
    )
    @ApiResponse(responseCode = "200", description = "Login successful, JWT token returned")
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(
            @Valid @RequestBody AuthRequest request) {

        return ResponseEntity.ok(service.login(request));
    }
}