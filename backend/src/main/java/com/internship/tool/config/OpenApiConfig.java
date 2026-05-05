package com.internship.tool.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {

        return new OpenAPI()

                // 🔥 API INFO (Very Important)
                .info(new Info()
                        .title("Risk Event Management API")
                        .version("1.0")
                        .description("Backend API for managing risk events with AI integration, pagination, filtering, RBAC, and logging")
                        .contact(new Contact()
                                .name("Balasubramanyam Singh")
                                .email("cgbabusingh@gmail.com")
                        )
                )

                // 🔐 Security Requirement
                .addSecurityItem(new SecurityRequirement().addList("bearerAuth"))

                // 🔐 JWT Configuration
                .components(new Components()
                        .addSecuritySchemes("bearerAuth",
                                new SecurityScheme()
                                        .name("Authorization")
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                        )
                );
    }
}