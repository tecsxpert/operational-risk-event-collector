package com.internship.tool.service;

import com.internship.tool.dto.AuthRequest;
import com.internship.tool.dto.AuthResponse;
import com.internship.tool.entity.User;
import com.internship.tool.repository.UserRepository;
import com.internship.tool.security.JwtUtil;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class AuthService {

    private static final Logger log = LoggerFactory.getLogger(AuthService.class);

    private final UserRepository userRepository;
    private final JwtUtil jwtUtil;
    private final PasswordEncoder passwordEncoder;

    public AuthService(UserRepository userRepository,
                       JwtUtil jwtUtil,
                       PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.jwtUtil = jwtUtil;
        this.passwordEncoder = passwordEncoder;
    }

    // REGISTER
    public void register(AuthRequest request) {

        log.info("Registering user: {}", request.getUsername());

        // ✅ Prevent duplicate users
        if (userRepository.findByUsername(request.getUsername()).isPresent()) {
            log.error("User already exists: {}", request.getUsername());
            throw new IllegalArgumentException("Username already exists");
        }

        // 🔐 Safe role assignment
        String role = (request.getRole() != null && request.getRole().equals("ADMIN"))
                ? "ADMIN"
                : "USER";

        User user = User.builder()
                .username(request.getUsername())
                .password(passwordEncoder.encode(request.getPassword()))
                .role(role)
                .build();

        userRepository.save(user);

        log.info("User registered successfully: {}", request.getUsername());
    }

    // LOGIN
    public AuthResponse login(AuthRequest request) {

        log.info("Login attempt for user: {}", request.getUsername());

        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> {
                    log.error("User not found: {}", request.getUsername());
                    return new IllegalArgumentException("User not found");
                });

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            log.error("Invalid password for user: {}", request.getUsername());
            throw new IllegalArgumentException("Invalid password");
        }

        log.info("Login successful for user: {}", request.getUsername());

        String token = jwtUtil.generateToken(user.getUsername(), user.getRole());

        return new AuthResponse(token);
    }
}