frappe.ui.form.on('Lead', {
    // ============================================
    // REAL-TIME SCORE CALCULATION & CHECKBOX AUTO-UPDATE
    // ============================================
    
    // Trigger recalculation on any relevant field change
    onload: function(frm) {
        calculate_llc_qualification_score(frm);
    },
    
    refresh: function(frm) {
        calculate_llc_qualification_score(frm);
    },
    
    custom_scope_of_enquiry: function(frm) {
        calculate_llc_qualification_score(frm);
    },
    
    custom_exclusion_of_personal_grievances: function(frm) {
        calculate_llc_qualification_score(frm);
    },
    
    custom_not_a_sub_contracting_lead: function(frm) {
        calculate_llc_qualification_score(frm);
    },
    
    custom_no_of_officesplants: function(frm) {
        calculate_llc_qualification_score(frm);
    },
    
    custom_turnover_in_inr: function(frm) {
        calculate_llc_qualification_score(frm);
    },
    
    custom_vertical: function(frm) {
        calculate_llc_qualification_score(frm);
    },

    // ============================================
    // VALIDATION ON SAVE
    // ============================================
    validate: function(frm) {
        if (frm.doc.custom_vertical !== "Labour Law Advisory & Compliance") {
            return; // Only apply to LLC vertical
        }

        // Recalculate score before validation
        let score = calculate_llc_qualification_score(frm);
        
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
                { field: "custom_scope_of_enquiry", label: "Scope of Enquiry" },
                { field: "custom_exclusion_of_personal_grievances", label: "Exclusion of Personal Grievances" },
                { field: "custom_not_a_sub_contracting_lead", label: "Not a Sub-contracting Lead" }
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
                
                // Only show message once per validation attempt
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
            if (score < 6) {
                frm.set_value("status", "Unqualified");
                
                // Only show message once per validation attempt
                if (!frm.doc.__validation_msg_shown) {
                    frappe.msgprint({
                        title: __("⚠️ Lead Unqualified"),
                        message: __(`
                            <div style="padding: 15px; text-align: center;">
                                <div style="padding: 20px; background: #fff3cd; border-left: 4px solid #ffc107; margin: 10px 0;">
                                    <div style="font-size: 18px; font-weight: bold; color: #856404;">
                                        Score: ${score} / 44
                                    </div>
                                    <div style="font-size: 14px; color: #856404; margin-top: 5px;">
                                        Minimum Required: 6
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
            // Lead meets all criteria - use subtle alert instead of popup
            // Show only if status actually changed to Qualified/Converted
            if (current_status !== previous_status) {
                frappe.show_alert({
                    message: __(`✓ Lead Qualified (Score: ${score}/44)`),
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
function calculate_llc_qualification_score(frm) {
    // Only calculate for Labour Law Advisory & Compliance vertical
    if (frm.doc.custom_vertical !== "Labour Law Advisory & Compliance") {
        return 0;
    }

    let score = 0;
    let breakdown = [];

    // --- 1. Scope of Enquiry (9 points) - MANDATORY ---
    if (frm.doc.custom_scope_of_enquiry) {
        score += 9;
        breakdown.push("✓ Scope of Enquiry: 9 pts");
    } else {
        breakdown.push("✗ Scope of Enquiry: 0 pts");
    }

    // --- 2. Exclusion of Personal Grievances (6 points) - MANDATORY ---
    if (frm.doc.custom_exclusion_of_personal_grievances) {
        score += 6;
        breakdown.push("✓ Exclusion of Personal Grievances: 6 pts");
    } else {
        breakdown.push("✗ Exclusion of Personal Grievances: 0 pts");
    }

    // --- 3. Not a Sub-contracting Lead (9 points) - MANDATORY ---
    if (frm.doc.custom_not_a_sub_contracting_lead) {
        score += 9;
        breakdown.push("✓ Not a Sub-contracting Lead: 9 pts");
    } else {
        breakdown.push("✗ Not a Sub-contracting Lead: 0 pts");
    }

    // --- 4. Number of Offices/Plants (6-10 points) ---
    if (frm.doc.custom_no_of_officesplants) {
        let volume_score = 0;
        switch (frm.doc.custom_no_of_officesplants.trim()) {
            case "1–2   Single / Local Operation":
                volume_score = 6;
                break;
            case "3–10 Regional Presence":
                volume_score = 8;
                break;
            case "11+	 Multi-location / National Presence":
                volume_score = 10;
                break;
            default:
                volume_score = 0;
        }
        score += volume_score;
        let presence_value = volume_score > 0 ? 1 : 0;
        if (frm.doc.custom_multilocation_presence !== presence_value) {
            frm.set_value("custom_multilocation_presence", presence_value);
        }
        if (volume_score > 0) {
            breakdown.push(`✓ Number of Offices/Plants (${frm.doc.custom_no_of_officesplants}): ${volume_score} pts`);
        } else {
            breakdown.push("✗ Number of Offices/Plants: 0 pts");
        }
    } else {
        if (frm.doc.custom_multilocation_presence !== 0) {
            frm.set_value("custom_multilocation_presence", 0);
        }
        breakdown.push("✗ Number of Offices/Plants: Not provided");
    }

    // --- 5. Turnover (6-10 points) ---
    if (frm.doc.custom_turnover_in_inr) {
        let turnover_score = 0;
        switch (frm.doc.custom_turnover_in_inr.trim()) {
            case "Less than 50 Cr":
                turnover_score = 6;
                break;
            case "50 Cr to 200 Cr":
                turnover_score = 8;
                break;
            case "200 and above":
                turnover_score = 10;
                break;
            default:
                turnover_score = 0;
        }
        score += turnover_score;
        let turnover_value = turnover_score > 0 ? 1 : 0;
        if (frm.doc.custom_turnover !== turnover_value) {
            frm.set_value("custom_turnover", turnover_value);
        }
        if (turnover_score > 0) {
            breakdown.push(`✓ Turnover (${frm.doc.custom_turnover_in_inr}): ${turnover_score} pts`);
        } else {
            breakdown.push("✗ Turnover: 0 pts");
        }
    } else {
        if (frm.doc.custom_turnover !== 0) {
            frm.set_value("custom_turnover", 0);
        }
        breakdown.push("✗ Turnover: Not provided");
    }

    // --- Save Final Score ---
    if (frm.doc.custom_qualification_score !== score) {
        frm.set_value("custom_qualification_score", score);
    }
    
    // --- Show Real-Time Score Display ---
    display_llc_realtime_score(frm, score, breakdown);

    return score;
}

// ============================================
// REAL-TIME SCORE DISPLAY FUNCTION
// ============================================
function display_llc_realtime_score(frm, score, breakdown) {
    // Check if all mandatory checkboxes are checked
    let all_mandatory_checked = 
        frm.doc.custom_scope_of_enquiry &&
        frm.doc.custom_exclusion_of_personal_grievances &&
        frm.doc.custom_not_a_sub_contracting_lead;
    
    // Determine if lead qualifies (score >= 6 AND all mandatory checks)
    let qualifies = score >= 6 && all_mandatory_checked;
    
    // Color coding based on qualification status
    let indicator_color = qualifies ? "#28a745" : "#dc3545";
    let indicator_bg = qualifies ? "#d4edda" : "#f8d7da";
    let status_text = qualifies ? "✓ QUALIFIES" : "✗ DOES NOT QUALIFY";
    let icon = qualifies ? "✓" : "⚠";
    
    // Build score breakdown HTML
    let breakdown_html = breakdown.map(item => `<div style="font-size: 11px; padding: 2px 0;">${item}</div>`).join('');
    
    // Create or update the score display card - MINIMAL & COMPACT
    let score_html = `
        <div id="llc-qualification-banner" style="
            padding: 10px 15px;
            background: ${indicator_bg};
            border-left: 3px solid ${indicator_color};
            border-radius: 4px;
            margin: 8px 0;
            font-size: 13px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: ${indicator_color}; font-weight: 600;">
                    ${icon} LLC Qualification Score: <strong style="font-size: 16px;">${score} / 44</strong>
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
    // Remove ALL qualification banners first to ensure only one is shown
    if (frm.$wrapper) {
        frm.$wrapper.find('#temp-qualification-banner, #perm-qualification-banner, #ld-qualification-banner, #franchise-qualification-banner, #llc-qualification-banner').remove();
        
        // Insert the banner right after the form-dashboard (where the funnel is)
        let $form_layout = frm.$wrapper.find('.form-layout');
        if ($form_layout.length) {
            $form_layout.prepend(score_html);
        }
    }
}

