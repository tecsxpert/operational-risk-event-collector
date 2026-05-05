package com.internship.tool.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;

@Component
public class JwtUtil {

    // ✅ Secure key
    private final SecretKey SECRET_KEY = Keys.secretKeyFor(SignatureAlgorithm.HS256);

    private final long EXPIRATION_TIME = 1000 * 60 * 60; // 1 hour

    // 🔐 Generate Token (with role)
    public String generateToken(String username, String role) {
        return Jwts.builder()
                .setSubject(username)
                .claim("role", role)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(SECRET_KEY)
                .compact();
    }

    // 🔍 Extract Claims
    public Claims extractClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(SECRET_KEY)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    // 🔍 Extract Username
    public String extractUsername(String token) {
        return extractClaims(token).getSubject();
    }

    // 🔍 Extract Role (NEW 🔥)
    public String extractRole(String token) {
        return extractClaims(token).get("role", String.class);
    }

    // 🔍 Check Expiry
    public boolean isTokenExpired(String token) {
        return extractClaims(token).getExpiration().before(new Date());
    }

    // ✅ Validate Token
    public boolean validateToken(String token) {
        try {
            return !isTokenExpired(token);
        } catch (Exception e) {
            return false;
        }
    }
}