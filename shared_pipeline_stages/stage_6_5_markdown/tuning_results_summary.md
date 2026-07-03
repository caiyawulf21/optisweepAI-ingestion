# Stage 6.5 Tuning Results Summary

Generated: 2026-07-03T11:51:10.466223Z

See [weight_tuning_experiments.md](weight_tuning_experiments.md) for methodology.

## Comparison

| Experiment | Clusters | Pass-through | Combined max | Embeddings cached |
| --- | ---: | ---: | ---: | ---: |
| `baseline_v0.7_l0.3` | 5 | 389 | 0.6634 | 403 |
| `low_lexical_v0.85_l0.15` | 12 | 328 | 0.7537 | 403 |
| `low_lexical_v0.9_l0.1` | 8 | 290 | 0.7843 | 403 |
| `lower_threshold_min0.58` | 8 | 372 | 0.6634 | 403 |

## Cluster titles by experiment

### `baseline_v0.7_l0.3`

Output: `shared_pipeline_stages/data/output/shared/stage_6_5_tuning/baseline_v0.7_l0.3/`

- cluster_use_the_agv_status_screen_to_identify_current_agv_location_and_presence_of_error_codes (score=0.6634, needs_review): Check Current AGV System Status Using the RMS Page; Open the AGV Status Screen and Check AGV Locations and Current Error Codes; Review Fleet Status On the Overall System AGV Status Screen (+3 more)
- cluster_resend_a_geek_command_from_the_api_screen (score=0.6617, needs_review): Resend A Geek+ Command From The API Screen; Resend Geek Command Using A Command GUID After Geek+ Communication Retry Stops
- cluster_use_execute_agv_command_for_system_recovery (score=0.6357, needs_review): Execute AGV Command To Complete An AGV Task After A Missed RMS Callback; Use Execute AGV Command For System Recovery
- cluster_review_information_categories_on_the_hmi_calculations_screen (score=0.6231, needs_review): Identify Customer-Defined Calculation Types In the Overall System HMI; Review Information Categories on the HMI Calculations Screen
- cluster_explain_the_basic_tipper_tote_handling_sequence (score=0.6213, needs_review): Explain the Basic Tipper Tote Handling Sequence; Identify Tipper Station Controls And Verify The Documented Tote Handling Flow

### `low_lexical_v0.85_l0.15`

Output: `shared_pipeline_stages/data/output/shared/stage_6_5_tuning/low_lexical_v0.85_l0.15/`

- cluster_resend_a_geek_command_from_the_api_screen (score=0.7537, needs_review): Resend A Geek+ Command From The API Screen; Resend Geek Command Using A Command GUID After Geek+ Communication Retry Stops
- cluster_use_the_agv_status_screen_to_identify_current_agv_location_and_presence_of_error_codes (score=0.7514, needs_review): Check Current AGV System Status Using the RMS Page; Distinguish Whether An AGV Is In The System Versus In The Map; Identify Available System Controls and Status Areas on the Viva Overview (+9 more)
- cluster_position_the_gripper_and_lock_out_the_tipper_before_gripper_replacement_removal (score=0.7184, needs_review): Access the Tipping Station HMI Screen; Add An AGV Back Into The System Using Recover AGV; Check Operator Station Fault Beacon To Identify A Tipper Fault (+38 more)
- cluster_remove_a_tote_from_the_system_using_the_hospital_hmi_remove_tote_screen (score=0.6833, needs_review): Remove a tote from the system using the Hospital HMI Remove Tote screen; Remove a Tote From the System
- cluster_shut_down_the_system_from_the_system_api_screen (score=0.6806, needs_review): Place the System into Shutdown from the HMI; Shut Down The System From The System API Screen
- cluster_review_information_categories_on_the_hmi_calculations_screen (score=0.6755, needs_review): Identify Customer-Defined Calculation Types In the Overall System HMI; Review Information Categories on the HMI Calculations Screen
- cluster_verify_trailing_agv_back_fill_during_exchange_fault_recovery (score=0.6529, needs_review): Interpret An AGV Departure Without A Replacement AGV Behind It; Verify Trailing AGV Back Fill During Exchange Fault Recovery
- cluster_reset_tipper_stats_data_on_the_visu_data_screen (score=0.646, needs_review): Manually Reset Tipper Stats From the Overall System Aveva API Page; Reset Tipper Stats Data On The VISU_DATA Screen
- cluster_start_up_the_agv_system (score=0.6437, needs_review): Interpret The High-Level Sort Lifecycle And AGV State Progression; Start Up the AGV System
- cluster_interpret_agv_bump_exception_codes_on_the_bump_fault_screen (score=0.6409, needs_review): Interpret AGV BUMP Exception Codes On The Bump Fault Screen; Interpret AGV Obstacle Alarm Visibility In RMS; Recover An AGV From A BUMP Fault Code
- cluster_add_a_tote_back_into_the_system_using_the_add_tote_screen (score=0.6373, needs_review): Add a Tote Back Into the System Using the Add Tote Screen; Add a Tote Back to the System Using a Station ID; Find A Tote By Entering A Location Number On the Container Selection Screen
- cluster_navigate_to_the_primary_operator_station_hmi_screens (score=0.62, needs_review): Navigate the Viva Main Overview and Open Subscreens; Navigate To The Primary Operator Station HMI Screens

