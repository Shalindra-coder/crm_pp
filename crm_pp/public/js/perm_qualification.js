frappe.ui.form.on('Lead', {
    // ============================================
    // REAL-TIME SCORE CALCULATION & CHECKBOX AUTO-UPDATE
    // ============================================
    
    // Trigger recalculation on any relevant field change
    onload: function(frm) {
        calculate_qualification_score(frm);
    },
    
    refresh: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_company_establishment_year: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_salary_offering: function(frm) {
        calculate_qualification_score(frm);
    },
    
    website: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_recruitment_doability_approved: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_positions_open_from: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_recruitment_volume_perm: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_company_type: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_turnover_in_inr: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_jd_completeness: function(frm) {
        calculate_qualification_score(frm);
    },
    
    custom_vertical: function(frm) {
        calculate_qualification_score(frm);
    },

    // ============================================
    // VALIDATION ON SAVE
    // ============================================
    validate: function(frm) {
        if (frm.doc.custom_vertical !== "Permanent Staffing") {
            return; // Only apply to Permanent Staffing vertical
        }

        // Recalculate score before validation
        let score = calculate_qualification_score(frm);
        
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
                { field: "custom_recruitment_doability_approved", label: "Recruitment Do-ability Approved" },
                { field: "custom_company_age__3_years", label: "Company Age (≥3 Years)" },
                { field: "custom_eligible_mandate_ctc__6l", label: "Eligible Mandate (CTC ≥ 6L)" }
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
                                        Score: ${score} / 100
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
                    message: __(`✓ Lead Qualified (Score: ${score}/100)`),
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
function calculate_qualification_score(frm) {
    // Only calculate for Permanent Staffing vertical
    if (frm.doc.custom_vertical !== "Permanent Staffing") {
        return 0;
    }

    let score = 0;
    let breakdown = [];

    // --- 1. Company Age (6 points) ---
    if (frm.doc.custom_company_establishment_year) {
        let currentYear = new Date().getFullYear();
        let companyAge = currentYear - frm.doc.custom_company_establishment_year;
        if (companyAge >= 3) {
            frm.set_value("custom_company_age__3_years", 1);
            score += 6;
            breakdown.push("✓ Company Age (≥3 years): 6 pts");
        } else {
            frm.set_value("custom_company_age__3_years", 0);
            breakdown.push("✗ Company Age (<3 years): 0 pts");
        }
    } else {
        frm.set_value("custom_company_age__3_years", 0);
        breakdown.push("✗ Company Age: Not provided");
    }

    // --- 2. Salary Offering / CTC (6-10 points) ---
    if (frm.doc.custom_salary_offering) {
        let ctc_score = 0;
        switch (frm.doc.custom_salary_offering.trim()) {
            case "5.01 to 8lakhs": ctc_score = 6; break;
            case "8 to 12LPA": ctc_score = 8; break;
            case "12 to 20 LPA": ctc_score = 9; break;
            case "20.01 and above": ctc_score = 10; break;
            default: ctc_score = 0;
        }
        score += ctc_score;
        frm.set_value("custom_eligible_mandate_ctc__6l", ctc_score > 0 ? 1 : 0);
        if (ctc_score > 0) {
            breakdown.push(`✓ Salary Offering (${frm.doc.custom_salary_offering}): ${ctc_score} pts`);
        } else {
            breakdown.push("✗ Salary Offering: 0 pts");
        }
    } else {
        frm.set_value("custom_eligible_mandate_ctc__6l", 0);
        breakdown.push("✗ Salary Offering: Not provided");
    }

    // --- 3. Website Domain (6 points) ---
    if (frm.doc.website) {
        score += 6;
        frm.set_value("custom_verified_client_websitedomain_check", 1);
        breakdown.push("✓ Verified Website: 6 pts");
    } else {
        frm.set_value("custom_verified_client_websitedomain_check", 0);
        breakdown.push("✗ No Website: 0 pts");
    }

    // --- 4. Recruitment Do-ability (10 points) ---
    if (frm.doc.custom_recruitment_doability_approved) {
        score += 10;
        breakdown.push("✓ Recruitment Do-ability: 10 pts");
    } else {
        breakdown.push("✗ Recruitment Do-ability: 0 pts");
    }

    // --- 5. Positions Open From (5-10 points) ---
    if (frm.doc.custom_positions_open_from) {
        let position_score = 0;
        switch (frm.doc.custom_positions_open_from.trim()) {
            case "Less than 60 Days": 
                position_score = 10; 
                break;
            case "60 to 120 Days": 
                position_score = 5; 
                break;
        }
        score += position_score;
        frm.set_value("custom_recent_openings_60_days", position_score > 0 ? 1 : 0);
        if (position_score > 0) {
            breakdown.push(`✓ Positions Open (${frm.doc.custom_positions_open_from}): ${position_score} pts`);
        } else {
            breakdown.push("✗ Positions Open: 0 pts");
        }
    } else {
        frm.set_value("custom_recent_openings_60_days", 0);
        breakdown.push("✗ Positions Open: Not provided");
    }

    // --- 6. Recruitment Volume (5-10 points) ---
    if (frm.doc.custom_recruitment_volume_perm) {
        let volume_score = 0;
        switch (frm.doc.custom_recruitment_volume_perm.trim()) {
            case "1 to 3": volume_score = 5; break;
            case "4 to 6": volume_score = 6; break;
            case "7 and Above": volume_score = 10; break;
        }
        score += volume_score;
        frm.set_value("custom_multiple_openings", volume_score > 0 ? 1 : 0);
        if (volume_score > 0) {
            breakdown.push(`✓ Recruitment Volume (${frm.doc.custom_recruitment_volume_perm}): ${volume_score} pts`);
        } else {
            breakdown.push("✗ Recruitment Volume: 0 pts");
        }
    } else {
        frm.set_value("custom_multiple_openings", 0);
        breakdown.push("✗ Recruitment Volume: Not provided");
    }

    // --- 7. Company Type (6 points) ---
    if (["Private Limited", "Listed","Proprietorship","Partnership","Limited","LLP"].includes(frm.doc.custom_company_type)) {
        score += 6;
        frm.set_value("custom_company_type_private_ltd__listed", 1);
        breakdown.push(`✓ Company Type (${frm.doc.custom_company_type}): 6 pts`);
    } else {
        frm.set_value("custom_company_type_private_ltd__listed", 0);
        if (frm.doc.custom_company_type) {
            breakdown.push(`✗ Company Type (${frm.doc.custom_company_type}): 0 pts`);
        } else {
            breakdown.push("✗ Company Type: Not provided");
        }
    }

    // --- 8. Turnover (0, 6, 9 points) ---
    if (frm.doc.custom_turnover_in_inr) {
        let turnover_score = 0;
        switch (frm.doc.custom_turnover_in_inr.trim()) {
            case "Less than 50 Cr": turnover_score = 0; break;
            case "50 Cr to 200 Cr": turnover_score = 6; break;
            case "200 Cr and Above": turnover_score = 9; break;
        }
        score += turnover_score;
        frm.set_value("custom_turnover__50_cr", turnover_score > 0 ? 1 : 0);
        if (turnover_score > 0) {
            breakdown.push(`✓ Turnover (${frm.doc.custom_turnover_in_inr}): ${turnover_score} pts`);
        } else {
            breakdown.push(`✗ Turnover (${frm.doc.custom_turnover_in_inr}): 0 pts`);
        }
    } else {
        frm.set_value("custom_turnover__50_cr", 0);
        breakdown.push("✗ Turnover: Not provided");
    }

    // --- 9. JD Completeness (8 points) ---
    if (frm.doc.custom_jd_completeness) {
        score += 8;
        breakdown.push("✓ JD Completeness: 8 pts");
    } else {
        breakdown.push("✗ JD Completeness: 0 pts");
    }

    // --- Save Final Score ---
    frm.set_value("custom_qualification_score", score);
    
    // --- Show Real-Time Score Display ---
    display_realtime_score(frm, score, breakdown);

    return score;
}

// ============================================
// REAL-TIME SCORE DISPLAY FUNCTION
// ============================================
function display_realtime_score(frm, score, breakdown) {
    // Check if all mandatory checkboxes are checked
    let all_mandatory_checked = 
        frm.doc.custom_recruitment_doability_approved &&
        frm.doc.custom_company_age__3_years &&
        frm.doc.custom_eligible_mandate_ctc__6l;
    
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
        <div id="perm-qualification-banner" style="
            padding: 10px 15px;
            background: ${indicator_bg};
            border-left: 3px solid ${indicator_color};
            border-radius: 4px;
            margin: 8px 0;
            font-size: 13px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: ${indicator_color}; font-weight: 600;">
                    ${icon} Permanent Staffing Score: <strong style="font-size: 16px;">${score} / 100</strong>
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

