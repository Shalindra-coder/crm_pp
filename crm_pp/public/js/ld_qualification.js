frappe.ui.form.on('Lead', {
    // ============================================
    // REAL-TIME SCORE CALCULATION & CHECKBOX AUTO-UPDATE
    // ============================================
    
    // Trigger recalculation on any relevant field change
    onload: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    refresh: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    custom_trainer_availability__scheduling_fit: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    custom_direct_delivery_no_subcontracting: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    custom_b2b_engagement: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    no_of_employees: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    custom_turnover_in_inr: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    custom_requested_training_timeline: function(frm) {
        calculate_ld_qualification_score(frm);
    },
    
    custom_vertical: function(frm) {
        calculate_ld_qualification_score(frm);
    },

    // ============================================
    // VALIDATION ON SAVE
    // ============================================
    validate: function(frm) {
        if (frm.doc.custom_vertical !== "Learning & Development") {
            return; // Only apply to Learning & Development vertical
        }

        // Recalculate score before validation
        let score = calculate_ld_qualification_score(frm);
        
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
            
            // --- Check Mandatory Fields ---
            let missing_fields = [];
            
            if (!frm.doc.no_of_employees) {
                missing_fields.push("Number of Employees / Participants");
            } else if (frm.doc.no_of_employees < 5) {
                missing_fields.push("Number of Employees / Participants (Minimum 5 required)");
            }
            
            if (!frm.doc.custom_requested_training_timeline) {
                missing_fields.push("Requested Training Timeline");
            }

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
            if (score < 20) {
                frm.set_value("status", "Unqualified");
                
                if (!frm.doc.__validation_msg_shown) {
                    frappe.msgprint({
                        title: __("⚠️ Lead Unqualified"),
                        message: __(`
                            <div style="padding: 15px; text-align: center;">
                                <div style="padding: 20px; background: #fff3cd; border-left: 4px solid #ffc107; margin: 10px 0;">
                                    <div style="font-size: 18px; font-weight: bold; color: #856404;">
                                        Score: ${score} / 47
                                    </div>
                                    <div style="font-size: 14px; color: #856404; margin-top: 5px;">
                                        Minimum Required: 20
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
                    message: __(`✓ Lead Qualified (Score: ${score}/47)`),
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
function calculate_ld_qualification_score(frm) {
    // Only calculate for Learning & Development vertical
    if (frm.doc.custom_vertical !== "Learning & Development") {
        return 0;
    }

    let score = 0;
    let breakdown = [];

    // --- 1. Trainer Availability / Scheduling Fit (9 points) ---
    if (frm.doc.custom_trainer_availability__scheduling_fit) {
        score += 9;
        breakdown.push("✓ Trainer Availability / Scheduling Fit: 9 pts");
    } else {
        breakdown.push("✗ Trainer Availability / Scheduling Fit: 0 pts");
    }

    // --- 2. Direct Delivery (No Subcontracting) (9 points) ---
    if (frm.doc.custom_direct_delivery_no_subcontracting) {
        score += 9;
        breakdown.push("✓ Direct Delivery (No Subcontracting): 9 pts");
    } else {
        breakdown.push("✗ Direct Delivery (No Subcontracting): 0 pts");
    }

    // --- 3. B2B Engagement (7 points) ---
    if (frm.doc.custom_b2b_engagement) {
        score += 7;
        breakdown.push("✓ B2B Engagement: 7 pts");
    } else {
        breakdown.push("✗ B2B Engagement: 0 pts");
    }

    // --- 4. Number of Employees / Participants (7 points) - MANDATORY, >= 5 ---
    if (frm.doc.no_of_employees && frm.doc.no_of_employees >= 5) {
        score += 7;
        if (frm.doc.custom_number_of_employees__participants !== 1) {
            frm.set_value("custom_number_of_employees__participants", 1);
        }
        breakdown.push(`✓ Number of Employees / Participants (${frm.doc.no_of_employees}): 7 pts`);
    } else {
        if (frm.doc.custom_number_of_employees__participants !== 0) {
            frm.set_value("custom_number_of_employees__participants", 0);
        }
        if (frm.doc.no_of_employees) {
            breakdown.push(`✗ Number of Employees / Participants (${frm.doc.no_of_employees} - Need ≥5): 0 pts`);
        } else {
            breakdown.push("✗ Number of Employees / Participants: Not provided");
        }
    }

    // --- 5. Turnover (5-9 points) ---
    if (frm.doc.custom_turnover_in_inr) {
        let turnover_score = 0;
        switch (frm.doc.custom_turnover_in_inr.trim()) {
            case "Less than 50 Cr":
                turnover_score = 5;
                break;
            case "50 Cr to 200 Cr":
                turnover_score = 7;
                break;
            case "200 and above":
                turnover_score = 9;
                break;
            default:
                turnover_score = 0;
        }
        score += turnover_score;
        let turnover_value = turnover_score > 0 ? 1 : 0;
        if (frm.doc.custom_turnover_ld !== turnover_value) {
            frm.set_value("custom_turnover_ld", turnover_value);
        }
        if (turnover_score > 0) {
            breakdown.push(`✓ Turnover (${frm.doc.custom_turnover_in_inr}): ${turnover_score} pts`);
        } else {
            breakdown.push("✗ Turnover: 0 pts");
        }
    } else {
        if (frm.doc.custom_turnover_ld !== 0) {
            frm.set_value("custom_turnover_ld", 0);
        }
        breakdown.push("✗ Turnover: Not provided");
    }

    // --- 6. Requested Training Timeline (6-10 points) - MANDATORY ---
    if (frm.doc.custom_requested_training_timeline) {
        let timeline_score = 0;
        switch (frm.doc.custom_requested_training_timeline.trim()) {
            case "Less Than 30 Days":
                timeline_score = 10;
                break;
            case "30 days to 60 Days":
                timeline_score = 8;
                break;
            case "60 Days and Above":
                timeline_score = 6;
                break;
            default:
                timeline_score = 0;
        }
        score += timeline_score;
        let timeline_value = timeline_score > 0 ? 1 : 0;
        if (frm.doc.custom_urgency__timeline !== timeline_value) {
            frm.set_value("custom_urgency__timeline", timeline_value);
        }
        if (timeline_score > 0) {
            breakdown.push(`✓ Requested Training Timeline (${frm.doc.custom_requested_training_timeline}): ${timeline_score} pts`);
        } else {
            breakdown.push("✗ Requested Training Timeline: 0 pts");
        }
    } else {
        if (frm.doc.custom_urgency__timeline !== 0) {
            frm.set_value("custom_urgency__timeline", 0);
        }
        breakdown.push("✗ Requested Training Timeline: Not provided");
    }

    // --- Save Final Score ---
    if (frm.doc.custom_qualification_score !== score) {
        frm.set_value("custom_qualification_score", score);
    }
    
    // --- Show Real-Time Score Display ---
    display_ld_realtime_score(frm, score, breakdown);

    return score;
}

// ============================================
// REAL-TIME SCORE DISPLAY FUNCTION
// ============================================
function display_ld_realtime_score(frm, score, breakdown) {
    // Check if all mandatory criteria are met
    let all_mandatory_met = 
        frm.doc.no_of_employees && frm.doc.no_of_employees >= 5 &&
        frm.doc.custom_requested_training_timeline;
    
    // Determine if lead qualifies (score >= 40 AND all mandatory met)
    let qualifies = score >=20 && all_mandatory_met;
    
    // Color coding based on qualification status
    let indicator_color = qualifies ? "#28a745" : "#dc3545";
    let indicator_bg = qualifies ? "#d4edda" : "#f8d7da";
    let status_text = qualifies ? "✓ QUALIFIES" : "✗ DOES NOT QUALIFY";
    let icon = qualifies ? "✓" : "⚠";
    
    // Build score breakdown HTML
    let breakdown_html = breakdown.map(item => `<div style="font-size: 11px; padding: 2px 0;">${item}</div>`).join('');
    
    // Create or update the score display card - MINIMAL & COMPACT
    let score_html = `
        <div id="ld-qualification-banner" style="
            padding: 10px 15px;
            background: ${indicator_bg};
            border-left: 3px solid ${indicator_color};
            border-radius: 4px;
            margin: 8px 0;
            font-size: 13px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: ${indicator_color}; font-weight: 600;">
                    ${icon} L&D Score: <strong style="font-size: 16px;">${score} / 47</strong>
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