### `low_lexical_v0.9_l0.1`

Output: `shared_pipeline_stages/data/output/shared/stage_6_5_tuning/low_lexical_v0.9_l0.1/`

- cluster_resend_a_geek_command_from_the_api_screen (score=0.7843, likely_same_procedure): Resend A Geek+ Command From The API Screen; Resend Geek Command Using A Command GUID After Geek+ Communication Retry Stops
- cluster_recover_a_non_recoverable_operator_station_motor_fault_by_manually_resetting_and_repositioning_the_tote (score=0.7808, likely_same_procedure): Access the Tipping Station HMI Screen; Add a Tote Back Into the System Using the Add Tote Screen; Add a Tote Back to the System Using a Station ID (+93 more)
- cluster_verify_a_manually_removed_tote_is_returned_with_the_same_tote_id_to_its_original_sorter_position (score=0.7122, needs_review): Remove a tote from the system using the Hospital HMI Remove Tote screen; Remove a Tote From the System; Verify a Manually Removed Tote Is Returned With the Same Tote ID to Its Original Sorter Position
- cluster_shut_down_the_system_from_the_system_api_screen (score=0.7099, needs_review): Place the System into Shutdown from the HMI; Shut Down The System From The System API Screen
- cluster_review_information_categories_on_the_hmi_calculations_screen (score=0.693, needs_review): Identify Customer-Defined Calculation Types In the Overall System HMI; Review Information Categories on the HMI Calculations Screen
- cluster_start_up_the_agv_system (score=0.6717, needs_review): Interpret The High-Level Sort Lifecycle And AGV State Progression; Perform Bag Out to Clear Remaining Totes at End of Sort; Start Up the AGV System
- cluster_reset_tipper_stats_data_on_the_visu_data_screen (score=0.6711, needs_review): Manually Reset Tipper Stats From the Overall System Aveva API Page; Reset Tipper Stats Data On The VISU_DATA Screen
- cluster_navigate_from_the_hospital_hmi_main_menu_to_available_menus (score=0.6448, needs_review): Navigate From the Hospital HMI Main Menu to Available Menus; Navigate the Viva Main Overview and Open Subscreens; Navigate To The Primary Operator Station HMI Screens

### `lower_threshold_min0.58`

Output: `shared_pipeline_stages/data/output/shared/stage_6_5_tuning/lower_threshold_min0.58/`

- cluster_use_the_agv_status_screen_to_identify_current_agv_location_and_presence_of_error_codes (score=0.6634, needs_review): Check Current AGV System Status Using the RMS Page; Distinguish Whether An AGV Is In The System Versus In The Map; Open the AGV Status Screen and Check AGV Locations and Current Error Codes (+6 more)
- cluster_resend_a_geek_command_from_the_api_screen (score=0.6617, needs_review): Resend A Geek+ Command From The API Screen; Resend Geek Command Using A Command GUID After Geek+ Communication Retry Stops
- cluster_use_execute_agv_command_for_system_recovery (score=0.6357, needs_review): Execute AGV Command To Complete An AGV Task After A Missed RMS Callback; Use Aveva AGV Command Functions For Remove Recover Pause All And Resume All; Use Execute AGV Command For System Recovery
- cluster_review_information_categories_on_the_hmi_calculations_screen (score=0.6231, needs_review): Identify Customer-Defined Calculation Types In the Overall System HMI; Review Information Categories on the HMI Calculations Screen
- cluster_start_a_left_or_right_tipper_cycle_using_the_operator_station_push_buttons (score=0.6213, needs_review): Access the Tipping Station HMI Screen; Explain the Basic Tipper Tote Handling Sequence; Identify Main Components At The Operator Station (+4 more)
- cluster_remove_a_tote_from_the_system_using_the_hospital_hmi_remove_tote_screen (score=0.5967, needs_review): Remove a tote from the system using the Hospital HMI Remove Tote screen; Remove a Tote From the System
- cluster_handle_a_tote_at_the_hospital_station_and_return_an_empty_tote_to_the_agv (score=0.594, needs_review): Handle A Tote At The Hospital Station And Return An Empty Tote To The AGV; Identify Why A Tote Was Sent To The Hospital Station; Send An AGV To The Hospital To Drop The Tote And Reinitialize (+1 more)
- cluster_shut_down_the_system_from_the_system_api_screen (score=0.593, needs_review): Place the System into Shutdown from the HMI; Shut Down The System From The System API Screen

## Notes

- Lexical Jaccard uses stopword-filtered tokens (not exact phrases).
- Each experiment directory contains `merge_cluster_review.md` with full runbook descriptions and link explanations.
- Lower lexical weight increases reliance on Azure embedding cosine similarity.
