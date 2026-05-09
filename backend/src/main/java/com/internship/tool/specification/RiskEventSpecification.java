package com.internship.tool.specification;

import com.internship.tool.entity.RiskEvent;
import org.springframework.data.jpa.domain.Specification;

import java.time.LocalDateTime;

public class RiskEventSpecification {

    // 🔍 Keyword search (title + description + AI)
    public static Specification<RiskEvent> hasKeyword(String keyword) {
        return (root, query, cb) -> {
            if (keyword == null || keyword.isBlank()) return null;

            String like = "%" + keyword.toLowerCase() + "%";

            return cb.or(
                    cb.like(cb.lower(root.get("title")), like),
                    cb.like(cb.lower(root.get("description")), like),
                    cb.like(cb.lower(root.get("aiDescription")), like) // 🔥 NEW
            );
        };
    }

    // 📂 Category filter
    public static Specification<RiskEvent> hasCategory(String category) {
        return (root, query, cb) ->
                (category == null || category.isBlank()) ? null :
                        cb.equal(cb.lower(root.get("category")), category.toLowerCase());
    }

    // ⚠️ Severity filter
    public static Specification<RiskEvent> hasSeverity(String severity) {
        return (root, query, cb) ->
                (severity == null || severity.isBlank()) ? null :
                        cb.equal(cb.lower(root.get("severity")), severity.toLowerCase());
    }

    // 📊 Status filter
    public static Specification<RiskEvent> hasStatus(String status) {
        return (root, query, cb) ->
                (status == null || status.isBlank()) ? null :
                        cb.equal(cb.lower(root.get("status")), status.toLowerCase());
    }

    // 📅 FILTER: Created After
    public static Specification<RiskEvent> createdAfter(LocalDateTime fromDate) {
        return (root, query, cb) ->
                (fromDate == null) ? null :
                        cb.greaterThanOrEqualTo(root.get("createdAt"), fromDate);
    }

    // 📅 FILTER: Created Before
    public static Specification<RiskEvent> createdBefore(LocalDateTime toDate) {
        return (root, query, cb) ->
                (toDate == null) ? null :
                        cb.lessThanOrEqualTo(root.get("createdAt"), toDate);
    }

    // 🔥 BONUS: Severity IN (multiple values)
    public static Specification<RiskEvent> hasSeverityIn(String[] severities) {
        return (root, query, cb) -> {
            if (severities == null || severities.length == 0) return null;
            return root.get("severity").in((Object[]) severities);
        };
    }
}