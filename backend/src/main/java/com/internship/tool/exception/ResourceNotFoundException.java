package com.internship.tool.exception;

public class ResourceNotFoundException extends RuntimeException {

    public ResourceNotFoundException(String message) {
        super(message);
    }

    // 🔥 STANDARD FORMAT HELPER
    public static ResourceNotFoundException forResource(String resource, String field, Object value) {
        return new ResourceNotFoundException(
                String.format("%s not found with %s: %s", resource, field, value)
        );
    }
}