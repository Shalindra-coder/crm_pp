frappe.ui.form.on('Lead', {
    // ============================================
    // REAL-TIME SCORE CALCULATION & CHECKBOX AUTO-UPDATE
    // ============================================
    
    // Trigger recalculation on any relevant field change
    onload: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    refresh: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom_local_connections: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom_office_space_franchise: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom_recruitment_investment: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom_target_city: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom_financial_readiness: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom_team_hiring: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom__franchisee_engagement_intent: function(frm) {
        calculate_franchise_qualification_score(frm);
    },
    
    custom_vertical: function(frm) {
        calculate_franchise_qualification_score(frm);
    },

    // ============================================
    // VALIDATION ON SAVE
    // ============================================
    validate: function(frm) {
        if (frm.doc.custom_vertical !== "Franchise") {
            return; // Only apply to Franchise vertical
        }

        // Recalculate score before validation
        let score = calculate_franchise_qualification_score(frm);
        
        const current_status = (frm.doc.status || "").trim();
        const previous_status = (frm.doc.__last_status || "").trim();

        // ============================================
        // PREVENT INVALID STATUS TRANSITIONS
        // ============================================
        if (previous_status === "Converted" && current_status === "Unqualified") {
            frappe.throw({
                title: __("❌ Invalid Status Change"),
                message: __("You cannot move a Converted lead back to Unqualified. Please contact your administrator if you need to reverse this lead.")
            });
        }

        // ============================================
        // QUALIFICATION LOGIC - ONLY AFTER NURTURING
        // ============================================
        const stages_requiring_qualification = ["Qualified", "Converted"];
        
        if (stages_requiring_qualification.includes(current_status)) {
            
            // --- Check Mandatory Checkboxes ---
            const mandatory_checks = [
                { field: "custom_recruitment_investment", label: "Recruitment Investment" },
                { field: "custom_team_hiring", label: "Team Hiring" },
                { field: "custom_target_city", label: "Target City" }
            ];

            let missing_fields = [];
            mandatory_checks.forEach(check => {
                if (!frm.doc[check.field]) {
                    missing_fields.push(check.label);
                }
            });

            // --- If mandatory fields are missing ---
            if (missing_fields.length > 0) {
                frm.set_value("status", "Unqualified");
                
                if (!frm.doc.__validation_msg_shown) {
                    frappe.msgprint({
                        title: __("⚠️ Lead Unqualified"),
                        message: __(`
                            <div style="padding: 15px;">
                                <p style="font-size: 15px; margin-bottom: 15px;">
                                    <strong>Missing Required Criteria:</strong>
                                </p>
                                <ul style="margin-left: 20px; color: #d73a49; font-size: 14px;">
                                    ${missing_fields.map(f => `<li>${f}</li>`).join('')}
                                </ul>
                            </div>
                        `),
                        indicator: "red"
                    });
                    frm.doc.__validation_msg_shown = true;
                }
                
                frappe.validated = false; // Prevent save
                return;
            }

            // --- Check if score is sufficient ---
            if (score < 12) {
                frm.set_value("status", "Unqualified");
                
                if (!frm.doc.__validation_msg_shown) {
                    frappe.msgprint({
                        title: __("⚠️ Lead Unqualified"),
                        message: __(`
                            <div style="padding: 15px; text-align: center;">
                                <div style="padding: 20px; background: #fff3cd; border-left: 4px solid #ffc107; margin: 10px 0;">
                                    <div style="font-size: 18px; font-weight: bold; color: #856404;">
                                        Score: ${score} / 64
                                    </div>
                                    <div style="font-size: 14px; color: #856404; margin-top: 5px;">
                                        Minimum Required: 12
                                    </div>
                                </div>
                            </div>
                        `),
                        indicator: "red"
                    });
                    frm.doc.__validation_msg_shown = true;
                }
                
                frappe.validated = false; // Prevent save
                return;
            }

            // ============================================
            // LEAD QUALIFIED - SHOW SUBTLE ALERT
            // ============================================
            if (current_status !== previous_status) {
                frappe.show_alert({
                    message: __(`✓ Lead Qualified (Score: ${score}/64)`),
                    indicator: 'green'
                }, 5);
            }
        }

        // Reset validation message flag and store current status for next validation
        frm.doc.__validation_msg_shown = false;
        frm.doc.__last_status = current_status;
    }
});

// ============================================
// SCORING & CHECKBOX CALCULATION FUNCTION
// ============================================
function calculate_franchise_qualification_score(frm) {
    // Only calculate for Franchise vertical
    if (frm.doc.custom_vertical !== "Franchise") {
        return 0;
    }

    let score = 0;
    let breakdown = [];

    // --- 1. Local Connections (8 points) ---
    if (frm.doc.custom_local_connections) {
        score += 8;
        breakdown.push("✓ Local Connections: 8 pts");
    } else {
        breakdown.push("✗ Local Connections: 0 pts");
    }

    // --- 2. Office Space (7 points) ---
    if (frm.doc.custom_office_space_franchise) {
        score += 7;
        if (frm.doc.custom_office_space !== 1) {
            frm.set_value("custom_office_space", 1);
        }
        breakdown.push("✓ Office Space: 7 pts");
    } else {
        score += 0;
        if (frm.doc.custom_office_space !== 0) {
            frm.set_value("custom_office_space", 0);
        }
        breakdown.push("✗ Office Space: 0 pts");
    }

    // --- 3. Recruitment Investment (10 points) - MANDATORY ---
    if (frm.doc.custom_recruitment_investment) {
        score += 10;
        breakdown.push("✓ Recruitment Investment: 10 pts");
    } else {
        breakdown.push("✗ Recruitment Investment: 0 pts");
    }

    // --- 4. Target City (9 points) - MANDATORY ---
    if (frm.doc.custom_target_city) {
        score += 9;
        breakdown.push("✓ Target City: 9 pts");
    } else {
        breakdown.push("✗ Target City: 0 pts");
    }

    // --- 5. Financial Readiness (10 points) ---
    if (frm.doc.custom_financial_readiness) {
        score += 10;
        breakdown.push("✓ Financial Readiness: 10 pts");
    } else {
        breakdown.push("✗ Financial Readiness: 0 pts");
    }

    // --- 6. Team Hiring (10 points) - MANDATORY ---
    if (frm.doc.custom_team_hiring) {
        score += 10;
        breakdown.push("✓ Team Hiring: 10 pts");
    } else {
        breakdown.push("✗ Team Hiring: 0 pts");
    }

    // --- 7. Franchisee Engagement Intent (3-10 points) ---
    if (frm.doc.custom__franchisee_engagement_intent) {
        let intent_score = 0;
        switch (frm.doc.custom__franchisee_engagement_intent.trim()) {
            case "Full-time (Active Operational Involvement)":
                intent_score = 10;
                break;
            case "Part-time (Supervisory / Oversight Role)":
                intent_score = 7;
                break;
            case "Undecided / To be discussed":
                intent_score = 3;
                break;
            default:
                intent_score = 0;
        }
        score += intent_score;
        let involvement_value = intent_score > 0 ? 1 : 0;
        if (frm.doc.custom_active_involvement !== involvement_value) {
            frm.set_value("custom_active_involvement", involvement_value);
        }
        if (intent_score > 0) {
            breakdown.push(`✓ Franchisee Engagement (${frm.doc.custom__franchisee_engagement_intent}): ${intent_score} pts`);
        } else {
            breakdown.push("✗ Franchisee Engagement: 0 pts");
        }
    } else {
        if (frm.doc.custom_active_involvement !== 0) {
            frm.set_value("custom_active_involvement", 0);
        }
        breakdown.push("✗ Franchisee Engagement: Not provided");
    }

    // --- Save Final Score ---
    if (frm.doc.custom_qualification_score !== score) {
        frm.set_value("custom_qualification_score", score);
    }
    
    // --- Show Real-Time Score Display ---
    display_franchise_realtime_score(frm, score, breakdown);

    return score;
}

// ============================================
// REAL-TIME SCORE DISPLAY FUNCTION
// ============================================
function display_franchise_realtime_score(frm, score, breakdown) {
    // Check if all mandatory checkboxes are checked
    let all_mandatory_checked = 
        frm.doc.custom_recruitment_investment &&
        frm.doc.custom_team_hiring &&
        frm.doc.custom_target_city;
    
    // Determine if lead qualifies (score >= 12 AND all mandatory checks)
    let qualifies = score >= 12 && all_mandatory_checked;
    
    // Color coding based on qualification status
    let indicator_color = qualifies ? "#28a745" : "#dc3545";
    let indicator_bg = qualifies ? "#d4edda" : "#f8d7da";
    let status_text = qualifies ? "✓ QUALIFIES" : "✗ DOES NOT QUALIFY";
    let icon = qualifies ? "✓" : "⚠";
    
    // Build score breakdown HTML
    let breakdown_html = breakdown.map(item => `<div style="font-size: 11px; padding: 2px 0;">${item}</div>`).join('');
    
    // Create or update the score display card - MINIMAL & COMPACT
    let score_html = `
        <div id="franchise-qualification-banner" style="
            padding: 10px 15px;
            background: ${indicator_bg};
            border-left: 3px solid ${indicator_color};
            border-radius: 4px;
            margin: 8px 0;
            font-size: 13px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: ${indicator_color}; font-weight: 600;">
                    ${icon} Franchise Score: <strong style="font-size: 16px;">${score} / 64</strong>
                </span>
                <span style="color: ${indicator_color}; font-weight: 600; font-size: 12px;">
                    ${status_text}
                </span>
            </div>
            <details style="margin-top: 8px; cursor: pointer;">
                <summary style="font-size: 11px; color: #666; user-select: none;">
                    📊 View Breakdown
                </summary>
                <div style="margin-top: 6px; padding-left: 8px; border-left: 2px solid #ddd; font-size: 11px;">
                    ${breakdown_html || '<div style="color: #999;">No criteria met yet</div>'}
                </div>
            </details>
        </div>
    `;
    
    // Method 1: Update the description of the score field with visual display
    if (frm.fields_dict.custom_qualification_score) {
        frm.set_df_property('custom_qualification_score', 'description', score_html);
    }
    
    // Method 2: Add prominent banner at the top of the form (below funnel)
    if (frm.$wrapper) {
        // Remove ALL qualification banners first to ensure only one is shown
        frm.$wrapper.find('#temp-qualification-banner, #perm-qualification-banner, #ld-qualification-banner, #franchise-qualification-banner, #llc-qualification-banner').remove();
        let $form_layout = frm.$wrapper.find('.form-layout');
        if ($form_layout.length) {
            $form_layout.prepend(score_html);
        }
    }
}

