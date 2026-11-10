// Lean compiler output
// Module: Export
// Imports: public import Init public meta import Init public import Lean
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* l_Lean_Name_mkStr3(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Name_mkStr4(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Name_mkStr2(lean_object*, lean_object*);
lean_object* lean_mk_array(lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Meta_ExprDefEq_0__Lean_Meta_CheckAssignment_cache_spec__0___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Meta_ExprDefEq_0__Lean_Meta_CheckAssignment_findCached_x3f_spec__0___redArg(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
uint64_t lean_uint64_mix_hash(uint64_t, uint64_t);
uint64_t lean_uint64_of_nat(lean_object*);
uint8_t lean_name_eq(lean_object*, lean_object*);
uint64_t lean_string_hash(lean_object*);
lean_object* lean_string_utf8_byte_size(lean_object*);
lean_object* lean_array_push(lean_object*, lean_object*);
lean_object* l_Lean_Environment_getModuleIdxFor_x3f(lean_object*, lean_object*);
lean_object* lean_array_get(lean_object*, lean_object*, lean_object*);
uint8_t lean_usize_dec_lt(size_t, size_t);
lean_object* lean_array_uget_borrowed(lean_object*, size_t);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(lean_object*, lean_object*, lean_object*);
size_t lean_usize_add(size_t, size_t);
extern lean_object* l_Lean_instInhabitedFileMap_default;
extern lean_object* l_Lean_Options_empty;
lean_object* l_Lean_Options_set___at___00Lean_Option_set___at___00__private_Lean_Shell_0__Lean_ShellOptions_process_spec__2_spec__3(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Core_getMaxHeartbeats(lean_object*);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
lean_object* l_Lean_PersistentHashMap_mkEmptyEntriesArray(lean_object*, lean_object*);
lean_object* lean_io_get_num_heartbeats();
lean_object* l_Lean_Name_mkStr1(lean_object*);
lean_object* lean_st_mk_ref(lean_object*);
extern lean_object* l_Lean_inheritedTraceOptions;
lean_object* lean_st_ref_get(lean_object*);
extern lean_object* l_Lean_diagnostics;
uint8_t l_Lean_Option_get___at___00Lean_Elab_addMacroStack___at___00Lean_throwError___at___00Lean_throwErrorAt___at___00Lean_throwUnknownIdentifierAt___at___00Lean_throwUnknownConstantAt___at___00Lean_throwUnknownConstant___at___00Lean_getConstVal___at___00Lean_mkConstWithLevelParams___at___00Lean_Elab_addConstInfo___at___00Lean_Elab_PostprocessTraces_elabStoreTraceAs_spec__3_spec__5_spec__6_spec__9_spec__12_spec__14_spec__16_spec__18_spec__20_spec__21(lean_object*, lean_object*);
extern lean_object* l_Lean_maxRecDepth;
lean_object* l_Lean_Option_get___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0(lean_object*, lean_object*);
lean_object* l_Lean_findDeclarationRanges_x3f___at___00Lean_Linter_EnvLinter_sortResults_spec__0(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_MessageData_toString(lean_object*);
lean_object* l_Lean_InternalExceptionId_getName(lean_object*);
lean_object* lean_st_ref_take(lean_object*);
lean_object* l_Lean_Kernel_enableDiag(lean_object*, uint8_t);
lean_object* lean_st_ref_set(lean_object*, lean_object*);
uint8_t l_Lean_Kernel_isDiagnosticsEnabled(lean_object*);
uint8_t l_Lean_instDecidableEqPosition_decEq(lean_object*, lean_object*);
uint8_t l_List_elem___at___00Lean_Linter_List_indexLinter_spec__1(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_string_memcmp(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_String_Slice_Pos_nextn(lean_object*, lean_object*, lean_object*);
lean_object* l_String_Slice_Pos_skipWhile___at___00Std_Http_Header_ContentLength_parse_spec__0(lean_object*, lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
lean_object* l_Lean_ConstantInfo_type(lean_object*);
lean_object* l_Lean_Expr_getForallBody(lean_object*);
lean_object* l_Lean_Expr_getAppFn(lean_object*);
lean_object* l_Lean_Expr_constName(lean_object*);
uint8_t l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(lean_object*, lean_object*);
lean_object* l_Lean_Environment_getProjectionFnInfo_x3f(lean_object*, lean_object*);
uint8_t l_Lean_Name_hasMacroScopes(lean_object*);
uint8_t l_Lean_Meta_isMatcherCore(lean_object*, lean_object*);
uint8_t l_Lean_isAuxRecursor(lean_object*, lean_object*);
uint8_t l_Lean_isNoConfusion(lean_object*, lean_object*);
uint8_t l_Lean_Environment_contains(lean_object*, lean_object*, uint8_t);
uint8_t l_Lean_isPrivateName(lean_object*);
lean_object* l_Lean_privateToUserName(lean_object*);
lean_object* l_Std_Format_pretty(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_PrettyPrinter_ppSignature(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_array_uget(lean_object*, size_t);
lean_object* lean_array_uset(lean_object*, size_t, lean_object*);
lean_object* l_String_toName(lean_object*);
lean_object* l_Lean_Name_getRoot(lean_object*);
lean_object* l_mkPanicMessageWithDecl(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_panic_fn_borrowed(lean_object*, lean_object*);
uint8_t l_List_isEmpty___redArg(lean_object*);
uint8_t l_Std_DHashMap_Internal_Raw_u2080_contains___at___00Lean_Server_FileWorker_handleResolveImportAllUnknownIdentifiersCodeAction_x3f_spec__2___redArg(lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insertIfNew___at___00__private_Lean_Linter_Extra_UnreachableTactic_0__Lean_Linter_Extra_UnreachableTactic_initFn_00___x40_Lean_Linter_Extra_UnreachableTactic_949854657____hygCtx___hyg_2__spec__0___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__0___redArg(lean_object*, lean_object*);
lean_object* l_Lean_Environment_find_x3f(lean_object*, lean_object*, uint8_t);
lean_object* l_Lean_Expr_getUsedConstants(lean_object*);
lean_object* lean_array_to_list(lean_object*);
lean_object* l_List_appendTR___redArg(lean_object*, lean_object*);
uint8_t l_Option_instBEq_beq___at___00Lean_PostprocessTraces_ofClass_spec__0(lean_object*, lean_object*);
lean_object* l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(lean_object*, uint8_t);
uint8_t lean_usize_dec_eq(size_t, size_t);
size_t lean_array_size(lean_object*);
lean_object* lean_array_get_size(lean_object*);
uint64_t lean_uint64_shift_right(uint64_t, uint64_t);
uint64_t lean_uint64_xor(uint64_t, uint64_t);
size_t lean_uint64_to_usize(uint64_t);
size_t lean_usize_of_nat(lean_object*);
size_t lean_usize_sub(size_t, size_t);
size_t lean_usize_land(size_t, size_t);
lean_object* l_Lean_Meta_ppExpr(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(lean_object*);
lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00__private_Lean_Elab_DocString_Builtin_0__Lean_Doc_validateCat_spec__3___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
extern lean_object* l___private_Lean_Util_CollectAxioms_0__Lean_instInhabitedExportedAxiomsState;
lean_object* l_Lean_Environment_setExporting(lean_object*, uint8_t);
extern lean_object* l___private_Lean_Util_CollectAxioms_0__Lean_exportedAxiomsExt;
lean_object* l_Lean_PersistentEnvExtension_getState___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l___private_Lean_Util_CollectAxioms_0__Lean_ExportedAxiomsState_find_x3f___boxed(lean_object*, lean_object*, lean_object*);
lean_object* l___private_Lean_Util_CollectAxioms_0__Lean_CollectAxioms_collectAndGet___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l___private_Lean_Util_CollectAxioms_0__Lean_CollectAxioms_runM___redArg(lean_object*, lean_object*);
lean_object* lean_io_mono_ms_now();
lean_object* lean_array_fswap(lean_object*, lean_object*, lean_object*);
lean_object* lean_array_fget_borrowed(lean_object*, lean_object*);
uint8_t lean_string_dec_lt(lean_object*, lean_object*);
lean_object* l_Lean_ConstantInfo_levelParams(lean_object*);
lean_object* l_Array_append___redArg(lean_object*, lean_object*);
lean_object* l_Lean_Environment_header(lean_object*);
lean_object* l_Lean_EnvironmentHeader_moduleNames(lean_object*);
lean_object* l_Lean_findSysroot(lean_object*);
lean_object* l_Lean_initSearchPath(lean_object*, lean_object*);
lean_object* lean_enable_initializer_execution();
lean_object* l_IO_FS_lines(lean_object*);
lean_object* l_Lean_JsonNumber_fromNat(lean_object*);
lean_object* l_Array_extract___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Json_mkObj(lean_object*);
lean_object* l_Lean_Json_pretty(lean_object*, lean_object*);
lean_object* l_IO_FS_writeFile(lean_object*, lean_object*);
lean_object* l_String_Slice_toNat_x21(lean_object*);
lean_object* lean_string_append(lean_object*, lean_object*);
lean_object* l_Nat_reprFast(lean_object*);
lean_object* l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lean_io_prim_handle_mk(lean_object*, uint8_t);
lean_object* lean_nat_mod(lean_object*, lean_object*);
lean_object* l_Lean_Json_compress(lean_object*);
lean_object* l_IO_FS_Handle_putStrLn(lean_object*, lean_object*);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
lean_object* l_List_reverse___redArg(lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Server_Watchdog_handleRename_spec__1___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insert___at___00Lean_Server_Test_Cancel_mkTestTask_spec__1___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lean_uint64_to_nat(uint64_t);
lean_object* l_Nat_toDigits(lean_object*, lean_object*);
lean_object* lean_string_mk(lean_object*);
lean_object* l___private_Init_Data_Nat_Basic_0__Nat_repeatTR_loop___at___00Std_Time_instToStringDuration_leftPad_spec__0(lean_object*, lean_object*);
lean_object* lean_nat_log2(lean_object*);
uint8_t l_Lean_isClass(lean_object*, lean_object*);
uint8_t l_Lean_Meta_isInstanceCore(lean_object*, lean_object*);
lean_object* l_Lean_findDocString_x3f(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_findDeclarationRanges_x3f___at___00Lean_Linter_EnvLinter_sortResults_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_String_Slice_toString(lean_object*);
uint64_t l___private_Lean_Meta_Basic_0__Lean_Meta_Config_toKey(lean_object*);
lean_object* l_Lean_Meta_isProp(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t l_Lean_isStructure(lean_object*, lean_object*);
lean_object* lean_io_prim_handle_flush(lean_object*);
lean_object* lean_array_fget(lean_object*, lean_object*);
lean_object* lean_nat_shiftr(lean_object*, lean_object*);
lean_object* l_Lean_importModules(lean_object*, lean_object*, uint32_t, lean_object*, uint8_t, uint8_t, uint8_t, lean_object*);
lean_object* l_Lean_Environment_constants(lean_object*);
lean_object* l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00Lean_Kernel_Environment_replay_spec__2(lean_object*, size_t, size_t, lean_object*);
uint8_t lean_string_dec_eq(lean_object*, lean_object*);
static const lean_string_object l_NsExport_projectRoots___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "NavierStokes"};
static const lean_object* l_NsExport_projectRoots___closed__0 = (const lean_object*)&l_NsExport_projectRoots___closed__0_value;
static const lean_ctor_object l_NsExport_projectRoots___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_projectRoots___closed__0_value),LEAN_SCALAR_PTR_LITERAL(254, 13, 58, 167, 114, 207, 206, 89)}};
static const lean_object* l_NsExport_projectRoots___closed__1 = (const lean_object*)&l_NsExport_projectRoots___closed__1_value;
static const lean_string_object l_NsExport_projectRoots___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "Euler"};
static const lean_object* l_NsExport_projectRoots___closed__2 = (const lean_object*)&l_NsExport_projectRoots___closed__2_value;
static const lean_ctor_object l_NsExport_projectRoots___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_projectRoots___closed__2_value),LEAN_SCALAR_PTR_LITERAL(65, 209, 97, 245, 187, 19, 151, 148)}};
static const lean_object* l_NsExport_projectRoots___closed__3 = (const lean_object*)&l_NsExport_projectRoots___closed__3_value;
static const lean_string_object l_NsExport_projectRoots___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "ComparatorChallenges"};
static const lean_object* l_NsExport_projectRoots___closed__4 = (const lean_object*)&l_NsExport_projectRoots___closed__4_value;
static const lean_ctor_object l_NsExport_projectRoots___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_projectRoots___closed__4_value),LEAN_SCALAR_PTR_LITERAL(152, 154, 184, 93, 2, 207, 180, 225)}};
static const lean_object* l_NsExport_projectRoots___closed__5 = (const lean_object*)&l_NsExport_projectRoots___closed__5_value;
static const lean_ctor_object l_NsExport_projectRoots___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_projectRoots___closed__5_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l_NsExport_projectRoots___closed__6 = (const lean_object*)&l_NsExport_projectRoots___closed__6_value;
static const lean_ctor_object l_NsExport_projectRoots___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_projectRoots___closed__3_value),((lean_object*)&l_NsExport_projectRoots___closed__6_value)}};
static const lean_object* l_NsExport_projectRoots___closed__7 = (const lean_object*)&l_NsExport_projectRoots___closed__7_value;
static const lean_ctor_object l_NsExport_projectRoots___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_projectRoots___closed__1_value),((lean_object*)&l_NsExport_projectRoots___closed__7_value)}};
static const lean_object* l_NsExport_projectRoots___closed__8 = (const lean_object*)&l_NsExport_projectRoots___closed__8_value;
LEAN_EXPORT const lean_object* l_NsExport_projectRoots = (const lean_object*)&l_NsExport_projectRoots___closed__8_value;
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorIdx(lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorElim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorElim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_primary_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_primary_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_body_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_body_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_ctor_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_ctor_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_derived_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_derived_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_dropped_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_dropped_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_external_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_external_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_orphan_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_orphan_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_instInhabitedCls_default;
LEAN_EXPORT lean_object* l_NsExport_instInhabitedCls;
LEAN_EXPORT uint8_t l_NsExport_instBEqCls_beq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_instBEqCls_beq___boxed(lean_object*, lean_object*);
static const lean_closure_object l_NsExport_instBEqCls___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_NsExport_instBEqCls_beq___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* l_NsExport_instBEqCls___closed__0 = (const lean_object*)&l_NsExport_instBEqCls___closed__0_value;
LEAN_EXPORT const lean_object* l_NsExport_instBEqCls = (const lean_object*)&l_NsExport_instBEqCls___closed__0_value;
static const lean_string_object l_NsExport_softNames___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "else_eq"};
static const lean_object* l_NsExport_softNames___closed__0 = (const lean_object*)&l_NsExport_softNames___closed__0_value;
static const lean_string_object l_NsExport_softNames___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "ofNat_ctorIdx"};
static const lean_object* l_NsExport_softNames___closed__1 = (const lean_object*)&l_NsExport_softNames___closed__1_value;
static const lean_string_object l_NsExport_softNames___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "ctorIdx_ofNat"};
static const lean_object* l_NsExport_softNames___closed__2 = (const lean_object*)&l_NsExport_softNames___closed__2_value;
static const lean_string_object l_NsExport_softNames___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 16, .m_capacity = 16, .m_length = 15, .m_data = "toCtorIdx_ofNat"};
static const lean_object* l_NsExport_softNames___closed__3 = (const lean_object*)&l_NsExport_softNames___closed__3_value;
static const lean_string_object l_NsExport_softNames___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 16, .m_capacity = 16, .m_length = 15, .m_data = "ofNat_toCtorIdx"};
static const lean_object* l_NsExport_softNames___closed__4 = (const lean_object*)&l_NsExport_softNames___closed__4_value;
static const lean_ctor_object l_NsExport_softNames___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__4_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l_NsExport_softNames___closed__5 = (const lean_object*)&l_NsExport_softNames___closed__5_value;
static const lean_ctor_object l_NsExport_softNames___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__3_value),((lean_object*)&l_NsExport_softNames___closed__5_value)}};
static const lean_object* l_NsExport_softNames___closed__6 = (const lean_object*)&l_NsExport_softNames___closed__6_value;
static const lean_ctor_object l_NsExport_softNames___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__2_value),((lean_object*)&l_NsExport_softNames___closed__6_value)}};
static const lean_object* l_NsExport_softNames___closed__7 = (const lean_object*)&l_NsExport_softNames___closed__7_value;
static const lean_ctor_object l_NsExport_softNames___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__1_value),((lean_object*)&l_NsExport_softNames___closed__7_value)}};
static const lean_object* l_NsExport_softNames___closed__8 = (const lean_object*)&l_NsExport_softNames___closed__8_value;
static const lean_ctor_object l_NsExport_softNames___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__0_value),((lean_object*)&l_NsExport_softNames___closed__8_value)}};
static const lean_object* l_NsExport_softNames___closed__9 = (const lean_object*)&l_NsExport_softNames___closed__9_value;
static const lean_string_object l_NsExport_softNames___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "ndrecOn"};
static const lean_object* l_NsExport_softNames___closed__10 = (const lean_object*)&l_NsExport_softNames___closed__10_value;
static const lean_string_object l_NsExport_softNames___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "inj_iff"};
static const lean_object* l_NsExport_softNames___closed__11 = (const lean_object*)&l_NsExport_softNames___closed__11_value;
static const lean_string_object l_NsExport_softNames___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "eq_iff"};
static const lean_object* l_NsExport_softNames___closed__12 = (const lean_object*)&l_NsExport_softNames___closed__12_value;
static const lean_string_object l_NsExport_softNames___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "congr"};
static const lean_object* l_NsExport_softNames___closed__13 = (const lean_object*)&l_NsExport_softNames___closed__13_value;
static const lean_string_object l_NsExport_softNames___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "match_pattern"};
static const lean_object* l_NsExport_softNames___closed__14 = (const lean_object*)&l_NsExport_softNames___closed__14_value;
static const lean_ctor_object l_NsExport_softNames___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__14_value),((lean_object*)&l_NsExport_softNames___closed__9_value)}};
static const lean_object* l_NsExport_softNames___closed__15 = (const lean_object*)&l_NsExport_softNames___closed__15_value;
static const lean_ctor_object l_NsExport_softNames___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__13_value),((lean_object*)&l_NsExport_softNames___closed__15_value)}};
static const lean_object* l_NsExport_softNames___closed__16 = (const lean_object*)&l_NsExport_softNames___closed__16_value;
static const lean_ctor_object l_NsExport_softNames___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__12_value),((lean_object*)&l_NsExport_softNames___closed__16_value)}};
static const lean_object* l_NsExport_softNames___closed__17 = (const lean_object*)&l_NsExport_softNames___closed__17_value;
static const lean_ctor_object l_NsExport_softNames___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__11_value),((lean_object*)&l_NsExport_softNames___closed__17_value)}};
static const lean_object* l_NsExport_softNames___closed__18 = (const lean_object*)&l_NsExport_softNames___closed__18_value;
static const lean_ctor_object l_NsExport_softNames___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__10_value),((lean_object*)&l_NsExport_softNames___closed__18_value)}};
static const lean_object* l_NsExport_softNames___closed__19 = (const lean_object*)&l_NsExport_softNames___closed__19_value;
static const lean_string_object l_NsExport_softNames___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "splitter"};
static const lean_object* l_NsExport_softNames___closed__20 = (const lean_object*)&l_NsExport_softNames___closed__20_value;
static const lean_string_object l_NsExport_softNames___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "hinj"};
static const lean_object* l_NsExport_softNames___closed__21 = (const lean_object*)&l_NsExport_softNames___closed__21_value;
static const lean_string_object l_NsExport_softNames___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "binductionOn"};
static const lean_object* l_NsExport_softNames___closed__22 = (const lean_object*)&l_NsExport_softNames___closed__22_value;
static const lean_string_object l_NsExport_softNames___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "rec"};
static const lean_object* l_NsExport_softNames___closed__23 = (const lean_object*)&l_NsExport_softNames___closed__23_value;
static const lean_string_object l_NsExport_softNames___closed__24_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "ndrec"};
static const lean_object* l_NsExport_softNames___closed__24 = (const lean_object*)&l_NsExport_softNames___closed__24_value;
static const lean_ctor_object l_NsExport_softNames___closed__25_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__24_value),((lean_object*)&l_NsExport_softNames___closed__19_value)}};
static const lean_object* l_NsExport_softNames___closed__25 = (const lean_object*)&l_NsExport_softNames___closed__25_value;
static const lean_ctor_object l_NsExport_softNames___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__23_value),((lean_object*)&l_NsExport_softNames___closed__25_value)}};
static const lean_object* l_NsExport_softNames___closed__26 = (const lean_object*)&l_NsExport_softNames___closed__26_value;
static const lean_ctor_object l_NsExport_softNames___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__22_value),((lean_object*)&l_NsExport_softNames___closed__26_value)}};
static const lean_object* l_NsExport_softNames___closed__27 = (const lean_object*)&l_NsExport_softNames___closed__27_value;
static const lean_ctor_object l_NsExport_softNames___closed__28_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__21_value),((lean_object*)&l_NsExport_softNames___closed__27_value)}};
static const lean_object* l_NsExport_softNames___closed__28 = (const lean_object*)&l_NsExport_softNames___closed__28_value;
static const lean_ctor_object l_NsExport_softNames___closed__29_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__20_value),((lean_object*)&l_NsExport_softNames___closed__28_value)}};
static const lean_object* l_NsExport_softNames___closed__29 = (const lean_object*)&l_NsExport_softNames___closed__29_value;
static const lean_string_object l_NsExport_softNames___closed__30_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "toCtorIdx"};
static const lean_object* l_NsExport_softNames___closed__30 = (const lean_object*)&l_NsExport_softNames___closed__30_value;
static const lean_string_object l_NsExport_softNames___closed__31_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "ofNat"};
static const lean_object* l_NsExport_softNames___closed__31 = (const lean_object*)&l_NsExport_softNames___closed__31_value;
static const lean_string_object l_NsExport_softNames___closed__32_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "elim"};
static const lean_object* l_NsExport_softNames___closed__32 = (const lean_object*)&l_NsExport_softNames___closed__32_value;
static const lean_string_object l_NsExport_softNames___closed__33_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "ctorElim"};
static const lean_object* l_NsExport_softNames___closed__33 = (const lean_object*)&l_NsExport_softNames___closed__33_value;
static const lean_string_object l_NsExport_softNames___closed__34_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "ctorElimType"};
static const lean_object* l_NsExport_softNames___closed__34 = (const lean_object*)&l_NsExport_softNames___closed__34_value;
static const lean_ctor_object l_NsExport_softNames___closed__35_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__34_value),((lean_object*)&l_NsExport_softNames___closed__29_value)}};
static const lean_object* l_NsExport_softNames___closed__35 = (const lean_object*)&l_NsExport_softNames___closed__35_value;
static const lean_ctor_object l_NsExport_softNames___closed__36_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__33_value),((lean_object*)&l_NsExport_softNames___closed__35_value)}};
static const lean_object* l_NsExport_softNames___closed__36 = (const lean_object*)&l_NsExport_softNames___closed__36_value;
static const lean_ctor_object l_NsExport_softNames___closed__37_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__32_value),((lean_object*)&l_NsExport_softNames___closed__36_value)}};
static const lean_object* l_NsExport_softNames___closed__37 = (const lean_object*)&l_NsExport_softNames___closed__37_value;
static const lean_ctor_object l_NsExport_softNames___closed__38_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__31_value),((lean_object*)&l_NsExport_softNames___closed__37_value)}};
static const lean_object* l_NsExport_softNames___closed__38 = (const lean_object*)&l_NsExport_softNames___closed__38_value;
static const lean_ctor_object l_NsExport_softNames___closed__39_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__30_value),((lean_object*)&l_NsExport_softNames___closed__38_value)}};
static const lean_object* l_NsExport_softNames___closed__39 = (const lean_object*)&l_NsExport_softNames___closed__39_value;
static const lean_string_object l_NsExport_softNames___closed__40_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "casesOn"};
static const lean_object* l_NsExport_softNames___closed__40 = (const lean_object*)&l_NsExport_softNames___closed__40_value;
static const lean_string_object l_NsExport_softNames___closed__41_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "recOn"};
static const lean_object* l_NsExport_softNames___closed__41 = (const lean_object*)&l_NsExport_softNames___closed__41_value;
static const lean_string_object l_NsExport_softNames___closed__42_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "noConfusion"};
static const lean_object* l_NsExport_softNames___closed__42 = (const lean_object*)&l_NsExport_softNames___closed__42_value;
static const lean_string_object l_NsExport_softNames___closed__43_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 16, .m_capacity = 16, .m_length = 15, .m_data = "noConfusionType"};
static const lean_object* l_NsExport_softNames___closed__43 = (const lean_object*)&l_NsExport_softNames___closed__43_value;
static const lean_string_object l_NsExport_softNames___closed__44_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "ctorIdx"};
static const lean_object* l_NsExport_softNames___closed__44 = (const lean_object*)&l_NsExport_softNames___closed__44_value;
static const lean_ctor_object l_NsExport_softNames___closed__45_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__44_value),((lean_object*)&l_NsExport_softNames___closed__39_value)}};
static const lean_object* l_NsExport_softNames___closed__45 = (const lean_object*)&l_NsExport_softNames___closed__45_value;
static const lean_ctor_object l_NsExport_softNames___closed__46_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__43_value),((lean_object*)&l_NsExport_softNames___closed__45_value)}};
static const lean_object* l_NsExport_softNames___closed__46 = (const lean_object*)&l_NsExport_softNames___closed__46_value;
static const lean_ctor_object l_NsExport_softNames___closed__47_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__42_value),((lean_object*)&l_NsExport_softNames___closed__46_value)}};
static const lean_object* l_NsExport_softNames___closed__47 = (const lean_object*)&l_NsExport_softNames___closed__47_value;
static const lean_ctor_object l_NsExport_softNames___closed__48_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__41_value),((lean_object*)&l_NsExport_softNames___closed__47_value)}};
static const lean_object* l_NsExport_softNames___closed__48 = (const lean_object*)&l_NsExport_softNames___closed__48_value;
static const lean_ctor_object l_NsExport_softNames___closed__49_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__40_value),((lean_object*)&l_NsExport_softNames___closed__48_value)}};
static const lean_object* l_NsExport_softNames___closed__49 = (const lean_object*)&l_NsExport_softNames___closed__49_value;
static const lean_string_object l_NsExport_softNames___closed__50_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "fun_cases"};
static const lean_object* l_NsExport_softNames___closed__50 = (const lean_object*)&l_NsExport_softNames___closed__50_value;
static const lean_string_object l_NsExport_softNames___closed__51_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "fun_cases_unfolding"};
static const lean_object* l_NsExport_softNames___closed__51 = (const lean_object*)&l_NsExport_softNames___closed__51_value;
static const lean_string_object l_NsExport_softNames___closed__52_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "mutual_induct"};
static const lean_object* l_NsExport_softNames___closed__52 = (const lean_object*)&l_NsExport_softNames___closed__52_value;
static const lean_string_object l_NsExport_softNames___closed__53_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "below"};
static const lean_object* l_NsExport_softNames___closed__53 = (const lean_object*)&l_NsExport_softNames___closed__53_value;
static const lean_string_object l_NsExport_softNames___closed__54_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "brecOn"};
static const lean_object* l_NsExport_softNames___closed__54 = (const lean_object*)&l_NsExport_softNames___closed__54_value;
static const lean_ctor_object l_NsExport_softNames___closed__55_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__54_value),((lean_object*)&l_NsExport_softNames___closed__49_value)}};
static const lean_object* l_NsExport_softNames___closed__55 = (const lean_object*)&l_NsExport_softNames___closed__55_value;
static const lean_ctor_object l_NsExport_softNames___closed__56_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__53_value),((lean_object*)&l_NsExport_softNames___closed__55_value)}};
static const lean_object* l_NsExport_softNames___closed__56 = (const lean_object*)&l_NsExport_softNames___closed__56_value;
static const lean_ctor_object l_NsExport_softNames___closed__57_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__52_value),((lean_object*)&l_NsExport_softNames___closed__56_value)}};
static const lean_object* l_NsExport_softNames___closed__57 = (const lean_object*)&l_NsExport_softNames___closed__57_value;
static const lean_ctor_object l_NsExport_softNames___closed__58_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__51_value),((lean_object*)&l_NsExport_softNames___closed__57_value)}};
static const lean_object* l_NsExport_softNames___closed__58 = (const lean_object*)&l_NsExport_softNames___closed__58_value;
static const lean_ctor_object l_NsExport_softNames___closed__59_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__50_value),((lean_object*)&l_NsExport_softNames___closed__58_value)}};
static const lean_object* l_NsExport_softNames___closed__59 = (const lean_object*)&l_NsExport_softNames___closed__59_value;
static const lean_string_object l_NsExport_softNames___closed__60_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "inj"};
static const lean_object* l_NsExport_softNames___closed__60 = (const lean_object*)&l_NsExport_softNames___closed__60_value;
static const lean_string_object l_NsExport_softNames___closed__61_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "ext"};
static const lean_object* l_NsExport_softNames___closed__61 = (const lean_object*)&l_NsExport_softNames___closed__61_value;
static const lean_string_object l_NsExport_softNames___closed__62_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "ext_iff"};
static const lean_object* l_NsExport_softNames___closed__62 = (const lean_object*)&l_NsExport_softNames___closed__62_value;
static const lean_string_object l_NsExport_softNames___closed__63_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "induct"};
static const lean_object* l_NsExport_softNames___closed__63 = (const lean_object*)&l_NsExport_softNames___closed__63_value;
static const lean_string_object l_NsExport_softNames___closed__64_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 17, .m_capacity = 17, .m_length = 16, .m_data = "induct_unfolding"};
static const lean_object* l_NsExport_softNames___closed__64 = (const lean_object*)&l_NsExport_softNames___closed__64_value;
static const lean_ctor_object l_NsExport_softNames___closed__65_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__64_value),((lean_object*)&l_NsExport_softNames___closed__59_value)}};
static const lean_object* l_NsExport_softNames___closed__65 = (const lean_object*)&l_NsExport_softNames___closed__65_value;
static const lean_ctor_object l_NsExport_softNames___closed__66_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__63_value),((lean_object*)&l_NsExport_softNames___closed__65_value)}};
static const lean_object* l_NsExport_softNames___closed__66 = (const lean_object*)&l_NsExport_softNames___closed__66_value;
static const lean_ctor_object l_NsExport_softNames___closed__67_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__62_value),((lean_object*)&l_NsExport_softNames___closed__66_value)}};
static const lean_object* l_NsExport_softNames___closed__67 = (const lean_object*)&l_NsExport_softNames___closed__67_value;
static const lean_ctor_object l_NsExport_softNames___closed__68_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__61_value),((lean_object*)&l_NsExport_softNames___closed__67_value)}};
static const lean_object* l_NsExport_softNames___closed__68 = (const lean_object*)&l_NsExport_softNames___closed__68_value;
static const lean_ctor_object l_NsExport_softNames___closed__69_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__60_value),((lean_object*)&l_NsExport_softNames___closed__68_value)}};
static const lean_object* l_NsExport_softNames___closed__69 = (const lean_object*)&l_NsExport_softNames___closed__69_value;
static const lean_string_object l_NsExport_softNames___closed__70_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "eq_def"};
static const lean_object* l_NsExport_softNames___closed__70 = (const lean_object*)&l_NsExport_softNames___closed__70_value;
static const lean_string_object l_NsExport_softNames___closed__71_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "eq_unfold"};
static const lean_object* l_NsExport_softNames___closed__71 = (const lean_object*)&l_NsExport_softNames___closed__71_value;
static const lean_string_object l_NsExport_softNames___closed__72_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "congr_simp"};
static const lean_object* l_NsExport_softNames___closed__72 = (const lean_object*)&l_NsExport_softNames___closed__72_value;
static const lean_string_object l_NsExport_softNames___closed__73_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "sizeOf_spec"};
static const lean_object* l_NsExport_softNames___closed__73 = (const lean_object*)&l_NsExport_softNames___closed__73_value;
static const lean_string_object l_NsExport_softNames___closed__74_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "injEq"};
static const lean_object* l_NsExport_softNames___closed__74 = (const lean_object*)&l_NsExport_softNames___closed__74_value;
static const lean_ctor_object l_NsExport_softNames___closed__75_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__74_value),((lean_object*)&l_NsExport_softNames___closed__69_value)}};
static const lean_object* l_NsExport_softNames___closed__75 = (const lean_object*)&l_NsExport_softNames___closed__75_value;
static const lean_ctor_object l_NsExport_softNames___closed__76_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__73_value),((lean_object*)&l_NsExport_softNames___closed__75_value)}};
static const lean_object* l_NsExport_softNames___closed__76 = (const lean_object*)&l_NsExport_softNames___closed__76_value;
static const lean_ctor_object l_NsExport_softNames___closed__77_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__72_value),((lean_object*)&l_NsExport_softNames___closed__76_value)}};
static const lean_object* l_NsExport_softNames___closed__77 = (const lean_object*)&l_NsExport_softNames___closed__77_value;
static const lean_ctor_object l_NsExport_softNames___closed__78_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__71_value),((lean_object*)&l_NsExport_softNames___closed__77_value)}};
static const lean_object* l_NsExport_softNames___closed__78 = (const lean_object*)&l_NsExport_softNames___closed__78_value;
static const lean_ctor_object l_NsExport_softNames___closed__79_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_softNames___closed__70_value),((lean_object*)&l_NsExport_softNames___closed__78_value)}};
static const lean_object* l_NsExport_softNames___closed__79 = (const lean_object*)&l_NsExport_softNames___closed__79_value;
LEAN_EXPORT const lean_object* l_NsExport_softNames = (const lean_object*)&l_NsExport_softNames___closed__79_value;
static const lean_string_object l_NsExport_isEqNum___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "eq_"};
static const lean_object* l_NsExport_isEqNum___closed__0 = (const lean_object*)&l_NsExport_isEqNum___closed__0_value;
static lean_once_cell_t l_NsExport_isEqNum___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_NsExport_isEqNum___closed__1;
LEAN_EXPORT uint8_t l_NsExport_isEqNum(lean_object*);
LEAN_EXPORT lean_object* l_NsExport_isEqNum___boxed(lean_object*);
static const lean_string_object l_NsExport_droppedTypeHeads___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "Lean"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__0 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "ParserDescr"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__1 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__1_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__2_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__2_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__1_value),LEAN_SCALAR_PTR_LITERAL(92, 191, 134, 190, 206, 60, 55, 123)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__2 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__2_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "TrailingParserDescr"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__3 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__3_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__4_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__4_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__3_value),LEAN_SCALAR_PTR_LITERAL(73, 30, 7, 95, 84, 115, 124, 250)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__4 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__4_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "Macro"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__5 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__5_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__6_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__6_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__5_value),LEAN_SCALAR_PTR_LITERAL(168, 205, 218, 0, 241, 122, 66, 251)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__6 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__6_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "PrettyPrinter"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__7 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__7_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "Unexpander"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__8 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__8_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__9_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__9_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__9_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__7_value),LEAN_SCALAR_PTR_LITERAL(120, 167, 117, 148, 131, 202, 42, 4)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__9_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__8_value),LEAN_SCALAR_PTR_LITERAL(127, 37, 73, 100, 13, 145, 76, 255)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__9 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__9_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "Elab"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__10 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__10_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "Term"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__11 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__11_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "TermElab"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__12 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__12_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__13_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__13_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__13_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__10_value),LEAN_SCALAR_PTR_LITERAL(52, 247, 248, 201, 92, 23, 188, 159)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__13_value_aux_2 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__13_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__11_value),LEAN_SCALAR_PTR_LITERAL(252, 225, 247, 249, 114, 131, 135, 109)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__13_value_aux_2),((lean_object*)&l_NsExport_droppedTypeHeads___closed__12_value),LEAN_SCALAR_PTR_LITERAL(118, 153, 242, 23, 221, 73, 237, 6)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__13 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__13_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "Tactic"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__14 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__14_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__15_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__15_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__15_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__10_value),LEAN_SCALAR_PTR_LITERAL(52, 247, 248, 201, 92, 23, 188, 159)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__15_value_aux_2 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__15_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__14_value),LEAN_SCALAR_PTR_LITERAL(161, 230, 229, 85, 182, 144, 182, 176)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__15_value_aux_2),((lean_object*)&l_NsExport_droppedTypeHeads___closed__14_value),LEAN_SCALAR_PTR_LITERAL(232, 13, 253, 238, 247, 232, 20, 149)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__15 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__15_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "Command"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__16 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__16_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "CommandElab"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__17 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__17_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__18_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__18_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__18_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__10_value),LEAN_SCALAR_PTR_LITERAL(52, 247, 248, 201, 92, 23, 188, 159)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__18_value_aux_2 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__18_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__16_value),LEAN_SCALAR_PTR_LITERAL(177, 181, 244, 12, 1, 14, 170, 235)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__18_value_aux_2),((lean_object*)&l_NsExport_droppedTypeHeads___closed__17_value),LEAN_SCALAR_PTR_LITERAL(211, 81, 86, 187, 1, 234, 42, 9)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__18 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__18_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "Delaborator"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__19 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__19_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "Delab"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__20 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__20_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__21_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__21_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__21_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__7_value),LEAN_SCALAR_PTR_LITERAL(120, 167, 117, 148, 131, 202, 42, 4)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__21_value_aux_2 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__21_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__19_value),LEAN_SCALAR_PTR_LITERAL(79, 126, 247, 124, 241, 28, 11, 244)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__21_value_aux_2),((lean_object*)&l_NsExport_droppedTypeHeads___closed__20_value),LEAN_SCALAR_PTR_LITERAL(98, 145, 52, 44, 66, 160, 163, 69)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__21 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__21_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "Parser"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__22 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__22_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__23_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__23_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__23_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__22_value),LEAN_SCALAR_PTR_LITERAL(103, 136, 125, 166, 167, 98, 71, 111)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__23_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__22_value),LEAN_SCALAR_PTR_LITERAL(114, 164, 180, 82, 232, 106, 164, 24)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__23 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__23_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__24_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "TrailingParser"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__24 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__24_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__25_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__25_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__25_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__22_value),LEAN_SCALAR_PTR_LITERAL(103, 136, 125, 166, 167, 98, 71, 111)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__25_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__25_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__24_value),LEAN_SCALAR_PTR_LITERAL(232, 137, 139, 135, 36, 12, 238, 116)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__25 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__25_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "Formatter"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__26 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__26_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__27_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__27_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__27_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__7_value),LEAN_SCALAR_PTR_LITERAL(120, 167, 117, 148, 131, 202, 42, 4)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__27_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__26_value),LEAN_SCALAR_PTR_LITERAL(243, 65, 136, 208, 75, 168, 22, 8)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__27 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__27_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__28_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "Parenthesizer"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__28 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__28_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__29_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__29_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__29_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__7_value),LEAN_SCALAR_PTR_LITERAL(120, 167, 117, 148, 131, 202, 42, 4)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__29_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__29_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__28_value),LEAN_SCALAR_PTR_LITERAL(250, 80, 206, 144, 206, 86, 123, 88)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__29 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__29_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__30_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "Meta"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__30 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__30_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__31_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "Simp"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__31 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__31_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__32_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "Simproc"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__32 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__32_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__33_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__33_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__33_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__30_value),LEAN_SCALAR_PTR_LITERAL(194, 50, 106, 158, 41, 60, 103, 214)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__33_value_aux_2 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__33_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__31_value),LEAN_SCALAR_PTR_LITERAL(54, 38, 229, 237, 143, 62, 212, 6)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__33_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__33_value_aux_2),((lean_object*)&l_NsExport_droppedTypeHeads___closed__32_value),LEAN_SCALAR_PTR_LITERAL(18, 160, 179, 254, 130, 82, 156, 255)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__33 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__33_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__34_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "DSimproc"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__34 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__34_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__35_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__35_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__35_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__30_value),LEAN_SCALAR_PTR_LITERAL(194, 50, 106, 158, 41, 60, 103, 214)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__35_value_aux_2 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__35_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__31_value),LEAN_SCALAR_PTR_LITERAL(54, 38, 229, 237, 143, 62, 212, 6)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__35_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__35_value_aux_2),((lean_object*)&l_NsExport_droppedTypeHeads___closed__34_value),LEAN_SCALAR_PTR_LITERAL(119, 227, 62, 233, 71, 149, 243, 160)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__35 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__35_value;
static const lean_string_object l_NsExport_droppedTypeHeads___closed__36_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "Category"};
static const lean_object* l_NsExport_droppedTypeHeads___closed__36 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__36_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__37_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_droppedTypeHeads___closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 193, 83, 126, 233, 67, 208, 165)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__37_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__37_value_aux_0),((lean_object*)&l_NsExport_droppedTypeHeads___closed__22_value),LEAN_SCALAR_PTR_LITERAL(103, 136, 125, 166, 167, 98, 71, 111)}};
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__37_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__37_value_aux_1),((lean_object*)&l_NsExport_droppedTypeHeads___closed__36_value),LEAN_SCALAR_PTR_LITERAL(36, 45, 52, 71, 90, 26, 52, 161)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__37 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__37_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__38_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__37_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__38 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__38_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__39_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__35_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__38_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__39 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__39_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__40_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__33_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__39_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__40 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__40_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__41_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__29_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__40_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__41 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__41_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__42_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__27_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__41_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__42 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__42_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__43_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__25_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__42_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__43 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__43_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__44_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__23_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__43_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__44 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__44_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__45_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__21_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__44_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__45 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__45_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__46_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__18_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__45_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__46 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__46_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__47_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__15_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__46_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__47 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__47_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__48_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__13_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__47_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__48 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__48_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__49_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__9_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__48_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__49 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__49_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__50_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__6_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__49_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__50 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__50_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__51_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__4_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__50_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__51 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__51_value;
static const lean_ctor_object l_NsExport_droppedTypeHeads___closed__52_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_NsExport_droppedTypeHeads___closed__2_value),((lean_object*)&l_NsExport_droppedTypeHeads___closed__51_value)}};
static const lean_object* l_NsExport_droppedTypeHeads___closed__52 = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__52_value;
LEAN_EXPORT const lean_object* l_NsExport_droppedTypeHeads = (const lean_object*)&l_NsExport_droppedTypeHeads___closed__52_value;
LEAN_EXPORT lean_object* l_List_findIdx_go___at___00List_idxOf___at___00NsExport_hashLevel_spec__0_spec__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_findIdx_go___at___00List_idxOf___at___00NsExport_hashLevel_spec__0_spec__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_idxOf___at___00NsExport_hashLevel_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_idxOf___at___00NsExport_hashLevel_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint64_t l_NsExport_hashLevel(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_hashLevel___boxed(lean_object*, lean_object*);
static const lean_ctor_object l_NsExport_instInhabitedInfo_default___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 8, .m_other = 1, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* l_NsExport_instInhabitedInfo_default___closed__0 = (const lean_object*)&l_NsExport_instInhabitedInfo_default___closed__0_value;
LEAN_EXPORT const lean_object* l_NsExport_instInhabitedInfo_default = (const lean_object*)&l_NsExport_instInhabitedInfo_default___closed__0_value;
LEAN_EXPORT const lean_object* l_NsExport_instInhabitedInfo = (const lean_object*)&l_NsExport_instInhabitedInfo_default___closed__0_value;
LEAN_EXPORT uint64_t l_List_foldl___at___00NsExport_analyze_spec__0(lean_object*, uint64_t, lean_object*);
LEAN_EXPORT lean_object* l_List_foldl___at___00NsExport_analyze_spec__0___boxed(lean_object*, lean_object*, lean_object*);
static const lean_ctor_object l_NsExport_analyze___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 8, .m_other = 1, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(47, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* l_NsExport_analyze___closed__0 = (const lean_object*)&l_NsExport_analyze___closed__0_value;
LEAN_EXPORT lean_object* l_NsExport_analyze(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_analyze___boxed(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l_NsExport_sizes___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_NsExport_sizes___closed__0;
static lean_once_cell_t l_NsExport_sizes___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_NsExport_sizes___closed__1;
LEAN_EXPORT lean_object* l_NsExport_sizes(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_sizes___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_valueOf_x3f(lean_object*);
static const lean_string_object l_NsExport_hexOf___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 1, .m_capacity = 1, .m_length = 0, .m_data = ""};
static const lean_object* l_NsExport_hexOf___closed__0 = (const lean_object*)&l_NsExport_hexOf___closed__0_value;
LEAN_EXPORT lean_object* l_NsExport_hexOf(uint64_t);
LEAN_EXPORT lean_object* l_NsExport_hexOf___boxed(lean_object*);
LEAN_EXPORT lean_object* l_NsExport_moduleOf(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_moduleOf___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_resolveRoot(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_resolveRoot___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t l_Option_instBEq_beq___at___00NsExport_resolveDeps_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Option_instBEq_beq___at___00NsExport_resolveDeps_spec__0___boxed(lean_object*, lean_object*);
static const lean_ctor_object l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(5) << 1) | 1))}};
static const lean_object* l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg___closed__0 = (const lean_object*)&l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg___closed__0_value;
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l_NsExport_resolveDeps___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_NsExport_resolveDeps___closed__0;
static lean_once_cell_t l_NsExport_resolveDeps___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_NsExport_resolveDeps___closed__1;
LEAN_EXPORT lean_object* l_NsExport_resolveDeps(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_sortedNames_spec__0(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_sortedNames_spec__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_foldlM___at___00NsExport_sortedNames_spec__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_sortedNames_spec__2(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_sortedNames_spec__2___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_sortedNames(lean_object*);
LEAN_EXPORT lean_object* l_NsExport_sortedNames___boxed(lean_object*);
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_main___lam__0();
LEAN_EXPORT lean_object* l_NsExport_main___lam__0___boxed(lean_object*);
LEAN_EXPORT uint8_t l_NsExport_main___lam__1(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_main___lam__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_panic___at___00Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11_spec__13(lean_object*);
static const lean_string_object l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 43, .m_capacity = 43, .m_length = 42, .m_data = "Std.Data.DHashMap.Internal.AssocList.Basic"};
static const lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__0 = (const lean_object*)&l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__0_value;
static const lean_string_object l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 37, .m_capacity = 37, .m_length = 36, .m_data = "Std.DHashMap.Internal.AssocList.get!"};
static const lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__1 = (const lean_object*)&l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__1_value;
static const lean_string_object l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 33, .m_capacity = 33, .m_length = 32, .m_data = "key is not present in hash table"};
static const lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__2 = (const lean_object*)&l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__2_value;
static lean_once_cell_t l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__3;
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9___boxed(lean_object*, lean_object*);
static const lean_array_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___closed__0 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___closed__0_value;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13(lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__0(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00__private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2_spec__2(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00__private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2_spec__2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0(uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__1;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "_uniq"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__4 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__4_value;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__4_value),LEAN_SCALAR_PTR_LITERAL(237, 141, 162, 170, 202, 74, 55, 55)}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__5 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__5_value;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0(lean_object*, lean_object*, lean_object*, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, uint8_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "<export>"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "format"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__1 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__1_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "width"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__2 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__2_value;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__3_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__1_value),LEAN_SCALAR_PTR_LITERAL(41, 165, 100, 47, 160, 41, 84, 0)}};
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__3_value_aux_0),((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__2_value),LEAN_SCALAR_PTR_LITERAL(226, 244, 45, 141, 245, 85, 231, 30)}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__3 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__3_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "proof_"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__6 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__6_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "match_"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__8 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__8_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "_"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__10 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__10_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15(lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11(lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__0;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__2;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4;
static const lean_array_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__5 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__5_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__6;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__7;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__8;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__5_value),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11_value;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__12 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__12_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "\n| "};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__14 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__14_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = " : "};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__15 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__15_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21(lean_object*, lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16(lean_object*, lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__4___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__15(lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__15___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__14(lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__14___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__2(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__2___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_mapTR_loop___at___00NsExport_main_spec__4(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_foldrM___at___00NsExport_main_spec__7(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_foldrM___at___00NsExport_main_spec__7___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00NsExport_main_spec__8(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00NsExport_main_spec__8___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Std_Data_DHashMap_Internal_AssocList_Basic_0__Std_DHashMap_Internal_AssocList_forInStep_go___at___00NsExport_main_spec__5(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Std_Data_DHashMap_Internal_AssocList_Basic_0__Std_DHashMap_Internal_AssocList_forInStep_go___at___00NsExport_main_spec__5___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__6(lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__6___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___closed__0;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(lean_object*, lean_object*, lean_object*, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "] "};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__0 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__0_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = " written, "};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__1 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__1_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = " ms"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__2 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__2_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "auxProofSize"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__3 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__3_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "numAux"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__4 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__4_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "numCtors"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__5 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__5_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "typeDeps"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__6 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__6_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "valueDeps"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__7 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__7_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "numExtType"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__8 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__8_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "numExtValue"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__9 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__9_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "extTypeByRoot"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__10 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__10_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "extValueByRoot"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__11 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__11_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "typeIsProp"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__12 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__12_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "statementHash"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__13 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__13_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "line"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__14 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__14_value;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__14_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__15 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__15_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "endLine"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__16 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__16_value;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__16_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__17 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__17_value;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__17_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__18 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__18_value;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__15_value),((lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__18_value)}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__19 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__19_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "statement"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__20 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__20_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "statementChars"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__21 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__21_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 19, .m_capacity = 19, .m_length = 18, .m_data = "statementTruncated"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__22 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__22_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "ppOk"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__23 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__23_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__24_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "statementSize"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__24 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__24_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__25_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 17, .m_capacity = 17, .m_length = 16, .m_data = "statementDagSize"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__25 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__25_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "proofSize"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__26 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__26_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 18, .m_capacity = 18, .m_length = 17, .m_data = "proofTreeSizeLog2"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__27 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__27_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__28_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__28;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__30_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "name"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__30 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__30_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__31_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "userName"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__31 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__31_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__32_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "module"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__32 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__32_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__33_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "kind"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__33 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__33_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__34_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "isClass"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__34 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__34_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__35_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "instanceAttr"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__35 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__35_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__36_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "isPrivate"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__36 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__36_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__37_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "hasDocstring"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__37 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__37_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__38_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "instance"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__38 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__38_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__39_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "axiom"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__39 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__39_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__40_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "theorem"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__40 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__40_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__41_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "opaque"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__41 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__41_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__42_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "def"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__42 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__42_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__43_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "inductive"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__43 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__43_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__44_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "structure"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__44 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__44_value;
static const lean_string_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__45_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "other"};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__45 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__45_value;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1;
static const lean_ctor_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__2 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__2_value;
static lean_once_cell_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3;
static const lean_array_object l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__4 = (const lean_object*)&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__4_value;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13(lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10(lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__23(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__23___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__1(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__1___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__19(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__19___boxed(lean_object*, lean_object*, lean_object*);
static const lean_string_object l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "collectAxioms failed"};
static const lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__0 = (const lean_object*)&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__0_value;
static const lean_ctor_object l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__0_value)}};
static const lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__1 = (const lean_object*)&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__1_value;
static const lean_string_object l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 25, .m_capacity = 25, .m_length = 24, .m_data = "not found in environment"};
static const lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__2 = (const lean_object*)&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__2_value;
static const lean_ctor_object l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__2_value)}};
static const lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__3 = (const lean_object*)&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__3_value;
static const lean_ctor_object l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__4 = (const lean_object*)&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__4_value;
static lean_once_cell_t l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5;
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00__private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21_spec__29(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00__private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21_spec__29___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_string_object l_NsExport_main___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 80, .m_capacity = 80, .m_length = 79, .m_data = "usage: export modules.txt out.jsonl axioms.json meta.json shard nshards mains.."};
static const lean_object* l_NsExport_main___closed__0 = (const lean_object*)&l_NsExport_main___closed__0_value;
static const lean_ctor_object l_NsExport_main___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 18}, .m_objs = {((lean_object*)&l_NsExport_main___closed__0_value)}};
static const lean_object* l_NsExport_main___closed__1 = (const lean_object*)&l_NsExport_main___closed__1_value;
static const lean_string_object l_NsExport_main___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "lean"};
static const lean_object* l_NsExport_main___closed__2 = (const lean_object*)&l_NsExport_main___closed__2_value;
static const lean_string_object l_NsExport_main___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "rootModulesImported"};
static const lean_object* l_NsExport_main___closed__3 = (const lean_object*)&l_NsExport_main___closed__3_value;
static const lean_string_object l_NsExport_main___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "modulesTotal"};
static const lean_object* l_NsExport_main___closed__4 = (const lean_object*)&l_NsExport_main___closed__4_value;
static const lean_string_object l_NsExport_main___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "projectModules"};
static const lean_object* l_NsExport_main___closed__5 = (const lean_object*)&l_NsExport_main___closed__5_value;
static const lean_string_object l_NsExport_main___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 24, .m_capacity = 24, .m_length = 23, .m_data = "projectConstantsInclAux"};
static const lean_object* l_NsExport_main___closed__6 = (const lean_object*)&l_NsExport_main___closed__6_value;
static const lean_string_object l_NsExport_main___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "primary"};
static const lean_object* l_NsExport_main___closed__7 = (const lean_object*)&l_NsExport_main___closed__7_value;
static const lean_string_object l_NsExport_main___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "bodyAux"};
static const lean_object* l_NsExport_main___closed__8 = (const lean_object*)&l_NsExport_main___closed__8_value;
static const lean_string_object l_NsExport_main___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "ctor"};
static const lean_object* l_NsExport_main___closed__9 = (const lean_object*)&l_NsExport_main___closed__9_value;
static const lean_string_object l_NsExport_main___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "derivedAux"};
static const lean_object* l_NsExport_main___closed__10 = (const lean_object*)&l_NsExport_main___closed__10_value;
static const lean_string_object l_NsExport_main___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "dropped"};
static const lean_object* l_NsExport_main___closed__11 = (const lean_object*)&l_NsExport_main___closed__11_value;
static const lean_string_object l_NsExport_main___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "externalAux"};
static const lean_object* l_NsExport_main___closed__12 = (const lean_object*)&l_NsExport_main___closed__12_value;
static const lean_string_object l_NsExport_main___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "orphan"};
static const lean_object* l_NsExport_main___closed__13 = (const lean_object*)&l_NsExport_main___closed__13_value;
static const lean_string_object l_NsExport_main___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "orphanSample"};
static const lean_object* l_NsExport_main___closed__14 = (const lean_object*)&l_NsExport_main___closed__14_value;
static const lean_string_object l_NsExport_main___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "importMs"};
static const lean_object* l_NsExport_main___closed__15 = (const lean_object*)&l_NsExport_main___closed__15_value;
static const lean_string_object l_NsExport_main___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "] project constants (incl. auxiliaries): "};
static const lean_object* l_NsExport_main___closed__16 = (const lean_object*)&l_NsExport_main___closed__16_value;
static const lean_array_object l_NsExport_main___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l_NsExport_main___closed__17 = (const lean_object*)&l_NsExport_main___closed__17_value;
static const lean_ctor_object l_NsExport_main___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__17_value)}};
static const lean_object* l_NsExport_main___closed__18 = (const lean_object*)&l_NsExport_main___closed__18_value;
static const lean_ctor_object l_NsExport_main___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__18_value)}};
static const lean_object* l_NsExport_main___closed__19 = (const lean_object*)&l_NsExport_main___closed__19_value;
static const lean_ctor_object l_NsExport_main___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__19_value)}};
static const lean_object* l_NsExport_main___closed__20 = (const lean_object*)&l_NsExport_main___closed__20_value;
static const lean_ctor_object l_NsExport_main___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__20_value)}};
static const lean_object* l_NsExport_main___closed__21 = (const lean_object*)&l_NsExport_main___closed__21_value;
static const lean_ctor_object l_NsExport_main___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__21_value)}};
static const lean_object* l_NsExport_main___closed__22 = (const lean_object*)&l_NsExport_main___closed__22_value;
static const lean_ctor_object l_NsExport_main___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__22_value)}};
static const lean_object* l_NsExport_main___closed__23 = (const lean_object*)&l_NsExport_main___closed__23_value;
static const lean_ctor_object l_NsExport_main___closed__24_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__23_value)}};
static const lean_object* l_NsExport_main___closed__24 = (const lean_object*)&l_NsExport_main___closed__24_value;
static lean_once_cell_t l_NsExport_main___closed__25_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_NsExport_main___closed__25;
static lean_once_cell_t l_NsExport_main___closed__26_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_NsExport_main___closed__26;
static const lean_string_object l_NsExport_main___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "] primary "};
static const lean_object* l_NsExport_main___closed__27 = (const lean_object*)&l_NsExport_main___closed__27_value;
static const lean_string_object l_NsExport_main___closed__28_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = " body "};
static const lean_object* l_NsExport_main___closed__28 = (const lean_object*)&l_NsExport_main___closed__28_value;
static const lean_string_object l_NsExport_main___closed__29_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = " ctor "};
static const lean_object* l_NsExport_main___closed__29 = (const lean_object*)&l_NsExport_main___closed__29_value;
static const lean_string_object l_NsExport_main___closed__30_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = " derived "};
static const lean_object* l_NsExport_main___closed__30 = (const lean_object*)&l_NsExport_main___closed__30_value;
static const lean_string_object l_NsExport_main___closed__31_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = " dropped "};
static const lean_object* l_NsExport_main___closed__31 = (const lean_object*)&l_NsExport_main___closed__31_value;
static const lean_string_object l_NsExport_main___closed__32_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = " external "};
static const lean_object* l_NsExport_main___closed__32 = (const lean_object*)&l_NsExport_main___closed__32_value;
static const lean_string_object l_NsExport_main___closed__33_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = " orphan "};
static const lean_object* l_NsExport_main___closed__33 = (const lean_object*)&l_NsExport_main___closed__33_value;
static const lean_ctor_object l_NsExport_main___closed__34_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l_NsExport_main___closed__34 = (const lean_object*)&l_NsExport_main___closed__34_value;
static const lean_ctor_object l_NsExport_main___closed__35_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_NsExport_main___closed__34_value)}};
static const lean_object* l_NsExport_main___closed__35 = (const lean_object*)&l_NsExport_main___closed__35_value;
static const lean_string_object l_NsExport_main___closed__36_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "] wrote "};
static const lean_object* l_NsExport_main___closed__36 = (const lean_object*)&l_NsExport_main___closed__36_value;
static const lean_string_object l_NsExport_main___closed__37_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 23, .m_capacity = 23, .m_length = 22, .m_data = " declarations, ppFail "};
static const lean_object* l_NsExport_main___closed__37 = (const lean_object*)&l_NsExport_main___closed__37_value;
static const lean_string_object l_NsExport_main___closed__38_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = ", total "};
static const lean_object* l_NsExport_main___closed__38 = (const lean_object*)&l_NsExport_main___closed__38_value;
static const lean_array_object l_NsExport_main___closed__39_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l_NsExport_main___closed__39 = (const lean_object*)&l_NsExport_main___closed__39_value;
static const lean_string_object l_NsExport_main___closed__40_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "[shard "};
static const lean_object* l_NsExport_main___closed__40 = (const lean_object*)&l_NsExport_main___closed__40_value;
static const lean_string_object l_NsExport_main___closed__41_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 12, .m_capacity = 12, .m_length = 11, .m_data = "] imported "};
static const lean_object* l_NsExport_main___closed__41 = (const lean_object*)&l_NsExport_main___closed__41_value;
static const lean_string_object l_NsExport_main___closed__42_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 18, .m_capacity = 18, .m_length = 17, .m_data = " root modules in "};
static const lean_object* l_NsExport_main___closed__42 = (const lean_object*)&l_NsExport_main___closed__42_value;
static const lean_string_object l_NsExport_main___closed__43_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = " ms; "};
static const lean_object* l_NsExport_main___closed__43 = (const lean_object*)&l_NsExport_main___closed__43_value;
static const lean_string_object l_NsExport_main___closed__44_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = " modules total"};
static const lean_object* l_NsExport_main___closed__44 = (const lean_object*)&l_NsExport_main___closed__44_value;
LEAN_EXPORT lean_object* l_NsExport_main___boxed__const__1;
LEAN_EXPORT lean_object* l_NsExport_main(lean_object*);
LEAN_EXPORT lean_object* l_NsExport_main___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* _lean_main(lean_object*);
LEAN_EXPORT lean_object* l_main___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorIdx(lean_object* v_x_20_){
_start:
{
switch(lean_obj_tag(v_x_20_))
{
case 0:
{
lean_object* v___x_21_; 
v___x_21_ = lean_unsigned_to_nat(0u);
return v___x_21_;
}
case 1:
{
lean_object* v___x_22_; 
v___x_22_ = lean_unsigned_to_nat(1u);
return v___x_22_;
}
case 2:
{
lean_object* v___x_23_; 
v___x_23_ = lean_unsigned_to_nat(2u);
return v___x_23_;
}
case 3:
{
lean_object* v___x_24_; 
v___x_24_ = lean_unsigned_to_nat(3u);
return v___x_24_;
}
case 4:
{
lean_object* v___x_25_; 
v___x_25_ = lean_unsigned_to_nat(4u);
return v___x_25_;
}
case 5:
{
lean_object* v___x_26_; 
v___x_26_ = lean_unsigned_to_nat(5u);
return v___x_26_;
}
default: 
{
lean_object* v___x_27_; 
v___x_27_ = lean_unsigned_to_nat(6u);
return v___x_27_;
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorIdx___boxed(lean_object* v_x_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = l_NsExport_Cls_ctorIdx(v_x_28_);
lean_dec(v_x_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorElim___redArg(lean_object* v_t_30_, lean_object* v_k_31_){
_start:
{
switch(lean_obj_tag(v_t_30_))
{
case 1:
{
lean_object* v_parent_32_; lean_object* v___x_33_; 
v_parent_32_ = lean_ctor_get(v_t_30_, 0);
lean_inc(v_parent_32_);
lean_dec_ref_known(v_t_30_, 1);
v___x_33_ = lean_apply_1(v_k_31_, v_parent_32_);
return v___x_33_;
}
case 2:
{
lean_object* v_parent_34_; lean_object* v___x_35_; 
v_parent_34_ = lean_ctor_get(v_t_30_, 0);
lean_inc(v_parent_34_);
lean_dec_ref_known(v_t_30_, 1);
v___x_35_ = lean_apply_1(v_k_31_, v_parent_34_);
return v___x_35_;
}
case 3:
{
lean_object* v_parent_36_; lean_object* v___x_37_; 
v_parent_36_ = lean_ctor_get(v_t_30_, 0);
lean_inc(v_parent_36_);
lean_dec_ref_known(v_t_30_, 1);
v___x_37_ = lean_apply_1(v_k_31_, v_parent_36_);
return v___x_37_;
}
default: 
{
lean_dec(v_t_30_);
return v_k_31_;
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorElim(lean_object* v_motive_38_, lean_object* v_ctorIdx_39_, lean_object* v_t_40_, lean_object* v_h_41_, lean_object* v_k_42_){
_start:
{
lean_object* v___x_43_; 
v___x_43_ = l_NsExport_Cls_ctorElim___redArg(v_t_40_, v_k_42_);
return v___x_43_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_ctorElim___boxed(lean_object* v_motive_44_, lean_object* v_ctorIdx_45_, lean_object* v_t_46_, lean_object* v_h_47_, lean_object* v_k_48_){
_start:
{
lean_object* v_res_49_; 
v_res_49_ = l_NsExport_Cls_ctorElim(v_motive_44_, v_ctorIdx_45_, v_t_46_, v_h_47_, v_k_48_);
lean_dec(v_ctorIdx_45_);
return v_res_49_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_primary_elim___redArg(lean_object* v_t_50_, lean_object* v_primary_51_){
_start:
{
lean_object* v___x_52_; 
v___x_52_ = l_NsExport_Cls_ctorElim___redArg(v_t_50_, v_primary_51_);
return v___x_52_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_primary_elim(lean_object* v_motive_53_, lean_object* v_t_54_, lean_object* v_h_55_, lean_object* v_primary_56_){
_start:
{
lean_object* v___x_57_; 
v___x_57_ = l_NsExport_Cls_ctorElim___redArg(v_t_54_, v_primary_56_);
return v___x_57_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_body_elim___redArg(lean_object* v_t_58_, lean_object* v_body_59_){
_start:
{
lean_object* v___x_60_; 
v___x_60_ = l_NsExport_Cls_ctorElim___redArg(v_t_58_, v_body_59_);
return v___x_60_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_body_elim(lean_object* v_motive_61_, lean_object* v_t_62_, lean_object* v_h_63_, lean_object* v_body_64_){
_start:
{
lean_object* v___x_65_; 
v___x_65_ = l_NsExport_Cls_ctorElim___redArg(v_t_62_, v_body_64_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_ctor_elim___redArg(lean_object* v_t_66_, lean_object* v_ctor_67_){
_start:
{
lean_object* v___x_68_; 
v___x_68_ = l_NsExport_Cls_ctorElim___redArg(v_t_66_, v_ctor_67_);
return v___x_68_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_ctor_elim(lean_object* v_motive_69_, lean_object* v_t_70_, lean_object* v_h_71_, lean_object* v_ctor_72_){
_start:
{
lean_object* v___x_73_; 
v___x_73_ = l_NsExport_Cls_ctorElim___redArg(v_t_70_, v_ctor_72_);
return v___x_73_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_derived_elim___redArg(lean_object* v_t_74_, lean_object* v_derived_75_){
_start:
{
lean_object* v___x_76_; 
v___x_76_ = l_NsExport_Cls_ctorElim___redArg(v_t_74_, v_derived_75_);
return v___x_76_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_derived_elim(lean_object* v_motive_77_, lean_object* v_t_78_, lean_object* v_h_79_, lean_object* v_derived_80_){
_start:
{
lean_object* v___x_81_; 
v___x_81_ = l_NsExport_Cls_ctorElim___redArg(v_t_78_, v_derived_80_);
return v___x_81_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_dropped_elim___redArg(lean_object* v_t_82_, lean_object* v_dropped_83_){
_start:
{
lean_object* v___x_84_; 
v___x_84_ = l_NsExport_Cls_ctorElim___redArg(v_t_82_, v_dropped_83_);
return v___x_84_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_dropped_elim(lean_object* v_motive_85_, lean_object* v_t_86_, lean_object* v_h_87_, lean_object* v_dropped_88_){
_start:
{
lean_object* v___x_89_; 
v___x_89_ = l_NsExport_Cls_ctorElim___redArg(v_t_86_, v_dropped_88_);
return v___x_89_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_external_elim___redArg(lean_object* v_t_90_, lean_object* v_external_91_){
_start:
{
lean_object* v___x_92_; 
v___x_92_ = l_NsExport_Cls_ctorElim___redArg(v_t_90_, v_external_91_);
return v___x_92_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_external_elim(lean_object* v_motive_93_, lean_object* v_t_94_, lean_object* v_h_95_, lean_object* v_external_96_){
_start:
{
lean_object* v___x_97_; 
v___x_97_ = l_NsExport_Cls_ctorElim___redArg(v_t_94_, v_external_96_);
return v___x_97_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_orphan_elim___redArg(lean_object* v_t_98_, lean_object* v_orphan_99_){
_start:
{
lean_object* v___x_100_; 
v___x_100_ = l_NsExport_Cls_ctorElim___redArg(v_t_98_, v_orphan_99_);
return v___x_100_;
}
}
LEAN_EXPORT lean_object* l_NsExport_Cls_orphan_elim(lean_object* v_motive_101_, lean_object* v_t_102_, lean_object* v_h_103_, lean_object* v_orphan_104_){
_start:
{
lean_object* v___x_105_; 
v___x_105_ = l_NsExport_Cls_ctorElim___redArg(v_t_102_, v_orphan_104_);
return v___x_105_;
}
}
static lean_object* _init_l_NsExport_instInhabitedCls_default(void){
_start:
{
lean_object* v___x_106_; 
v___x_106_ = lean_box(0);
return v___x_106_;
}
}
static lean_object* _init_l_NsExport_instInhabitedCls(void){
_start:
{
lean_object* v___x_107_; 
v___x_107_ = lean_box(0);
return v___x_107_;
}
}
LEAN_EXPORT uint8_t l_NsExport_instBEqCls_beq(lean_object* v_x_108_, lean_object* v_x_109_){
_start:
{
switch(lean_obj_tag(v_x_108_))
{
case 0:
{
if (lean_obj_tag(v_x_109_) == 0)
{
uint8_t v___x_110_; 
v___x_110_ = 1;
return v___x_110_;
}
else
{
uint8_t v___x_111_; 
v___x_111_ = 0;
return v___x_111_;
}
}
case 1:
{
if (lean_obj_tag(v_x_109_) == 1)
{
lean_object* v_parent_112_; lean_object* v_parent_113_; uint8_t v___x_114_; 
v_parent_112_ = lean_ctor_get(v_x_108_, 0);
v_parent_113_ = lean_ctor_get(v_x_109_, 0);
v___x_114_ = lean_name_eq(v_parent_112_, v_parent_113_);
return v___x_114_;
}
else
{
uint8_t v___x_115_; 
v___x_115_ = 0;
return v___x_115_;
}
}
case 2:
{
if (lean_obj_tag(v_x_109_) == 2)
{
lean_object* v_parent_116_; lean_object* v_parent_117_; uint8_t v___x_118_; 
v_parent_116_ = lean_ctor_get(v_x_108_, 0);
v_parent_117_ = lean_ctor_get(v_x_109_, 0);
v___x_118_ = lean_name_eq(v_parent_116_, v_parent_117_);
return v___x_118_;
}
else
{
uint8_t v___x_119_; 
v___x_119_ = 0;
return v___x_119_;
}
}
case 3:
{
if (lean_obj_tag(v_x_109_) == 3)
{
lean_object* v_parent_120_; lean_object* v_parent_121_; uint8_t v___x_122_; 
v_parent_120_ = lean_ctor_get(v_x_108_, 0);
v_parent_121_ = lean_ctor_get(v_x_109_, 0);
v___x_122_ = lean_name_eq(v_parent_120_, v_parent_121_);
return v___x_122_;
}
else
{
uint8_t v___x_123_; 
v___x_123_ = 0;
return v___x_123_;
}
}
case 4:
{
if (lean_obj_tag(v_x_109_) == 4)
{
uint8_t v___x_124_; 
v___x_124_ = 1;
return v___x_124_;
}
else
{
uint8_t v___x_125_; 
v___x_125_ = 0;
return v___x_125_;
}
}
case 5:
{
if (lean_obj_tag(v_x_109_) == 5)
{
uint8_t v___x_126_; 
v___x_126_ = 1;
return v___x_126_;
}
else
{
uint8_t v___x_127_; 
v___x_127_ = 0;
return v___x_127_;
}
}
default: 
{
if (lean_obj_tag(v_x_109_) == 6)
{
uint8_t v___x_128_; 
v___x_128_ = 1;
return v___x_128_;
}
else
{
uint8_t v___x_129_; 
v___x_129_ = 0;
return v___x_129_;
}
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_instBEqCls_beq___boxed(lean_object* v_x_130_, lean_object* v_x_131_){
_start:
{
uint8_t v_res_132_; lean_object* v_r_133_; 
v_res_132_ = l_NsExport_instBEqCls_beq(v_x_130_, v_x_131_);
lean_dec(v_x_131_);
lean_dec(v_x_130_);
v_r_133_ = lean_box(v_res_132_);
return v_r_133_;
}
}
static lean_object* _init_l_NsExport_isEqNum___closed__1(void){
_start:
{
lean_object* v___x_298_; lean_object* v___x_299_; 
v___x_298_ = ((lean_object*)(l_NsExport_isEqNum___closed__0));
v___x_299_ = lean_string_utf8_byte_size(v___x_298_);
return v___x_299_;
}
}
LEAN_EXPORT uint8_t l_NsExport_isEqNum(lean_object* v_s_300_){
_start:
{
lean_object* v___x_301_; lean_object* v___x_302_; lean_object* v___x_303_; uint8_t v___x_304_; 
v___x_301_ = ((lean_object*)(l_NsExport_isEqNum___closed__0));
v___x_302_ = lean_string_utf8_byte_size(v_s_300_);
v___x_303_ = lean_obj_once(&l_NsExport_isEqNum___closed__1, &l_NsExport_isEqNum___closed__1_once, _init_l_NsExport_isEqNum___closed__1);
v___x_304_ = lean_nat_dec_le(v___x_303_, v___x_302_);
if (v___x_304_ == 0)
{
lean_dec_ref(v_s_300_);
return v___x_304_;
}
else
{
lean_object* v___x_305_; uint8_t v___x_306_; 
v___x_305_ = lean_unsigned_to_nat(0u);
v___x_306_ = lean_string_memcmp(v_s_300_, v___x_301_, v___x_305_, v___x_305_, v___x_303_);
if (v___x_306_ == 0)
{
lean_dec_ref(v_s_300_);
return v___x_306_;
}
else
{
lean_object* v___x_307_; lean_object* v___x_308_; lean_object* v___x_309_; lean_object* v___x_310_; lean_object* v___x_311_; lean_object* v___x_312_; uint8_t v___x_313_; 
v___x_307_ = lean_unsigned_to_nat(3u);
lean_inc_ref_n(v_s_300_, 2);
v___x_308_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_308_, 0, v_s_300_);
lean_ctor_set(v___x_308_, 1, v___x_305_);
lean_ctor_set(v___x_308_, 2, v___x_302_);
v___x_309_ = l_String_Slice_Pos_nextn(v___x_308_, v___x_305_, v___x_307_);
lean_dec_ref_known(v___x_308_, 3);
lean_inc(v___x_309_);
v___x_310_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_310_, 0, v_s_300_);
lean_ctor_set(v___x_310_, 1, v___x_309_);
lean_ctor_set(v___x_310_, 2, v___x_302_);
v___x_311_ = l_String_Slice_Pos_skipWhile___at___00Std_Http_Header_ContentLength_parse_spec__0(v___x_310_, v___x_305_);
lean_dec_ref_known(v___x_310_, 3);
v___x_312_ = lean_nat_sub(v___x_302_, v___x_309_);
lean_dec(v___x_309_);
v___x_313_ = lean_nat_dec_eq(v___x_311_, v___x_312_);
lean_dec(v___x_312_);
lean_dec(v___x_311_);
if (v___x_313_ == 0)
{
lean_dec_ref(v_s_300_);
return v___x_313_;
}
else
{
lean_object* v___x_314_; uint8_t v___x_315_; 
v___x_314_ = lean_string_length(v_s_300_);
lean_dec_ref(v_s_300_);
v___x_315_ = lean_nat_dec_lt(v___x_307_, v___x_314_);
return v___x_315_;
}
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_isEqNum___boxed(lean_object* v_s_316_){
_start:
{
uint8_t v_res_317_; lean_object* v_r_318_; 
v_res_317_ = l_NsExport_isEqNum(v_s_316_);
v_r_318_ = lean_box(v_res_317_);
return v_r_318_;
}
}
LEAN_EXPORT lean_object* l_List_findIdx_go___at___00List_idxOf___at___00NsExport_hashLevel_spec__0_spec__0(lean_object* v_a_449_, lean_object* v_a_450_, lean_object* v_a_451_){
_start:
{
if (lean_obj_tag(v_a_450_) == 0)
{
return v_a_451_;
}
else
{
lean_object* v_head_452_; lean_object* v_tail_453_; uint8_t v___x_454_; 
v_head_452_ = lean_ctor_get(v_a_450_, 0);
v_tail_453_ = lean_ctor_get(v_a_450_, 1);
v___x_454_ = lean_name_eq(v_head_452_, v_a_449_);
if (v___x_454_ == 0)
{
lean_object* v___x_455_; lean_object* v___x_456_; 
v___x_455_ = lean_unsigned_to_nat(1u);
v___x_456_ = lean_nat_add(v_a_451_, v___x_455_);
lean_dec(v_a_451_);
v_a_450_ = v_tail_453_;
v_a_451_ = v___x_456_;
goto _start;
}
else
{
return v_a_451_;
}
}
}
}
LEAN_EXPORT lean_object* l_List_findIdx_go___at___00List_idxOf___at___00NsExport_hashLevel_spec__0_spec__0___boxed(lean_object* v_a_458_, lean_object* v_a_459_, lean_object* v_a_460_){
_start:
{
lean_object* v_res_461_; 
v_res_461_ = l_List_findIdx_go___at___00List_idxOf___at___00NsExport_hashLevel_spec__0_spec__0(v_a_458_, v_a_459_, v_a_460_);
lean_dec(v_a_459_);
lean_dec(v_a_458_);
return v_res_461_;
}
}
LEAN_EXPORT lean_object* l_List_idxOf___at___00NsExport_hashLevel_spec__0(lean_object* v_a_462_, lean_object* v_l_463_){
_start:
{
lean_object* v___x_464_; lean_object* v___x_465_; 
v___x_464_ = lean_unsigned_to_nat(0u);
v___x_465_ = l_List_findIdx_go___at___00List_idxOf___at___00NsExport_hashLevel_spec__0_spec__0(v_a_462_, v_l_463_, v___x_464_);
return v___x_465_;
}
}
LEAN_EXPORT lean_object* l_List_idxOf___at___00NsExport_hashLevel_spec__0___boxed(lean_object* v_a_466_, lean_object* v_l_467_){
_start:
{
lean_object* v_res_468_; 
v_res_468_ = l_List_idxOf___at___00NsExport_hashLevel_spec__0(v_a_466_, v_l_467_);
lean_dec(v_l_467_);
lean_dec(v_a_466_);
return v_res_468_;
}
}
LEAN_EXPORT uint64_t l_NsExport_hashLevel(lean_object* v_ps_469_, lean_object* v_x_470_){
_start:
{
switch(lean_obj_tag(v_x_470_))
{
case 0:
{
uint64_t v___x_471_; 
v___x_471_ = 11ULL;
return v___x_471_;
}
case 1:
{
lean_object* v_a_472_; uint64_t v___x_473_; uint64_t v___x_474_; uint64_t v___x_475_; 
v_a_472_ = lean_ctor_get(v_x_470_, 0);
v___x_473_ = 13ULL;
v___x_474_ = l_NsExport_hashLevel(v_ps_469_, v_a_472_);
v___x_475_ = lean_uint64_mix_hash(v___x_473_, v___x_474_);
return v___x_475_;
}
case 2:
{
lean_object* v_a_476_; lean_object* v_a_477_; uint64_t v___x_478_; uint64_t v___x_479_; uint64_t v___x_480_; uint64_t v___x_481_; uint64_t v___x_482_; 
v_a_476_ = lean_ctor_get(v_x_470_, 0);
v_a_477_ = lean_ctor_get(v_x_470_, 1);
v___x_478_ = 17ULL;
v___x_479_ = l_NsExport_hashLevel(v_ps_469_, v_a_476_);
v___x_480_ = l_NsExport_hashLevel(v_ps_469_, v_a_477_);
v___x_481_ = lean_uint64_mix_hash(v___x_479_, v___x_480_);
v___x_482_ = lean_uint64_mix_hash(v___x_478_, v___x_481_);
return v___x_482_;
}
case 3:
{
lean_object* v_a_483_; lean_object* v_a_484_; uint64_t v___x_485_; uint64_t v___x_486_; uint64_t v___x_487_; uint64_t v___x_488_; uint64_t v___x_489_; 
v_a_483_ = lean_ctor_get(v_x_470_, 0);
v_a_484_ = lean_ctor_get(v_x_470_, 1);
v___x_485_ = 19ULL;
v___x_486_ = l_NsExport_hashLevel(v_ps_469_, v_a_483_);
v___x_487_ = l_NsExport_hashLevel(v_ps_469_, v_a_484_);
v___x_488_ = lean_uint64_mix_hash(v___x_486_, v___x_487_);
v___x_489_ = lean_uint64_mix_hash(v___x_485_, v___x_488_);
return v___x_489_;
}
case 4:
{
lean_object* v_a_490_; uint64_t v___x_491_; lean_object* v___x_492_; uint64_t v___x_493_; uint64_t v___x_494_; 
v_a_490_ = lean_ctor_get(v_x_470_, 0);
v___x_491_ = 23ULL;
v___x_492_ = l_List_idxOf___at___00NsExport_hashLevel_spec__0(v_a_490_, v_ps_469_);
v___x_493_ = lean_uint64_of_nat(v___x_492_);
lean_dec(v___x_492_);
v___x_494_ = lean_uint64_mix_hash(v___x_491_, v___x_493_);
return v___x_494_;
}
default: 
{
uint64_t v___x_495_; 
v___x_495_ = 29ULL;
return v___x_495_;
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_hashLevel___boxed(lean_object* v_ps_496_, lean_object* v_x_497_){
_start:
{
uint64_t v_res_498_; lean_object* v_r_499_; 
v_res_498_ = l_NsExport_hashLevel(v_ps_496_, v_x_497_);
lean_dec(v_x_497_);
lean_dec(v_ps_496_);
v_r_499_ = lean_box_uint64(v_res_498_);
return v_r_499_;
}
}
LEAN_EXPORT uint64_t l_List_foldl___at___00NsExport_analyze_spec__0(lean_object* v_ps_505_, uint64_t v_x_506_, lean_object* v_x_507_){
_start:
{
if (lean_obj_tag(v_x_507_) == 0)
{
return v_x_506_;
}
else
{
lean_object* v_head_508_; lean_object* v_tail_509_; uint64_t v___x_510_; uint64_t v___x_511_; 
v_head_508_ = lean_ctor_get(v_x_507_, 0);
v_tail_509_ = lean_ctor_get(v_x_507_, 1);
v___x_510_ = l_NsExport_hashLevel(v_ps_505_, v_head_508_);
v___x_511_ = lean_uint64_mix_hash(v_x_506_, v___x_510_);
v_x_506_ = v___x_511_;
v_x_507_ = v_tail_509_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l_List_foldl___at___00NsExport_analyze_spec__0___boxed(lean_object* v_ps_513_, lean_object* v_x_514_, lean_object* v_x_515_){
_start:
{
uint64_t v_x_5137__boxed_516_; uint64_t v_res_517_; lean_object* v_r_518_; 
v_x_5137__boxed_516_ = lean_unbox_uint64(v_x_514_);
lean_dec_ref(v_x_514_);
v_res_517_ = l_List_foldl___at___00NsExport_analyze_spec__0(v_ps_513_, v_x_5137__boxed_516_, v_x_515_);
lean_dec(v_x_515_);
lean_dec(v_ps_513_);
v_r_518_ = lean_box_uint64(v_res_517_);
return v_r_518_;
}
}
LEAN_EXPORT lean_object* l_NsExport_analyze(lean_object* v_ps_522_, lean_object* v_e_523_, lean_object* v_a_524_){
_start:
{
lean_object* v_r_526_; lean_object* v___y_527_; 
if (lean_obj_tag(v_e_523_) == 10)
{
lean_object* v_expr_530_; 
v_expr_530_ = lean_ctor_get(v_e_523_, 1);
lean_inc_ref(v_expr_530_);
lean_dec_ref_known(v_e_523_, 2);
v_e_523_ = v_expr_530_;
goto _start;
}
else
{
lean_object* v___x_532_; 
v___x_532_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Meta_ExprDefEq_0__Lean_Meta_CheckAssignment_findCached_x3f_spec__0___redArg(v_a_524_, v_e_523_);
if (lean_obj_tag(v___x_532_) == 1)
{
lean_object* v_val_533_; lean_object* v___x_534_; 
lean_dec_ref(v_e_523_);
v_val_533_ = lean_ctor_get(v___x_532_, 0);
lean_inc(v_val_533_);
lean_dec_ref_known(v___x_532_, 1);
v___x_534_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_534_, 0, v_val_533_);
lean_ctor_set(v___x_534_, 1, v_a_524_);
return v___x_534_;
}
else
{
lean_dec(v___x_532_);
switch(lean_obj_tag(v_e_523_))
{
case 5:
{
lean_object* v_fn_535_; lean_object* v_arg_536_; lean_object* v___x_537_; lean_object* v_fst_538_; lean_object* v_snd_539_; lean_object* v___x_540_; lean_object* v_fst_541_; lean_object* v_snd_542_; lean_object* v_tree_543_; uint64_t v_h_544_; lean_object* v_tree_545_; uint64_t v_h_546_; lean_object* v___x_548_; uint8_t v_isShared_549_; uint8_t v_isSharedCheck_559_; 
v_fn_535_ = lean_ctor_get(v_e_523_, 0);
v_arg_536_ = lean_ctor_get(v_e_523_, 1);
lean_inc_ref(v_fn_535_);
v___x_537_ = l_NsExport_analyze(v_ps_522_, v_fn_535_, v_a_524_);
v_fst_538_ = lean_ctor_get(v___x_537_, 0);
lean_inc(v_fst_538_);
v_snd_539_ = lean_ctor_get(v___x_537_, 1);
lean_inc(v_snd_539_);
lean_dec_ref(v___x_537_);
lean_inc_ref(v_arg_536_);
v___x_540_ = l_NsExport_analyze(v_ps_522_, v_arg_536_, v_snd_539_);
v_fst_541_ = lean_ctor_get(v___x_540_, 0);
lean_inc(v_fst_541_);
v_snd_542_ = lean_ctor_get(v___x_540_, 1);
lean_inc(v_snd_542_);
lean_dec_ref(v___x_540_);
v_tree_543_ = lean_ctor_get(v_fst_538_, 0);
lean_inc(v_tree_543_);
v_h_544_ = lean_ctor_get_uint64(v_fst_538_, sizeof(void*)*1);
lean_dec(v_fst_538_);
v_tree_545_ = lean_ctor_get(v_fst_541_, 0);
v_h_546_ = lean_ctor_get_uint64(v_fst_541_, sizeof(void*)*1);
v_isSharedCheck_559_ = !lean_is_exclusive(v_fst_541_);
if (v_isSharedCheck_559_ == 0)
{
v___x_548_ = v_fst_541_;
v_isShared_549_ = v_isSharedCheck_559_;
goto v_resetjp_547_;
}
else
{
lean_inc(v_tree_545_);
lean_dec(v_fst_541_);
v___x_548_ = lean_box(0);
v_isShared_549_ = v_isSharedCheck_559_;
goto v_resetjp_547_;
}
v_resetjp_547_:
{
lean_object* v___x_550_; lean_object* v___x_551_; lean_object* v___x_552_; uint64_t v___x_553_; uint64_t v___x_554_; uint64_t v___x_555_; lean_object* v___x_557_; 
v___x_550_ = lean_nat_add(v_tree_543_, v_tree_545_);
lean_dec(v_tree_545_);
lean_dec(v_tree_543_);
v___x_551_ = lean_unsigned_to_nat(1u);
v___x_552_ = lean_nat_add(v___x_550_, v___x_551_);
lean_dec(v___x_550_);
v___x_553_ = 7ULL;
v___x_554_ = lean_uint64_mix_hash(v_h_544_, v_h_546_);
v___x_555_ = lean_uint64_mix_hash(v___x_553_, v___x_554_);
if (v_isShared_549_ == 0)
{
lean_ctor_set(v___x_548_, 0, v___x_552_);
v___x_557_ = v___x_548_;
goto v_reusejp_556_;
}
else
{
lean_object* v_reuseFailAlloc_558_; 
v_reuseFailAlloc_558_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v_reuseFailAlloc_558_, 0, v___x_552_);
v___x_557_ = v_reuseFailAlloc_558_;
goto v_reusejp_556_;
}
v_reusejp_556_:
{
lean_ctor_set_uint64(v___x_557_, sizeof(void*)*1, v___x_555_);
v_r_526_ = v___x_557_;
v___y_527_ = v_snd_542_;
goto v___jp_525_;
}
}
}
case 6:
{
lean_object* v_binderType_560_; lean_object* v_body_561_; lean_object* v___x_562_; lean_object* v_fst_563_; lean_object* v_snd_564_; lean_object* v___x_565_; lean_object* v_fst_566_; lean_object* v_snd_567_; lean_object* v_tree_568_; uint64_t v_h_569_; lean_object* v_tree_570_; uint64_t v_h_571_; lean_object* v___x_573_; uint8_t v_isShared_574_; uint8_t v_isSharedCheck_584_; 
v_binderType_560_ = lean_ctor_get(v_e_523_, 1);
v_body_561_ = lean_ctor_get(v_e_523_, 2);
lean_inc_ref(v_binderType_560_);
v___x_562_ = l_NsExport_analyze(v_ps_522_, v_binderType_560_, v_a_524_);
v_fst_563_ = lean_ctor_get(v___x_562_, 0);
lean_inc(v_fst_563_);
v_snd_564_ = lean_ctor_get(v___x_562_, 1);
lean_inc(v_snd_564_);
lean_dec_ref(v___x_562_);
lean_inc_ref(v_body_561_);
v___x_565_ = l_NsExport_analyze(v_ps_522_, v_body_561_, v_snd_564_);
v_fst_566_ = lean_ctor_get(v___x_565_, 0);
lean_inc(v_fst_566_);
v_snd_567_ = lean_ctor_get(v___x_565_, 1);
lean_inc(v_snd_567_);
lean_dec_ref(v___x_565_);
v_tree_568_ = lean_ctor_get(v_fst_563_, 0);
lean_inc(v_tree_568_);
v_h_569_ = lean_ctor_get_uint64(v_fst_563_, sizeof(void*)*1);
lean_dec(v_fst_563_);
v_tree_570_ = lean_ctor_get(v_fst_566_, 0);
v_h_571_ = lean_ctor_get_uint64(v_fst_566_, sizeof(void*)*1);
v_isSharedCheck_584_ = !lean_is_exclusive(v_fst_566_);
if (v_isSharedCheck_584_ == 0)
{
v___x_573_ = v_fst_566_;
v_isShared_574_ = v_isSharedCheck_584_;
goto v_resetjp_572_;
}
else
{
lean_inc(v_tree_570_);
lean_dec(v_fst_566_);
v___x_573_ = lean_box(0);
v_isShared_574_ = v_isSharedCheck_584_;
goto v_resetjp_572_;
}
v_resetjp_572_:
{
lean_object* v___x_575_; lean_object* v___x_576_; lean_object* v___x_577_; uint64_t v___x_578_; uint64_t v___x_579_; uint64_t v___x_580_; lean_object* v___x_582_; 
v___x_575_ = lean_nat_add(v_tree_568_, v_tree_570_);
lean_dec(v_tree_570_);
lean_dec(v_tree_568_);
v___x_576_ = lean_unsigned_to_nat(1u);
v___x_577_ = lean_nat_add(v___x_575_, v___x_576_);
lean_dec(v___x_575_);
v___x_578_ = 59ULL;
v___x_579_ = lean_uint64_mix_hash(v_h_569_, v_h_571_);
v___x_580_ = lean_uint64_mix_hash(v___x_578_, v___x_579_);
if (v_isShared_574_ == 0)
{
lean_ctor_set(v___x_573_, 0, v___x_577_);
v___x_582_ = v___x_573_;
goto v_reusejp_581_;
}
else
{
lean_object* v_reuseFailAlloc_583_; 
v_reuseFailAlloc_583_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v_reuseFailAlloc_583_, 0, v___x_577_);
v___x_582_ = v_reuseFailAlloc_583_;
goto v_reusejp_581_;
}
v_reusejp_581_:
{
lean_ctor_set_uint64(v___x_582_, sizeof(void*)*1, v___x_580_);
v_r_526_ = v___x_582_;
v___y_527_ = v_snd_567_;
goto v___jp_525_;
}
}
}
case 7:
{
lean_object* v_binderType_585_; lean_object* v_body_586_; lean_object* v___x_587_; lean_object* v_fst_588_; lean_object* v_snd_589_; lean_object* v___x_590_; lean_object* v_fst_591_; lean_object* v_snd_592_; lean_object* v_tree_593_; uint64_t v_h_594_; lean_object* v_tree_595_; uint64_t v_h_596_; lean_object* v___x_598_; uint8_t v_isShared_599_; uint8_t v_isSharedCheck_609_; 
v_binderType_585_ = lean_ctor_get(v_e_523_, 1);
v_body_586_ = lean_ctor_get(v_e_523_, 2);
lean_inc_ref(v_binderType_585_);
v___x_587_ = l_NsExport_analyze(v_ps_522_, v_binderType_585_, v_a_524_);
v_fst_588_ = lean_ctor_get(v___x_587_, 0);
lean_inc(v_fst_588_);
v_snd_589_ = lean_ctor_get(v___x_587_, 1);
lean_inc(v_snd_589_);
lean_dec_ref(v___x_587_);
lean_inc_ref(v_body_586_);
v___x_590_ = l_NsExport_analyze(v_ps_522_, v_body_586_, v_snd_589_);
v_fst_591_ = lean_ctor_get(v___x_590_, 0);
lean_inc(v_fst_591_);
v_snd_592_ = lean_ctor_get(v___x_590_, 1);
lean_inc(v_snd_592_);
lean_dec_ref(v___x_590_);
v_tree_593_ = lean_ctor_get(v_fst_588_, 0);
lean_inc(v_tree_593_);
v_h_594_ = lean_ctor_get_uint64(v_fst_588_, sizeof(void*)*1);
lean_dec(v_fst_588_);
v_tree_595_ = lean_ctor_get(v_fst_591_, 0);
v_h_596_ = lean_ctor_get_uint64(v_fst_591_, sizeof(void*)*1);
v_isSharedCheck_609_ = !lean_is_exclusive(v_fst_591_);
if (v_isSharedCheck_609_ == 0)
{
v___x_598_ = v_fst_591_;
v_isShared_599_ = v_isSharedCheck_609_;
goto v_resetjp_597_;
}
else
{
lean_inc(v_tree_595_);
lean_dec(v_fst_591_);
v___x_598_ = lean_box(0);
v_isShared_599_ = v_isSharedCheck_609_;
goto v_resetjp_597_;
}
v_resetjp_597_:
{
lean_object* v___x_600_; lean_object* v___x_601_; lean_object* v___x_602_; uint64_t v___x_603_; uint64_t v___x_604_; uint64_t v___x_605_; lean_object* v___x_607_; 
v___x_600_ = lean_nat_add(v_tree_593_, v_tree_595_);
lean_dec(v_tree_595_);
lean_dec(v_tree_593_);
v___x_601_ = lean_unsigned_to_nat(1u);
v___x_602_ = lean_nat_add(v___x_600_, v___x_601_);
lean_dec(v___x_600_);
v___x_603_ = 61ULL;
v___x_604_ = lean_uint64_mix_hash(v_h_594_, v_h_596_);
v___x_605_ = lean_uint64_mix_hash(v___x_603_, v___x_604_);
if (v_isShared_599_ == 0)
{
lean_ctor_set(v___x_598_, 0, v___x_602_);
v___x_607_ = v___x_598_;
goto v_reusejp_606_;
}
else
{
lean_object* v_reuseFailAlloc_608_; 
v_reuseFailAlloc_608_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v_reuseFailAlloc_608_, 0, v___x_602_);
v___x_607_ = v_reuseFailAlloc_608_;
goto v_reusejp_606_;
}
v_reusejp_606_:
{
lean_ctor_set_uint64(v___x_607_, sizeof(void*)*1, v___x_605_);
v_r_526_ = v___x_607_;
v___y_527_ = v_snd_592_;
goto v___jp_525_;
}
}
}
case 8:
{
lean_object* v_type_610_; lean_object* v_value_611_; lean_object* v_body_612_; lean_object* v___x_613_; lean_object* v_fst_614_; lean_object* v_snd_615_; lean_object* v___x_616_; lean_object* v_fst_617_; lean_object* v_snd_618_; lean_object* v___x_619_; lean_object* v_fst_620_; lean_object* v_snd_621_; lean_object* v_tree_622_; uint64_t v_h_623_; lean_object* v_tree_624_; uint64_t v_h_625_; lean_object* v_tree_626_; uint64_t v_h_627_; lean_object* v___x_629_; uint8_t v_isShared_630_; uint8_t v_isSharedCheck_642_; 
v_type_610_ = lean_ctor_get(v_e_523_, 1);
v_value_611_ = lean_ctor_get(v_e_523_, 2);
v_body_612_ = lean_ctor_get(v_e_523_, 3);
lean_inc_ref(v_type_610_);
v___x_613_ = l_NsExport_analyze(v_ps_522_, v_type_610_, v_a_524_);
v_fst_614_ = lean_ctor_get(v___x_613_, 0);
lean_inc(v_fst_614_);
v_snd_615_ = lean_ctor_get(v___x_613_, 1);
lean_inc(v_snd_615_);
lean_dec_ref(v___x_613_);
lean_inc_ref(v_value_611_);
v___x_616_ = l_NsExport_analyze(v_ps_522_, v_value_611_, v_snd_615_);
v_fst_617_ = lean_ctor_get(v___x_616_, 0);
lean_inc(v_fst_617_);
v_snd_618_ = lean_ctor_get(v___x_616_, 1);
lean_inc(v_snd_618_);
lean_dec_ref(v___x_616_);
lean_inc_ref(v_body_612_);
v___x_619_ = l_NsExport_analyze(v_ps_522_, v_body_612_, v_snd_618_);
v_fst_620_ = lean_ctor_get(v___x_619_, 0);
lean_inc(v_fst_620_);
v_snd_621_ = lean_ctor_get(v___x_619_, 1);
lean_inc(v_snd_621_);
lean_dec_ref(v___x_619_);
v_tree_622_ = lean_ctor_get(v_fst_614_, 0);
lean_inc(v_tree_622_);
v_h_623_ = lean_ctor_get_uint64(v_fst_614_, sizeof(void*)*1);
lean_dec(v_fst_614_);
v_tree_624_ = lean_ctor_get(v_fst_617_, 0);
lean_inc(v_tree_624_);
v_h_625_ = lean_ctor_get_uint64(v_fst_617_, sizeof(void*)*1);
lean_dec(v_fst_617_);
v_tree_626_ = lean_ctor_get(v_fst_620_, 0);
v_h_627_ = lean_ctor_get_uint64(v_fst_620_, sizeof(void*)*1);
v_isSharedCheck_642_ = !lean_is_exclusive(v_fst_620_);
if (v_isSharedCheck_642_ == 0)
{
v___x_629_ = v_fst_620_;
v_isShared_630_ = v_isSharedCheck_642_;
goto v_resetjp_628_;
}
else
{
lean_inc(v_tree_626_);
lean_dec(v_fst_620_);
v___x_629_ = lean_box(0);
v_isShared_630_ = v_isSharedCheck_642_;
goto v_resetjp_628_;
}
v_resetjp_628_:
{
lean_object* v___x_631_; lean_object* v___x_632_; lean_object* v___x_633_; lean_object* v___x_634_; uint64_t v___x_635_; uint64_t v___x_636_; uint64_t v___x_637_; uint64_t v___x_638_; lean_object* v___x_640_; 
v___x_631_ = lean_nat_add(v_tree_622_, v_tree_624_);
lean_dec(v_tree_624_);
lean_dec(v_tree_622_);
v___x_632_ = lean_nat_add(v___x_631_, v_tree_626_);
lean_dec(v_tree_626_);
lean_dec(v___x_631_);
v___x_633_ = lean_unsigned_to_nat(1u);
v___x_634_ = lean_nat_add(v___x_632_, v___x_633_);
lean_dec(v___x_632_);
v___x_635_ = 67ULL;
v___x_636_ = lean_uint64_mix_hash(v_h_625_, v_h_627_);
v___x_637_ = lean_uint64_mix_hash(v_h_623_, v___x_636_);
v___x_638_ = lean_uint64_mix_hash(v___x_635_, v___x_637_);
if (v_isShared_630_ == 0)
{
lean_ctor_set(v___x_629_, 0, v___x_634_);
v___x_640_ = v___x_629_;
goto v_reusejp_639_;
}
else
{
lean_object* v_reuseFailAlloc_641_; 
v_reuseFailAlloc_641_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v_reuseFailAlloc_641_, 0, v___x_634_);
v___x_640_ = v_reuseFailAlloc_641_;
goto v_reusejp_639_;
}
v_reusejp_639_:
{
lean_ctor_set_uint64(v___x_640_, sizeof(void*)*1, v___x_638_);
v_r_526_ = v___x_640_;
v___y_527_ = v_snd_621_;
goto v___jp_525_;
}
}
}
case 11:
{
lean_object* v_typeName_643_; lean_object* v_idx_644_; lean_object* v_struct_645_; lean_object* v___x_646_; lean_object* v_fst_647_; lean_object* v_snd_648_; lean_object* v_tree_649_; uint64_t v_h_650_; lean_object* v___x_652_; uint8_t v_isShared_653_; uint8_t v_isSharedCheck_668_; 
v_typeName_643_ = lean_ctor_get(v_e_523_, 0);
v_idx_644_ = lean_ctor_get(v_e_523_, 1);
v_struct_645_ = lean_ctor_get(v_e_523_, 2);
lean_inc_ref(v_struct_645_);
v___x_646_ = l_NsExport_analyze(v_ps_522_, v_struct_645_, v_a_524_);
v_fst_647_ = lean_ctor_get(v___x_646_, 0);
lean_inc(v_fst_647_);
v_snd_648_ = lean_ctor_get(v___x_646_, 1);
lean_inc(v_snd_648_);
lean_dec_ref(v___x_646_);
v_tree_649_ = lean_ctor_get(v_fst_647_, 0);
v_h_650_ = lean_ctor_get_uint64(v_fst_647_, sizeof(void*)*1);
v_isSharedCheck_668_ = !lean_is_exclusive(v_fst_647_);
if (v_isSharedCheck_668_ == 0)
{
v___x_652_ = v_fst_647_;
v_isShared_653_ = v_isSharedCheck_668_;
goto v_resetjp_651_;
}
else
{
lean_inc(v_tree_649_);
lean_dec(v_fst_647_);
v___x_652_ = lean_box(0);
v_isShared_653_ = v_isSharedCheck_668_;
goto v_resetjp_651_;
}
v_resetjp_651_:
{
lean_object* v___x_654_; lean_object* v___x_655_; uint64_t v___x_656_; uint64_t v___y_658_; 
v___x_654_ = lean_unsigned_to_nat(1u);
v___x_655_ = lean_nat_add(v_tree_649_, v___x_654_);
lean_dec(v_tree_649_);
v___x_656_ = 71ULL;
if (lean_obj_tag(v_typeName_643_) == 0)
{
uint64_t v___x_666_; 
v___x_666_ = 1723ULL;
v___y_658_ = v___x_666_;
goto v___jp_657_;
}
else
{
uint64_t v_hash_667_; 
v_hash_667_ = lean_ctor_get_uint64(v_typeName_643_, sizeof(void*)*2);
v___y_658_ = v_hash_667_;
goto v___jp_657_;
}
v___jp_657_:
{
uint64_t v___x_659_; uint64_t v___x_660_; uint64_t v___x_661_; uint64_t v___x_662_; lean_object* v___x_664_; 
v___x_659_ = lean_uint64_of_nat(v_idx_644_);
v___x_660_ = lean_uint64_mix_hash(v___x_659_, v_h_650_);
v___x_661_ = lean_uint64_mix_hash(v___y_658_, v___x_660_);
v___x_662_ = lean_uint64_mix_hash(v___x_656_, v___x_661_);
if (v_isShared_653_ == 0)
{
lean_ctor_set(v___x_652_, 0, v___x_655_);
v___x_664_ = v___x_652_;
goto v_reusejp_663_;
}
else
{
lean_object* v_reuseFailAlloc_665_; 
v_reuseFailAlloc_665_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v_reuseFailAlloc_665_, 0, v___x_655_);
v___x_664_ = v_reuseFailAlloc_665_;
goto v_reusejp_663_;
}
v_reusejp_663_:
{
lean_ctor_set_uint64(v___x_664_, sizeof(void*)*1, v___x_662_);
v_r_526_ = v___x_664_;
v___y_527_ = v_snd_648_;
goto v___jp_525_;
}
}
}
}
case 0:
{
lean_object* v_deBruijnIndex_669_; lean_object* v___x_670_; uint64_t v___x_671_; uint64_t v___x_672_; uint64_t v___x_673_; lean_object* v___x_674_; 
v_deBruijnIndex_669_ = lean_ctor_get(v_e_523_, 0);
v___x_670_ = lean_unsigned_to_nat(1u);
v___x_671_ = 3ULL;
v___x_672_ = lean_uint64_of_nat(v_deBruijnIndex_669_);
v___x_673_ = lean_uint64_mix_hash(v___x_671_, v___x_672_);
v___x_674_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_674_, 0, v___x_670_);
lean_ctor_set_uint64(v___x_674_, sizeof(void*)*1, v___x_673_);
v_r_526_ = v___x_674_;
v___y_527_ = v_a_524_;
goto v___jp_525_;
}
case 3:
{
lean_object* v_u_675_; lean_object* v___x_676_; uint64_t v___x_677_; uint64_t v___x_678_; uint64_t v___x_679_; lean_object* v___x_680_; 
v_u_675_ = lean_ctor_get(v_e_523_, 0);
v___x_676_ = lean_unsigned_to_nat(1u);
v___x_677_ = 37ULL;
v___x_678_ = l_NsExport_hashLevel(v_ps_522_, v_u_675_);
v___x_679_ = lean_uint64_mix_hash(v___x_677_, v___x_678_);
v___x_680_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_680_, 0, v___x_676_);
lean_ctor_set_uint64(v___x_680_, sizeof(void*)*1, v___x_679_);
v_r_526_ = v___x_680_;
v___y_527_ = v_a_524_;
goto v___jp_525_;
}
case 9:
{
lean_object* v_a_681_; 
v_a_681_ = lean_ctor_get(v_e_523_, 0);
if (lean_obj_tag(v_a_681_) == 0)
{
lean_object* v_val_682_; lean_object* v___x_683_; uint64_t v___x_684_; uint64_t v___x_685_; uint64_t v___x_686_; lean_object* v___x_687_; 
v_val_682_ = lean_ctor_get(v_a_681_, 0);
v___x_683_ = lean_unsigned_to_nat(1u);
v___x_684_ = 41ULL;
v___x_685_ = lean_uint64_of_nat(v_val_682_);
v___x_686_ = lean_uint64_mix_hash(v___x_684_, v___x_685_);
v___x_687_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_687_, 0, v___x_683_);
lean_ctor_set_uint64(v___x_687_, sizeof(void*)*1, v___x_686_);
v_r_526_ = v___x_687_;
v___y_527_ = v_a_524_;
goto v___jp_525_;
}
else
{
lean_object* v_val_688_; lean_object* v___x_689_; uint64_t v___x_690_; uint64_t v___x_691_; uint64_t v___x_692_; lean_object* v___x_693_; 
v_val_688_ = lean_ctor_get(v_a_681_, 0);
v___x_689_ = lean_unsigned_to_nat(1u);
v___x_690_ = 43ULL;
v___x_691_ = lean_string_hash(v_val_688_);
v___x_692_ = lean_uint64_mix_hash(v___x_690_, v___x_691_);
v___x_693_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_693_, 0, v___x_689_);
lean_ctor_set_uint64(v___x_693_, sizeof(void*)*1, v___x_692_);
v_r_526_ = v___x_693_;
v___y_527_ = v_a_524_;
goto v___jp_525_;
}
}
case 4:
{
lean_object* v_declName_694_; lean_object* v_us_695_; lean_object* v___x_696_; uint64_t v___x_697_; uint64_t v___y_699_; 
v_declName_694_ = lean_ctor_get(v_e_523_, 0);
v_us_695_ = lean_ctor_get(v_e_523_, 1);
v___x_696_ = lean_unsigned_to_nat(1u);
v___x_697_ = 5ULL;
if (lean_obj_tag(v_declName_694_) == 0)
{
uint64_t v___x_703_; 
v___x_703_ = 1723ULL;
v___y_699_ = v___x_703_;
goto v___jp_698_;
}
else
{
uint64_t v_hash_704_; 
v_hash_704_ = lean_ctor_get_uint64(v_declName_694_, sizeof(void*)*2);
v___y_699_ = v_hash_704_;
goto v___jp_698_;
}
v___jp_698_:
{
uint64_t v___x_700_; uint64_t v___x_701_; lean_object* v___x_702_; 
v___x_700_ = l_List_foldl___at___00NsExport_analyze_spec__0(v_ps_522_, v___y_699_, v_us_695_);
v___x_701_ = lean_uint64_mix_hash(v___x_697_, v___x_700_);
v___x_702_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_702_, 0, v___x_696_);
lean_ctor_set_uint64(v___x_702_, sizeof(void*)*1, v___x_701_);
v_r_526_ = v___x_702_;
v___y_527_ = v_a_524_;
goto v___jp_525_;
}
}
default: 
{
lean_object* v___x_705_; 
v___x_705_ = ((lean_object*)(l_NsExport_analyze___closed__0));
v_r_526_ = v___x_705_;
v___y_527_ = v_a_524_;
goto v___jp_525_;
}
}
}
}
v___jp_525_:
{
lean_object* v___x_528_; lean_object* v___x_529_; 
lean_inc_ref(v_r_526_);
v___x_528_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Meta_ExprDefEq_0__Lean_Meta_CheckAssignment_cache_spec__0___redArg(v___y_527_, v_e_523_, v_r_526_);
v___x_529_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_529_, 0, v_r_526_);
lean_ctor_set(v___x_529_, 1, v___x_528_);
return v___x_529_;
}
}
}
LEAN_EXPORT lean_object* l_NsExport_analyze___boxed(lean_object* v_ps_706_, lean_object* v_e_707_, lean_object* v_a_708_){
_start:
{
lean_object* v_res_709_; 
v_res_709_ = l_NsExport_analyze(v_ps_706_, v_e_707_, v_a_708_);
lean_dec(v_ps_706_);
return v_res_709_;
}
}
static lean_object* _init_l_NsExport_sizes___closed__0(void){
_start:
{
lean_object* v___x_710_; lean_object* v___x_711_; lean_object* v___x_712_; 
v___x_710_ = lean_box(0);
v___x_711_ = lean_unsigned_to_nat(16u);
v___x_712_ = lean_mk_array(v___x_711_, v___x_710_);
return v___x_712_;
}
}
static lean_object* _init_l_NsExport_sizes___closed__1(void){
_start:
{
lean_object* v___x_713_; lean_object* v___x_714_; lean_object* v___x_715_; 
v___x_713_ = lean_obj_once(&l_NsExport_sizes___closed__0, &l_NsExport_sizes___closed__0_once, _init_l_NsExport_sizes___closed__0);
v___x_714_ = lean_unsigned_to_nat(0u);
v___x_715_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_715_, 0, v___x_714_);
lean_ctor_set(v___x_715_, 1, v___x_713_);
return v___x_715_;
}
}
LEAN_EXPORT lean_object* l_NsExport_sizes(lean_object* v_ps_716_, lean_object* v_e_717_){
_start:
{
lean_object* v___x_718_; lean_object* v___x_719_; lean_object* v_fst_720_; lean_object* v_snd_721_; lean_object* v___x_723_; uint8_t v_isShared_724_; uint8_t v_isSharedCheck_740_; 
v___x_718_ = lean_obj_once(&l_NsExport_sizes___closed__1, &l_NsExport_sizes___closed__1_once, _init_l_NsExport_sizes___closed__1);
v___x_719_ = l_NsExport_analyze(v_ps_716_, v_e_717_, v___x_718_);
v_fst_720_ = lean_ctor_get(v___x_719_, 0);
v_snd_721_ = lean_ctor_get(v___x_719_, 1);
v_isSharedCheck_740_ = !lean_is_exclusive(v___x_719_);
if (v_isSharedCheck_740_ == 0)
{
v___x_723_ = v___x_719_;
v_isShared_724_ = v_isSharedCheck_740_;
goto v_resetjp_722_;
}
else
{
lean_inc(v_snd_721_);
lean_inc(v_fst_720_);
lean_dec(v___x_719_);
v___x_723_ = lean_box(0);
v_isShared_724_ = v_isSharedCheck_740_;
goto v_resetjp_722_;
}
v_resetjp_722_:
{
lean_object* v_tree_725_; uint64_t v_h_726_; lean_object* v_size_727_; lean_object* v___x_729_; uint8_t v_isShared_730_; uint8_t v_isSharedCheck_738_; 
v_tree_725_ = lean_ctor_get(v_fst_720_, 0);
lean_inc(v_tree_725_);
v_h_726_ = lean_ctor_get_uint64(v_fst_720_, sizeof(void*)*1);
lean_dec(v_fst_720_);
v_size_727_ = lean_ctor_get(v_snd_721_, 0);
v_isSharedCheck_738_ = !lean_is_exclusive(v_snd_721_);
if (v_isSharedCheck_738_ == 0)
{
lean_object* v_unused_739_; 
v_unused_739_ = lean_ctor_get(v_snd_721_, 1);
lean_dec(v_unused_739_);
v___x_729_ = v_snd_721_;
v_isShared_730_ = v_isSharedCheck_738_;
goto v_resetjp_728_;
}
else
{
lean_inc(v_size_727_);
lean_dec(v_snd_721_);
v___x_729_ = lean_box(0);
v_isShared_730_ = v_isSharedCheck_738_;
goto v_resetjp_728_;
}
v_resetjp_728_:
{
lean_object* v___x_731_; lean_object* v___x_733_; 
v___x_731_ = lean_box_uint64(v_h_726_);
if (v_isShared_724_ == 0)
{
lean_ctor_set(v___x_723_, 1, v___x_731_);
lean_ctor_set(v___x_723_, 0, v_size_727_);
v___x_733_ = v___x_723_;
goto v_reusejp_732_;
}
else
{
lean_object* v_reuseFailAlloc_737_; 
v_reuseFailAlloc_737_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_737_, 0, v_size_727_);
lean_ctor_set(v_reuseFailAlloc_737_, 1, v___x_731_);
v___x_733_ = v_reuseFailAlloc_737_;
goto v_reusejp_732_;
}
v_reusejp_732_:
{
lean_object* v___x_735_; 
if (v_isShared_730_ == 0)
{
lean_ctor_set(v___x_729_, 1, v___x_733_);
lean_ctor_set(v___x_729_, 0, v_tree_725_);
v___x_735_ = v___x_729_;
goto v_reusejp_734_;
}
else
{
lean_object* v_reuseFailAlloc_736_; 
v_reuseFailAlloc_736_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_736_, 0, v_tree_725_);
lean_ctor_set(v_reuseFailAlloc_736_, 1, v___x_733_);
v___x_735_ = v_reuseFailAlloc_736_;
goto v_reusejp_734_;
}
v_reusejp_734_:
{
return v___x_735_;
}
}
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_sizes___boxed(lean_object* v_ps_741_, lean_object* v_e_742_){
_start:
{
lean_object* v_res_743_; 
v_res_743_ = l_NsExport_sizes(v_ps_741_, v_e_742_);
lean_dec(v_ps_741_);
return v_res_743_;
}
}
LEAN_EXPORT lean_object* l_NsExport_valueOf_x3f(lean_object* v_x_744_){
_start:
{
switch(lean_obj_tag(v_x_744_))
{
case 2:
{
lean_object* v_val_745_; lean_object* v___x_747_; uint8_t v_isShared_748_; uint8_t v_isSharedCheck_753_; 
v_val_745_ = lean_ctor_get(v_x_744_, 0);
v_isSharedCheck_753_ = !lean_is_exclusive(v_x_744_);
if (v_isSharedCheck_753_ == 0)
{
v___x_747_ = v_x_744_;
v_isShared_748_ = v_isSharedCheck_753_;
goto v_resetjp_746_;
}
else
{
lean_inc(v_val_745_);
lean_dec(v_x_744_);
v___x_747_ = lean_box(0);
v_isShared_748_ = v_isSharedCheck_753_;
goto v_resetjp_746_;
}
v_resetjp_746_:
{
lean_object* v_value_749_; lean_object* v___x_751_; 
v_value_749_ = lean_ctor_get(v_val_745_, 1);
lean_inc_ref(v_value_749_);
lean_dec_ref(v_val_745_);
if (v_isShared_748_ == 0)
{
lean_ctor_set_tag(v___x_747_, 1);
lean_ctor_set(v___x_747_, 0, v_value_749_);
v___x_751_ = v___x_747_;
goto v_reusejp_750_;
}
else
{
lean_object* v_reuseFailAlloc_752_; 
v_reuseFailAlloc_752_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_752_, 0, v_value_749_);
v___x_751_ = v_reuseFailAlloc_752_;
goto v_reusejp_750_;
}
v_reusejp_750_:
{
return v___x_751_;
}
}
}
case 1:
{
lean_object* v_val_754_; lean_object* v___x_756_; uint8_t v_isShared_757_; uint8_t v_isSharedCheck_762_; 
v_val_754_ = lean_ctor_get(v_x_744_, 0);
v_isSharedCheck_762_ = !lean_is_exclusive(v_x_744_);
if (v_isSharedCheck_762_ == 0)
{
v___x_756_ = v_x_744_;
v_isShared_757_ = v_isSharedCheck_762_;
goto v_resetjp_755_;
}
else
{
lean_inc(v_val_754_);
lean_dec(v_x_744_);
v___x_756_ = lean_box(0);
v_isShared_757_ = v_isSharedCheck_762_;
goto v_resetjp_755_;
}
v_resetjp_755_:
{
lean_object* v_value_758_; lean_object* v___x_760_; 
v_value_758_ = lean_ctor_get(v_val_754_, 1);
lean_inc_ref(v_value_758_);
lean_dec_ref(v_val_754_);
if (v_isShared_757_ == 0)
{
lean_ctor_set(v___x_756_, 0, v_value_758_);
v___x_760_ = v___x_756_;
goto v_reusejp_759_;
}
else
{
lean_object* v_reuseFailAlloc_761_; 
v_reuseFailAlloc_761_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_761_, 0, v_value_758_);
v___x_760_ = v_reuseFailAlloc_761_;
goto v_reusejp_759_;
}
v_reusejp_759_:
{
return v___x_760_;
}
}
}
case 3:
{
lean_object* v_val_763_; lean_object* v___x_765_; uint8_t v_isShared_766_; uint8_t v_isSharedCheck_771_; 
v_val_763_ = lean_ctor_get(v_x_744_, 0);
v_isSharedCheck_771_ = !lean_is_exclusive(v_x_744_);
if (v_isSharedCheck_771_ == 0)
{
v___x_765_ = v_x_744_;
v_isShared_766_ = v_isSharedCheck_771_;
goto v_resetjp_764_;
}
else
{
lean_inc(v_val_763_);
lean_dec(v_x_744_);
v___x_765_ = lean_box(0);
v_isShared_766_ = v_isSharedCheck_771_;
goto v_resetjp_764_;
}
v_resetjp_764_:
{
lean_object* v_value_767_; lean_object* v___x_769_; 
v_value_767_ = lean_ctor_get(v_val_763_, 1);
lean_inc_ref(v_value_767_);
lean_dec_ref(v_val_763_);
if (v_isShared_766_ == 0)
{
lean_ctor_set_tag(v___x_765_, 1);
lean_ctor_set(v___x_765_, 0, v_value_767_);
v___x_769_ = v___x_765_;
goto v_reusejp_768_;
}
else
{
lean_object* v_reuseFailAlloc_770_; 
v_reuseFailAlloc_770_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_770_, 0, v_value_767_);
v___x_769_ = v_reuseFailAlloc_770_;
goto v_reusejp_768_;
}
v_reusejp_768_:
{
return v___x_769_;
}
}
}
default: 
{
lean_object* v___x_772_; 
lean_dec_ref(v_x_744_);
v___x_772_ = lean_box(0);
return v___x_772_;
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_hexOf(uint64_t v_h_774_){
_start:
{
lean_object* v___x_775_; lean_object* v___x_776_; lean_object* v___x_777_; lean_object* v_s_778_; lean_object* v___x_779_; lean_object* v___x_780_; lean_object* v___x_781_; lean_object* v___x_782_; lean_object* v___x_783_; 
v___x_775_ = lean_unsigned_to_nat(16u);
v___x_776_ = lean_uint64_to_nat(v_h_774_);
v___x_777_ = l_Nat_toDigits(v___x_775_, v___x_776_);
v_s_778_ = lean_string_mk(v___x_777_);
v___x_779_ = ((lean_object*)(l_NsExport_hexOf___closed__0));
v___x_780_ = lean_string_length(v_s_778_);
v___x_781_ = lean_nat_sub(v___x_775_, v___x_780_);
v___x_782_ = l___private_Init_Data_Nat_Basic_0__Nat_repeatTR_loop___at___00Std_Time_instToStringDuration_leftPad_spec__0(v___x_781_, v___x_779_);
v___x_783_ = lean_string_append(v___x_782_, v_s_778_);
lean_dec_ref(v_s_778_);
return v___x_783_;
}
}
LEAN_EXPORT lean_object* l_NsExport_hexOf___boxed(lean_object* v_h_784_){
_start:
{
uint64_t v_h_boxed_785_; lean_object* v_res_786_; 
v_h_boxed_785_ = lean_unbox_uint64(v_h_784_);
lean_dec_ref(v_h_784_);
v_res_786_ = l_NsExport_hexOf(v_h_boxed_785_);
return v_res_786_;
}
}
LEAN_EXPORT lean_object* l_NsExport_moduleOf(lean_object* v_env_787_, lean_object* v_n_788_){
_start:
{
lean_object* v___x_789_; 
v___x_789_ = l_Lean_Environment_getModuleIdxFor_x3f(v_env_787_, v_n_788_);
if (lean_obj_tag(v___x_789_) == 0)
{
lean_object* v___x_790_; 
v___x_790_ = lean_box(0);
return v___x_790_;
}
else
{
lean_object* v_val_791_; lean_object* v___x_792_; lean_object* v___x_793_; lean_object* v___x_794_; lean_object* v___x_795_; 
v_val_791_ = lean_ctor_get(v___x_789_, 0);
lean_inc(v_val_791_);
lean_dec_ref_known(v___x_789_, 1);
v___x_792_ = lean_box(0);
v___x_793_ = l_Lean_Environment_header(v_env_787_);
v___x_794_ = l_Lean_EnvironmentHeader_moduleNames(v___x_793_);
v___x_795_ = lean_array_get(v___x_792_, v___x_794_, v_val_791_);
lean_dec(v_val_791_);
lean_dec_ref(v___x_794_);
return v___x_795_;
}
}
}
LEAN_EXPORT lean_object* l_NsExport_moduleOf___boxed(lean_object* v_env_796_, lean_object* v_n_797_){
_start:
{
lean_object* v_res_798_; 
v_res_798_ = l_NsExport_moduleOf(v_env_796_, v_n_797_);
lean_dec(v_n_797_);
lean_dec_ref(v_env_796_);
return v_res_798_;
}
}
LEAN_EXPORT lean_object* l_NsExport_resolveRoot(lean_object* v_cx_799_, lean_object* v_n_800_, lean_object* v_fuel_801_){
_start:
{
lean_object* v_p_803_; lean_object* v___x_807_; uint8_t v___x_808_; 
v___x_807_ = lean_unsigned_to_nat(0u);
v___x_808_ = lean_nat_dec_eq(v_fuel_801_, v___x_807_);
if (v___x_808_ == 0)
{
lean_object* v_cls_809_; lean_object* v___x_810_; 
v_cls_809_ = lean_ctor_get(v_cx_799_, 2);
v___x_810_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__0___redArg(v_cls_809_, v_n_800_);
if (lean_obj_tag(v___x_810_) == 1)
{
lean_object* v_val_811_; lean_object* v___x_813_; uint8_t v_isShared_814_; uint8_t v_isSharedCheck_822_; 
v_val_811_ = lean_ctor_get(v___x_810_, 0);
v_isSharedCheck_822_ = !lean_is_exclusive(v___x_810_);
if (v_isSharedCheck_822_ == 0)
{
v___x_813_ = v___x_810_;
v_isShared_814_ = v_isSharedCheck_822_;
goto v_resetjp_812_;
}
else
{
lean_inc(v_val_811_);
lean_dec(v___x_810_);
v___x_813_ = lean_box(0);
v_isShared_814_ = v_isSharedCheck_822_;
goto v_resetjp_812_;
}
v_resetjp_812_:
{
switch(lean_obj_tag(v_val_811_))
{
case 0:
{
lean_object* v___x_816_; 
lean_dec(v_fuel_801_);
if (v_isShared_814_ == 0)
{
lean_ctor_set(v___x_813_, 0, v_n_800_);
v___x_816_ = v___x_813_;
goto v_reusejp_815_;
}
else
{
lean_object* v_reuseFailAlloc_817_; 
v_reuseFailAlloc_817_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_817_, 0, v_n_800_);
v___x_816_ = v_reuseFailAlloc_817_;
goto v_reusejp_815_;
}
v_reusejp_815_:
{
return v___x_816_;
}
}
case 1:
{
lean_object* v_parent_818_; 
lean_del_object(v___x_813_);
lean_dec(v_n_800_);
v_parent_818_ = lean_ctor_get(v_val_811_, 0);
lean_inc(v_parent_818_);
lean_dec_ref_known(v_val_811_, 1);
v_p_803_ = v_parent_818_;
goto v___jp_802_;
}
case 2:
{
lean_object* v_parent_819_; 
lean_del_object(v___x_813_);
lean_dec(v_n_800_);
v_parent_819_ = lean_ctor_get(v_val_811_, 0);
lean_inc(v_parent_819_);
lean_dec_ref_known(v_val_811_, 1);
v_p_803_ = v_parent_819_;
goto v___jp_802_;
}
case 3:
{
lean_object* v_parent_820_; 
lean_del_object(v___x_813_);
lean_dec(v_n_800_);
v_parent_820_ = lean_ctor_get(v_val_811_, 0);
lean_inc(v_parent_820_);
lean_dec_ref_known(v_val_811_, 1);
v_p_803_ = v_parent_820_;
goto v___jp_802_;
}
default: 
{
lean_object* v___x_821_; 
lean_del_object(v___x_813_);
lean_dec(v_val_811_);
lean_dec(v_fuel_801_);
lean_dec(v_n_800_);
v___x_821_ = lean_box(0);
return v___x_821_;
}
}
}
}
else
{
lean_object* v___x_823_; 
lean_dec(v___x_810_);
lean_dec(v_fuel_801_);
lean_dec(v_n_800_);
v___x_823_ = lean_box(0);
return v___x_823_;
}
}
else
{
lean_object* v___x_824_; 
lean_dec(v_fuel_801_);
lean_dec(v_n_800_);
v___x_824_ = lean_box(0);
return v___x_824_;
}
v___jp_802_:
{
lean_object* v___x_804_; lean_object* v___x_805_; 
v___x_804_ = lean_unsigned_to_nat(1u);
v___x_805_ = lean_nat_sub(v_fuel_801_, v___x_804_);
lean_dec(v_fuel_801_);
v_n_800_ = v_p_803_;
v_fuel_801_ = v___x_805_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l_NsExport_resolveRoot___boxed(lean_object* v_cx_825_, lean_object* v_n_826_, lean_object* v_fuel_827_){
_start:
{
lean_object* v_res_828_; 
v_res_828_ = l_NsExport_resolveRoot(v_cx_825_, v_n_826_, v_fuel_827_);
lean_dec_ref(v_cx_825_);
return v_res_828_;
}
}
LEAN_EXPORT uint8_t l_Option_instBEq_beq___at___00NsExport_resolveDeps_spec__0(lean_object* v_x_829_, lean_object* v_x_830_){
_start:
{
if (lean_obj_tag(v_x_829_) == 0)
{
if (lean_obj_tag(v_x_830_) == 0)
{
uint8_t v___x_831_; 
v___x_831_ = 1;
return v___x_831_;
}
else
{
uint8_t v___x_832_; 
v___x_832_ = 0;
return v___x_832_;
}
}
else
{
if (lean_obj_tag(v_x_830_) == 0)
{
uint8_t v___x_833_; 
v___x_833_ = 0;
return v___x_833_;
}
else
{
lean_object* v_val_834_; lean_object* v_val_835_; uint8_t v___x_836_; 
v_val_834_ = lean_ctor_get(v_x_829_, 0);
v_val_835_ = lean_ctor_get(v_x_830_, 0);
v___x_836_ = l_NsExport_instBEqCls_beq(v_val_834_, v_val_835_);
return v___x_836_;
}
}
}
}
LEAN_EXPORT lean_object* l_Option_instBEq_beq___at___00NsExport_resolveDeps_spec__0___boxed(lean_object* v_x_837_, lean_object* v_x_838_){
_start:
{
uint8_t v_res_839_; lean_object* v_r_840_; 
v_res_839_ = l_Option_instBEq_beq___at___00NsExport_resolveDeps_spec__0(v_x_837_, v_x_838_);
lean_dec(v_x_838_);
lean_dec(v_x_837_);
v_r_840_ = lean_box(v_res_839_);
return v_r_840_;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg(lean_object* v_cx_843_, lean_object* v_self_844_, lean_object* v_a_845_){
_start:
{
lean_object* v_snd_846_; lean_object* v_snd_847_; lean_object* v_fst_848_; lean_object* v___x_850_; uint8_t v_isShared_851_; uint8_t v_isSharedCheck_978_; 
v_snd_846_ = lean_ctor_get(v_a_845_, 1);
lean_inc(v_snd_846_);
v_snd_847_ = lean_ctor_get(v_snd_846_, 1);
lean_inc(v_snd_847_);
v_fst_848_ = lean_ctor_get(v_a_845_, 0);
v_isSharedCheck_978_ = !lean_is_exclusive(v_a_845_);
if (v_isSharedCheck_978_ == 0)
{
lean_object* v_unused_979_; 
v_unused_979_ = lean_ctor_get(v_a_845_, 1);
lean_dec(v_unused_979_);
v___x_850_ = v_a_845_;
v_isShared_851_ = v_isSharedCheck_978_;
goto v_resetjp_849_;
}
else
{
lean_inc(v_fst_848_);
lean_dec(v_a_845_);
v___x_850_ = lean_box(0);
v_isShared_851_ = v_isSharedCheck_978_;
goto v_resetjp_849_;
}
v_resetjp_849_:
{
lean_object* v_fst_852_; lean_object* v___x_854_; uint8_t v_isShared_855_; uint8_t v_isSharedCheck_976_; 
v_fst_852_ = lean_ctor_get(v_snd_846_, 0);
v_isSharedCheck_976_ = !lean_is_exclusive(v_snd_846_);
if (v_isSharedCheck_976_ == 0)
{
lean_object* v_unused_977_; 
v_unused_977_ = lean_ctor_get(v_snd_846_, 1);
lean_dec(v_unused_977_);
v___x_854_ = v_snd_846_;
v_isShared_855_ = v_isSharedCheck_976_;
goto v_resetjp_853_;
}
else
{
lean_inc(v_fst_852_);
lean_dec(v_snd_846_);
v___x_854_ = lean_box(0);
v_isShared_855_ = v_isSharedCheck_976_;
goto v_resetjp_853_;
}
v_resetjp_853_:
{
lean_object* v_fst_856_; lean_object* v_snd_857_; lean_object* v___x_859_; uint8_t v_isShared_860_; uint8_t v_isSharedCheck_975_; 
v_fst_856_ = lean_ctor_get(v_snd_847_, 0);
v_snd_857_ = lean_ctor_get(v_snd_847_, 1);
v_isSharedCheck_975_ = !lean_is_exclusive(v_snd_847_);
if (v_isSharedCheck_975_ == 0)
{
v___x_859_ = v_snd_847_;
v_isShared_860_ = v_isSharedCheck_975_;
goto v_resetjp_858_;
}
else
{
lean_inc(v_snd_857_);
lean_inc(v_fst_856_);
lean_dec(v_snd_847_);
v___x_859_ = lean_box(0);
v_isShared_860_ = v_isSharedCheck_975_;
goto v_resetjp_858_;
}
v_resetjp_858_:
{
uint8_t v___x_861_; 
v___x_861_ = l_List_isEmpty___redArg(v_snd_857_);
if (v___x_861_ == 0)
{
if (lean_obj_tag(v_snd_857_) == 0)
{
lean_object* v___x_863_; 
lean_dec(v_self_844_);
lean_dec_ref(v_cx_843_);
if (v_isShared_860_ == 0)
{
v___x_863_ = v___x_859_;
goto v_reusejp_862_;
}
else
{
lean_object* v_reuseFailAlloc_870_; 
v_reuseFailAlloc_870_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_870_, 0, v_fst_856_);
lean_ctor_set(v_reuseFailAlloc_870_, 1, v_snd_857_);
v___x_863_ = v_reuseFailAlloc_870_;
goto v_reusejp_862_;
}
v_reusejp_862_:
{
lean_object* v___x_865_; 
if (v_isShared_855_ == 0)
{
lean_ctor_set(v___x_854_, 1, v___x_863_);
v___x_865_ = v___x_854_;
goto v_reusejp_864_;
}
else
{
lean_object* v_reuseFailAlloc_869_; 
v_reuseFailAlloc_869_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_869_, 0, v_fst_852_);
lean_ctor_set(v_reuseFailAlloc_869_, 1, v___x_863_);
v___x_865_ = v_reuseFailAlloc_869_;
goto v_reusejp_864_;
}
v_reusejp_864_:
{
lean_object* v___x_867_; 
if (v_isShared_851_ == 0)
{
lean_ctor_set(v___x_850_, 1, v___x_865_);
v___x_867_ = v___x_850_;
goto v_reusejp_866_;
}
else
{
lean_object* v_reuseFailAlloc_868_; 
v_reuseFailAlloc_868_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_868_, 0, v_fst_848_);
lean_ctor_set(v_reuseFailAlloc_868_, 1, v___x_865_);
v___x_867_ = v_reuseFailAlloc_868_;
goto v_reusejp_866_;
}
v_reusejp_866_:
{
return v___x_867_;
}
}
}
}
else
{
lean_object* v_head_871_; lean_object* v_tail_872_; lean_object* v___x_874_; uint8_t v_isShared_875_; uint8_t v_isSharedCheck_965_; 
v_head_871_ = lean_ctor_get(v_snd_857_, 0);
v_tail_872_ = lean_ctor_get(v_snd_857_, 1);
v_isSharedCheck_965_ = !lean_is_exclusive(v_snd_857_);
if (v_isSharedCheck_965_ == 0)
{
v___x_874_ = v_snd_857_;
v_isShared_875_ = v_isSharedCheck_965_;
goto v_resetjp_873_;
}
else
{
lean_inc(v_tail_872_);
lean_inc(v_head_871_);
lean_dec(v_snd_857_);
v___x_874_ = lean_box(0);
v_isShared_875_ = v_isSharedCheck_965_;
goto v_resetjp_873_;
}
v_resetjp_873_:
{
uint8_t v___x_876_; 
v___x_876_ = l_Std_DHashMap_Internal_Raw_u2080_contains___at___00Lean_Server_FileWorker_handleResolveImportAllUnknownIdentifiersCodeAction_x3f_spec__2___redArg(v_fst_856_, v_head_871_);
if (v___x_876_ == 0)
{
lean_object* v_env_877_; lean_object* v_isProj_878_; lean_object* v_cls_879_; lean_object* v___x_880_; lean_object* v___x_881_; lean_object* v___x_894_; uint8_t v___x_895_; 
v_env_877_ = lean_ctor_get(v_cx_843_, 0);
v_isProj_878_ = lean_ctor_get(v_cx_843_, 1);
v_cls_879_ = lean_ctor_get(v_cx_843_, 2);
v___x_880_ = lean_box(0);
lean_inc_n(v_head_871_, 2);
v___x_881_ = l_Std_DHashMap_Internal_Raw_u2080_insertIfNew___at___00__private_Lean_Linter_Extra_UnreachableTactic_0__Lean_Linter_Extra_UnreachableTactic_initFn_00___x40_Lean_Linter_Extra_UnreachableTactic_949854657____hygCtx___hyg_2__spec__0___redArg(v_fst_856_, v_head_871_, v___x_880_);
lean_inc_ref(v_isProj_878_);
v___x_894_ = lean_apply_1(v_isProj_878_, v_head_871_);
v___x_895_ = lean_unbox(v___x_894_);
if (v___x_895_ == 0)
{
lean_del_object(v___x_874_);
goto v___jp_882_;
}
else
{
if (v___x_876_ == 0)
{
lean_object* v___x_896_; lean_object* v___x_897_; uint8_t v___x_898_; uint8_t v___y_930_; 
v___x_896_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__0___redArg(v_cls_879_, v_head_871_);
v___x_897_ = ((lean_object*)(l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg___closed__0));
v___x_898_ = l_Option_instBEq_beq___at___00NsExport_resolveDeps_spec__0(v___x_896_, v___x_897_);
if (v___x_898_ == 0)
{
lean_del_object(v___x_859_);
lean_del_object(v___x_854_);
lean_del_object(v___x_850_);
if (lean_obj_tag(v___x_896_) == 1)
{
lean_object* v_val_944_; lean_object* v___x_946_; uint8_t v_isShared_947_; uint8_t v_isSharedCheck_954_; 
v_val_944_ = lean_ctor_get(v___x_896_, 0);
v_isSharedCheck_954_ = !lean_is_exclusive(v___x_896_);
if (v_isSharedCheck_954_ == 0)
{
v___x_946_ = v___x_896_;
v_isShared_947_ = v_isSharedCheck_954_;
goto v_resetjp_945_;
}
else
{
lean_inc(v_val_944_);
lean_dec(v___x_896_);
v___x_946_ = lean_box(0);
v_isShared_947_ = v_isSharedCheck_954_;
goto v_resetjp_945_;
}
v_resetjp_945_:
{
if (lean_obj_tag(v_val_944_) == 1)
{
lean_object* v___x_948_; lean_object* v___x_949_; lean_object* v___x_951_; 
lean_dec_ref_known(v_val_944_, 1);
v___x_948_ = lean_unsigned_to_nat(64u);
lean_inc(v_head_871_);
v___x_949_ = l_NsExport_resolveRoot(v_cx_843_, v_head_871_, v___x_948_);
lean_inc(v_self_844_);
if (v_isShared_947_ == 0)
{
lean_ctor_set(v___x_946_, 0, v_self_844_);
v___x_951_ = v___x_946_;
goto v_reusejp_950_;
}
else
{
lean_object* v_reuseFailAlloc_953_; 
v_reuseFailAlloc_953_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_953_, 0, v_self_844_);
v___x_951_ = v_reuseFailAlloc_953_;
goto v_reusejp_950_;
}
v_reusejp_950_:
{
uint8_t v___x_952_; 
v___x_952_ = l_Option_instBEq_beq___at___00Lean_PostprocessTraces_ofClass_spec__0(v___x_949_, v___x_951_);
lean_dec_ref(v___x_951_);
lean_dec(v___x_949_);
if (v___x_952_ == 0)
{
goto v___jp_899_;
}
else
{
v___y_930_ = v___x_898_;
goto v___jp_929_;
}
}
}
else
{
lean_del_object(v___x_946_);
lean_dec(v_val_944_);
v___y_930_ = v___x_898_;
goto v___jp_929_;
}
}
}
else
{
lean_dec(v___x_896_);
v___y_930_ = v___x_898_;
goto v___jp_929_;
}
}
else
{
lean_dec(v___x_896_);
lean_del_object(v___x_874_);
goto v___jp_882_;
}
v___jp_899_:
{
lean_object* v___x_900_; 
lean_inc_ref(v_env_877_);
v___x_900_ = l_Lean_Environment_find_x3f(v_env_877_, v_head_871_, v___x_898_);
if (lean_obj_tag(v___x_900_) == 1)
{
lean_object* v_val_901_; lean_object* v___x_902_; lean_object* v___x_903_; lean_object* v___x_904_; lean_object* v___x_905_; lean_object* v___x_906_; 
v_val_901_ = lean_ctor_get(v___x_900_, 0);
lean_inc(v_val_901_);
lean_dec_ref_known(v___x_900_, 1);
v___x_902_ = l_Lean_ConstantInfo_type(v_val_901_);
v___x_903_ = l_Lean_Expr_getUsedConstants(v___x_902_);
v___x_904_ = lean_array_to_list(v___x_903_);
v___x_905_ = l_List_appendTR___redArg(v___x_904_, v_tail_872_);
v___x_906_ = l_NsExport_valueOf_x3f(v_val_901_);
if (lean_obj_tag(v___x_906_) == 1)
{
lean_object* v_val_907_; lean_object* v___x_908_; lean_object* v___x_909_; lean_object* v___x_910_; lean_object* v___x_912_; 
v_val_907_ = lean_ctor_get(v___x_906_, 0);
lean_inc(v_val_907_);
lean_dec_ref_known(v___x_906_, 1);
v___x_908_ = l_Lean_Expr_getUsedConstants(v_val_907_);
v___x_909_ = lean_array_to_list(v___x_908_);
v___x_910_ = l_List_appendTR___redArg(v___x_909_, v___x_905_);
if (v_isShared_875_ == 0)
{
lean_ctor_set_tag(v___x_874_, 0);
lean_ctor_set(v___x_874_, 1, v___x_910_);
lean_ctor_set(v___x_874_, 0, v___x_881_);
v___x_912_ = v___x_874_;
goto v_reusejp_911_;
}
else
{
lean_object* v_reuseFailAlloc_916_; 
v_reuseFailAlloc_916_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_916_, 0, v___x_881_);
lean_ctor_set(v_reuseFailAlloc_916_, 1, v___x_910_);
v___x_912_ = v_reuseFailAlloc_916_;
goto v_reusejp_911_;
}
v_reusejp_911_:
{
lean_object* v___x_913_; lean_object* v___x_914_; 
v___x_913_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_913_, 0, v_fst_852_);
lean_ctor_set(v___x_913_, 1, v___x_912_);
v___x_914_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_914_, 0, v_fst_848_);
lean_ctor_set(v___x_914_, 1, v___x_913_);
v_a_845_ = v___x_914_;
goto _start;
}
}
else
{
lean_object* v___x_918_; 
lean_dec(v___x_906_);
if (v_isShared_875_ == 0)
{
lean_ctor_set_tag(v___x_874_, 0);
lean_ctor_set(v___x_874_, 1, v___x_905_);
lean_ctor_set(v___x_874_, 0, v___x_881_);
v___x_918_ = v___x_874_;
goto v_reusejp_917_;
}
else
{
lean_object* v_reuseFailAlloc_922_; 
v_reuseFailAlloc_922_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_922_, 0, v___x_881_);
lean_ctor_set(v_reuseFailAlloc_922_, 1, v___x_905_);
v___x_918_ = v_reuseFailAlloc_922_;
goto v_reusejp_917_;
}
v_reusejp_917_:
{
lean_object* v___x_919_; lean_object* v___x_920_; 
v___x_919_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_919_, 0, v_fst_852_);
lean_ctor_set(v___x_919_, 1, v___x_918_);
v___x_920_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_920_, 0, v_fst_848_);
lean_ctor_set(v___x_920_, 1, v___x_919_);
v_a_845_ = v___x_920_;
goto _start;
}
}
}
else
{
lean_object* v___x_924_; 
lean_dec(v___x_900_);
if (v_isShared_875_ == 0)
{
lean_ctor_set_tag(v___x_874_, 0);
lean_ctor_set(v___x_874_, 0, v___x_881_);
v___x_924_ = v___x_874_;
goto v_reusejp_923_;
}
else
{
lean_object* v_reuseFailAlloc_928_; 
v_reuseFailAlloc_928_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_928_, 0, v___x_881_);
lean_ctor_set(v_reuseFailAlloc_928_, 1, v_tail_872_);
v___x_924_ = v_reuseFailAlloc_928_;
goto v_reusejp_923_;
}
v_reusejp_923_:
{
lean_object* v___x_925_; lean_object* v___x_926_; 
v___x_925_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_925_, 0, v_fst_852_);
lean_ctor_set(v___x_925_, 1, v___x_924_);
v___x_926_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_926_, 0, v_fst_848_);
lean_ctor_set(v___x_926_, 1, v___x_925_);
v_a_845_ = v___x_926_;
goto _start;
}
}
}
v___jp_929_:
{
if (v___y_930_ == 0)
{
lean_object* v___x_931_; lean_object* v___x_932_; 
v___x_931_ = lean_unsigned_to_nat(64u);
lean_inc(v_head_871_);
v___x_932_ = l_NsExport_resolveRoot(v_cx_843_, v_head_871_, v___x_931_);
if (lean_obj_tag(v___x_932_) == 0)
{
goto v___jp_899_;
}
else
{
lean_object* v_val_933_; uint8_t v___x_934_; 
lean_del_object(v___x_874_);
lean_dec(v_head_871_);
v_val_933_ = lean_ctor_get(v___x_932_, 0);
lean_inc(v_val_933_);
lean_dec_ref_known(v___x_932_, 1);
v___x_934_ = lean_name_eq(v_val_933_, v_self_844_);
if (v___x_934_ == 0)
{
lean_object* v___x_935_; lean_object* v___x_936_; lean_object* v___x_937_; lean_object* v___x_938_; 
v___x_935_ = l_Std_DHashMap_Internal_Raw_u2080_insertIfNew___at___00__private_Lean_Linter_Extra_UnreachableTactic_0__Lean_Linter_Extra_UnreachableTactic_initFn_00___x40_Lean_Linter_Extra_UnreachableTactic_949854657____hygCtx___hyg_2__spec__0___redArg(v_fst_848_, v_val_933_, v___x_880_);
v___x_936_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_936_, 0, v___x_881_);
lean_ctor_set(v___x_936_, 1, v_tail_872_);
v___x_937_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_937_, 0, v_fst_852_);
lean_ctor_set(v___x_937_, 1, v___x_936_);
v___x_938_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_938_, 0, v___x_935_);
lean_ctor_set(v___x_938_, 1, v___x_937_);
v_a_845_ = v___x_938_;
goto _start;
}
else
{
lean_object* v___x_940_; lean_object* v___x_941_; lean_object* v___x_942_; 
lean_dec(v_val_933_);
v___x_940_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_940_, 0, v___x_881_);
lean_ctor_set(v___x_940_, 1, v_tail_872_);
v___x_941_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_941_, 0, v_fst_852_);
lean_ctor_set(v___x_941_, 1, v___x_940_);
v___x_942_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_942_, 0, v_fst_848_);
lean_ctor_set(v___x_942_, 1, v___x_941_);
v_a_845_ = v___x_942_;
goto _start;
}
}
}
else
{
goto v___jp_899_;
}
}
}
else
{
lean_del_object(v___x_874_);
goto v___jp_882_;
}
}
v___jp_882_:
{
lean_object* v___x_883_; lean_object* v___x_885_; 
v___x_883_ = l_Std_DHashMap_Internal_Raw_u2080_insertIfNew___at___00__private_Lean_Linter_Extra_UnreachableTactic_0__Lean_Linter_Extra_UnreachableTactic_initFn_00___x40_Lean_Linter_Extra_UnreachableTactic_949854657____hygCtx___hyg_2__spec__0___redArg(v_fst_852_, v_head_871_, v___x_880_);
if (v_isShared_860_ == 0)
{
lean_ctor_set(v___x_859_, 1, v_tail_872_);
lean_ctor_set(v___x_859_, 0, v___x_881_);
v___x_885_ = v___x_859_;
goto v_reusejp_884_;
}
else
{
lean_object* v_reuseFailAlloc_893_; 
v_reuseFailAlloc_893_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_893_, 0, v___x_881_);
lean_ctor_set(v_reuseFailAlloc_893_, 1, v_tail_872_);
v___x_885_ = v_reuseFailAlloc_893_;
goto v_reusejp_884_;
}
v_reusejp_884_:
{
lean_object* v___x_887_; 
if (v_isShared_855_ == 0)
{
lean_ctor_set(v___x_854_, 1, v___x_885_);
lean_ctor_set(v___x_854_, 0, v___x_883_);
v___x_887_ = v___x_854_;
goto v_reusejp_886_;
}
else
{
lean_object* v_reuseFailAlloc_892_; 
v_reuseFailAlloc_892_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_892_, 0, v___x_883_);
lean_ctor_set(v_reuseFailAlloc_892_, 1, v___x_885_);
v___x_887_ = v_reuseFailAlloc_892_;
goto v_reusejp_886_;
}
v_reusejp_886_:
{
lean_object* v___x_889_; 
if (v_isShared_851_ == 0)
{
lean_ctor_set(v___x_850_, 1, v___x_887_);
v___x_889_ = v___x_850_;
goto v_reusejp_888_;
}
else
{
lean_object* v_reuseFailAlloc_891_; 
v_reuseFailAlloc_891_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_891_, 0, v_fst_848_);
lean_ctor_set(v_reuseFailAlloc_891_, 1, v___x_887_);
v___x_889_ = v_reuseFailAlloc_891_;
goto v_reusejp_888_;
}
v_reusejp_888_:
{
v_a_845_ = v___x_889_;
goto _start;
}
}
}
}
}
else
{
lean_object* v___x_956_; 
lean_del_object(v___x_874_);
lean_dec(v_head_871_);
if (v_isShared_860_ == 0)
{
lean_ctor_set(v___x_859_, 1, v_tail_872_);
v___x_956_ = v___x_859_;
goto v_reusejp_955_;
}
else
{
lean_object* v_reuseFailAlloc_964_; 
v_reuseFailAlloc_964_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_964_, 0, v_fst_856_);
lean_ctor_set(v_reuseFailAlloc_964_, 1, v_tail_872_);
v___x_956_ = v_reuseFailAlloc_964_;
goto v_reusejp_955_;
}
v_reusejp_955_:
{
lean_object* v___x_958_; 
if (v_isShared_855_ == 0)
{
lean_ctor_set(v___x_854_, 1, v___x_956_);
v___x_958_ = v___x_854_;
goto v_reusejp_957_;
}
else
{
lean_object* v_reuseFailAlloc_963_; 
v_reuseFailAlloc_963_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_963_, 0, v_fst_852_);
lean_ctor_set(v_reuseFailAlloc_963_, 1, v___x_956_);
v___x_958_ = v_reuseFailAlloc_963_;
goto v_reusejp_957_;
}
v_reusejp_957_:
{
lean_object* v___x_960_; 
if (v_isShared_851_ == 0)
{
lean_ctor_set(v___x_850_, 1, v___x_958_);
v___x_960_ = v___x_850_;
goto v_reusejp_959_;
}
else
{
lean_object* v_reuseFailAlloc_962_; 
v_reuseFailAlloc_962_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_962_, 0, v_fst_848_);
lean_ctor_set(v_reuseFailAlloc_962_, 1, v___x_958_);
v___x_960_ = v_reuseFailAlloc_962_;
goto v_reusejp_959_;
}
v_reusejp_959_:
{
v_a_845_ = v___x_960_;
goto _start;
}
}
}
}
}
}
}
else
{
lean_object* v___x_967_; 
lean_dec(v_self_844_);
lean_dec_ref(v_cx_843_);
if (v_isShared_860_ == 0)
{
v___x_967_ = v___x_859_;
goto v_reusejp_966_;
}
else
{
lean_object* v_reuseFailAlloc_974_; 
v_reuseFailAlloc_974_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_974_, 0, v_fst_856_);
lean_ctor_set(v_reuseFailAlloc_974_, 1, v_snd_857_);
v___x_967_ = v_reuseFailAlloc_974_;
goto v_reusejp_966_;
}
v_reusejp_966_:
{
lean_object* v___x_969_; 
if (v_isShared_855_ == 0)
{
lean_ctor_set(v___x_854_, 1, v___x_967_);
v___x_969_ = v___x_854_;
goto v_reusejp_968_;
}
else
{
lean_object* v_reuseFailAlloc_973_; 
v_reuseFailAlloc_973_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_973_, 0, v_fst_852_);
lean_ctor_set(v_reuseFailAlloc_973_, 1, v___x_967_);
v___x_969_ = v_reuseFailAlloc_973_;
goto v_reusejp_968_;
}
v_reusejp_968_:
{
lean_object* v___x_971_; 
if (v_isShared_851_ == 0)
{
lean_ctor_set(v___x_850_, 1, v___x_969_);
v___x_971_ = v___x_850_;
goto v_reusejp_970_;
}
else
{
lean_object* v_reuseFailAlloc_972_; 
v_reuseFailAlloc_972_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_972_, 0, v_fst_848_);
lean_ctor_set(v_reuseFailAlloc_972_, 1, v___x_969_);
v___x_971_ = v_reuseFailAlloc_972_;
goto v_reusejp_970_;
}
v_reusejp_970_:
{
return v___x_971_;
}
}
}
}
}
}
}
}
}
static lean_object* _init_l_NsExport_resolveDeps___closed__0(void){
_start:
{
lean_object* v___x_980_; lean_object* v___x_981_; lean_object* v___x_982_; 
v___x_980_ = lean_box(0);
v___x_981_ = lean_unsigned_to_nat(16u);
v___x_982_ = lean_mk_array(v___x_981_, v___x_980_);
return v___x_982_;
}
}
static lean_object* _init_l_NsExport_resolveDeps___closed__1(void){
_start:
{
lean_object* v___x_983_; lean_object* v___x_984_; lean_object* v_deps_985_; 
v___x_983_ = lean_obj_once(&l_NsExport_resolveDeps___closed__0, &l_NsExport_resolveDeps___closed__0_once, _init_l_NsExport_resolveDeps___closed__0);
v___x_984_ = lean_unsigned_to_nat(0u);
v_deps_985_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_deps_985_, 0, v___x_984_);
lean_ctor_set(v_deps_985_, 1, v___x_983_);
return v_deps_985_;
}
}
LEAN_EXPORT lean_object* l_NsExport_resolveDeps(lean_object* v_cx_986_, lean_object* v_self_987_, lean_object* v_consts_988_){
_start:
{
lean_object* v_deps_989_; lean_object* v_todo_990_; lean_object* v___x_991_; lean_object* v___x_992_; lean_object* v___x_993_; lean_object* v___x_994_; lean_object* v_snd_995_; lean_object* v_fst_996_; lean_object* v_fst_997_; lean_object* v___x_999_; uint8_t v_isShared_1000_; uint8_t v_isSharedCheck_1004_; 
v_deps_989_ = lean_obj_once(&l_NsExport_resolveDeps___closed__1, &l_NsExport_resolveDeps___closed__1_once, _init_l_NsExport_resolveDeps___closed__1);
v_todo_990_ = lean_array_to_list(v_consts_988_);
v___x_991_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_991_, 0, v_deps_989_);
lean_ctor_set(v___x_991_, 1, v_todo_990_);
v___x_992_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_992_, 0, v_deps_989_);
lean_ctor_set(v___x_992_, 1, v___x_991_);
v___x_993_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_993_, 0, v_deps_989_);
lean_ctor_set(v___x_993_, 1, v___x_992_);
v___x_994_ = l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg(v_cx_986_, v_self_987_, v___x_993_);
v_snd_995_ = lean_ctor_get(v___x_994_, 1);
lean_inc(v_snd_995_);
v_fst_996_ = lean_ctor_get(v___x_994_, 0);
lean_inc(v_fst_996_);
lean_dec_ref(v___x_994_);
v_fst_997_ = lean_ctor_get(v_snd_995_, 0);
v_isSharedCheck_1004_ = !lean_is_exclusive(v_snd_995_);
if (v_isSharedCheck_1004_ == 0)
{
lean_object* v_unused_1005_; 
v_unused_1005_ = lean_ctor_get(v_snd_995_, 1);
lean_dec(v_unused_1005_);
v___x_999_ = v_snd_995_;
v_isShared_1000_ = v_isSharedCheck_1004_;
goto v_resetjp_998_;
}
else
{
lean_inc(v_fst_997_);
lean_dec(v_snd_995_);
v___x_999_ = lean_box(0);
v_isShared_1000_ = v_isSharedCheck_1004_;
goto v_resetjp_998_;
}
v_resetjp_998_:
{
lean_object* v___x_1002_; 
if (v_isShared_1000_ == 0)
{
lean_ctor_set(v___x_999_, 1, v_fst_997_);
lean_ctor_set(v___x_999_, 0, v_fst_996_);
v___x_1002_ = v___x_999_;
goto v_reusejp_1001_;
}
else
{
lean_object* v_reuseFailAlloc_1003_; 
v_reuseFailAlloc_1003_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1003_, 0, v_fst_996_);
lean_ctor_set(v_reuseFailAlloc_1003_, 1, v_fst_997_);
v___x_1002_ = v_reuseFailAlloc_1003_;
goto v_reusejp_1001_;
}
v_reusejp_1001_:
{
return v___x_1002_;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1(lean_object* v_cx_1006_, lean_object* v_self_1007_, lean_object* v_inst_1008_, lean_object* v_a_1009_){
_start:
{
lean_object* v___x_1010_; 
v___x_1010_ = l___private_Init_While_0__repeatM_erased___at___00NsExport_resolveDeps_spec__1___redArg(v_cx_1006_, v_self_1007_, v_a_1009_);
return v___x_1010_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_sortedNames_spec__0(size_t v_sz_1011_, size_t v_i_1012_, lean_object* v_bs_1013_){
_start:
{
uint8_t v___x_1014_; 
v___x_1014_ = lean_usize_dec_lt(v_i_1012_, v_sz_1011_);
if (v___x_1014_ == 0)
{
return v_bs_1013_;
}
else
{
lean_object* v_v_1015_; lean_object* v___x_1016_; lean_object* v_bs_x27_1017_; uint8_t v___x_1018_; lean_object* v___x_1019_; size_t v___x_1020_; size_t v___x_1021_; lean_object* v___x_1022_; 
v_v_1015_ = lean_array_uget(v_bs_1013_, v_i_1012_);
v___x_1016_ = lean_unsigned_to_nat(0u);
v_bs_x27_1017_ = lean_array_uset(v_bs_1013_, v_i_1012_, v___x_1016_);
v___x_1018_ = 0;
v___x_1019_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_v_1015_, v___x_1018_);
v___x_1020_ = ((size_t)1ULL);
v___x_1021_ = lean_usize_add(v_i_1012_, v___x_1020_);
v___x_1022_ = lean_array_uset(v_bs_x27_1017_, v_i_1012_, v___x_1019_);
v_i_1012_ = v___x_1021_;
v_bs_1013_ = v___x_1022_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_sortedNames_spec__0___boxed(lean_object* v_sz_1024_, lean_object* v_i_1025_, lean_object* v_bs_1026_){
_start:
{
size_t v_sz_boxed_1027_; size_t v_i_boxed_1028_; lean_object* v_res_1029_; 
v_sz_boxed_1027_ = lean_unbox_usize(v_sz_1024_);
lean_dec(v_sz_1024_);
v_i_boxed_1028_ = lean_unbox_usize(v_i_1025_);
lean_dec(v_i_1025_);
v_res_1029_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_sortedNames_spec__0(v_sz_boxed_1027_, v_i_boxed_1028_, v_bs_1026_);
return v_res_1029_;
}
}
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_foldlM___at___00NsExport_sortedNames_spec__1(lean_object* v_x_1030_, lean_object* v_x_1031_){
_start:
{
if (lean_obj_tag(v_x_1031_) == 0)
{
return v_x_1030_;
}
else
{
lean_object* v_key_1032_; lean_object* v_tail_1033_; lean_object* v___x_1034_; 
v_key_1032_ = lean_ctor_get(v_x_1031_, 0);
lean_inc(v_key_1032_);
v_tail_1033_ = lean_ctor_get(v_x_1031_, 2);
lean_inc(v_tail_1033_);
lean_dec_ref_known(v_x_1031_, 3);
v___x_1034_ = lean_array_push(v_x_1030_, v_key_1032_);
v_x_1030_ = v___x_1034_;
v_x_1031_ = v_tail_1033_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_sortedNames_spec__2(lean_object* v_as_1036_, size_t v_i_1037_, size_t v_stop_1038_, lean_object* v_b_1039_){
_start:
{
uint8_t v___x_1040_; 
v___x_1040_ = lean_usize_dec_eq(v_i_1037_, v_stop_1038_);
if (v___x_1040_ == 0)
{
lean_object* v___x_1041_; lean_object* v___x_1042_; size_t v___x_1043_; size_t v___x_1044_; 
v___x_1041_ = lean_array_uget_borrowed(v_as_1036_, v_i_1037_);
lean_inc(v___x_1041_);
v___x_1042_ = l_Std_DHashMap_Internal_AssocList_foldlM___at___00NsExport_sortedNames_spec__1(v_b_1039_, v___x_1041_);
v___x_1043_ = ((size_t)1ULL);
v___x_1044_ = lean_usize_add(v_i_1037_, v___x_1043_);
v_i_1037_ = v___x_1044_;
v_b_1039_ = v___x_1042_;
goto _start;
}
else
{
return v_b_1039_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_sortedNames_spec__2___boxed(lean_object* v_as_1046_, lean_object* v_i_1047_, lean_object* v_stop_1048_, lean_object* v_b_1049_){
_start:
{
size_t v_i_boxed_1050_; size_t v_stop_boxed_1051_; lean_object* v_res_1052_; 
v_i_boxed_1050_ = lean_unbox_usize(v_i_1047_);
lean_dec(v_i_1047_);
v_stop_boxed_1051_ = lean_unbox_usize(v_stop_1048_);
lean_dec(v_stop_1048_);
v_res_1052_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_sortedNames_spec__2(v_as_1046_, v_i_boxed_1050_, v_stop_boxed_1051_, v_b_1049_);
lean_dec_ref(v_as_1046_);
return v_res_1052_;
}
}
LEAN_EXPORT lean_object* l_NsExport_sortedNames(lean_object* v_s_1053_){
_start:
{
lean_object* v___y_1055_; lean_object* v___y_1056_; lean_object* v___y_1057_; lean_object* v___y_1058_; lean_object* v___y_1063_; lean_object* v_size_1073_; lean_object* v_buckets_1074_; lean_object* v___x_1075_; lean_object* v___x_1076_; lean_object* v___x_1077_; uint8_t v___x_1078_; 
v_size_1073_ = lean_ctor_get(v_s_1053_, 0);
v_buckets_1074_ = lean_ctor_get(v_s_1053_, 1);
v___x_1075_ = lean_mk_empty_array_with_capacity(v_size_1073_);
v___x_1076_ = lean_unsigned_to_nat(0u);
v___x_1077_ = lean_array_get_size(v_buckets_1074_);
v___x_1078_ = lean_nat_dec_lt(v___x_1076_, v___x_1077_);
if (v___x_1078_ == 0)
{
v___y_1063_ = v___x_1075_;
goto v___jp_1062_;
}
else
{
uint8_t v___x_1079_; 
v___x_1079_ = lean_nat_dec_le(v___x_1077_, v___x_1077_);
if (v___x_1079_ == 0)
{
if (v___x_1078_ == 0)
{
v___y_1063_ = v___x_1075_;
goto v___jp_1062_;
}
else
{
size_t v___x_1080_; size_t v___x_1081_; lean_object* v___x_1082_; 
v___x_1080_ = ((size_t)0ULL);
v___x_1081_ = lean_usize_of_nat(v___x_1077_);
v___x_1082_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_sortedNames_spec__2(v_buckets_1074_, v___x_1080_, v___x_1081_, v___x_1075_);
v___y_1063_ = v___x_1082_;
goto v___jp_1062_;
}
}
else
{
size_t v___x_1083_; size_t v___x_1084_; lean_object* v___x_1085_; 
v___x_1083_ = ((size_t)0ULL);
v___x_1084_ = lean_usize_of_nat(v___x_1077_);
v___x_1085_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_sortedNames_spec__2(v_buckets_1074_, v___x_1083_, v___x_1084_, v___x_1075_);
v___y_1063_ = v___x_1085_;
goto v___jp_1062_;
}
}
v___jp_1054_:
{
uint8_t v___x_1059_; 
v___x_1059_ = lean_nat_dec_le(v___y_1058_, v___y_1055_);
if (v___x_1059_ == 0)
{
lean_object* v___x_1060_; 
lean_dec(v___y_1055_);
lean_inc(v___y_1058_);
v___x_1060_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00__private_Lean_Elab_DocString_Builtin_0__Lean_Doc_validateCat_spec__3___redArg(v___y_1056_, v___y_1057_, v___y_1058_, v___y_1058_);
lean_dec(v___y_1058_);
lean_dec(v___y_1056_);
return v___x_1060_;
}
else
{
lean_object* v___x_1061_; 
v___x_1061_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00__private_Lean_Elab_DocString_Builtin_0__Lean_Doc_validateCat_spec__3___redArg(v___y_1056_, v___y_1057_, v___y_1058_, v___y_1055_);
lean_dec(v___y_1055_);
lean_dec(v___y_1056_);
return v___x_1061_;
}
}
v___jp_1062_:
{
size_t v_sz_1064_; size_t v___x_1065_; lean_object* v___x_1066_; lean_object* v___x_1067_; lean_object* v___x_1068_; uint8_t v___x_1069_; 
v_sz_1064_ = lean_array_size(v___y_1063_);
v___x_1065_ = ((size_t)0ULL);
v___x_1066_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_sortedNames_spec__0(v_sz_1064_, v___x_1065_, v___y_1063_);
v___x_1067_ = lean_array_get_size(v___x_1066_);
v___x_1068_ = lean_unsigned_to_nat(0u);
v___x_1069_ = lean_nat_dec_eq(v___x_1067_, v___x_1068_);
if (v___x_1069_ == 0)
{
lean_object* v___x_1070_; lean_object* v___x_1071_; uint8_t v___x_1072_; 
v___x_1070_ = lean_unsigned_to_nat(1u);
v___x_1071_ = lean_nat_sub(v___x_1067_, v___x_1070_);
v___x_1072_ = lean_nat_dec_le(v___x_1068_, v___x_1071_);
if (v___x_1072_ == 0)
{
lean_inc(v___x_1071_);
v___y_1055_ = v___x_1071_;
v___y_1056_ = v___x_1067_;
v___y_1057_ = v___x_1066_;
v___y_1058_ = v___x_1071_;
goto v___jp_1054_;
}
else
{
v___y_1055_ = v___x_1071_;
v___y_1056_ = v___x_1067_;
v___y_1057_ = v___x_1066_;
v___y_1058_ = v___x_1068_;
goto v___jp_1054_;
}
}
else
{
return v___x_1066_;
}
}
}
}
LEAN_EXPORT lean_object* l_NsExport_sortedNames___boxed(lean_object* v_s_1086_){
_start:
{
lean_object* v_res_1087_; 
v_res_1087_ = l_NsExport_sortedNames(v_s_1086_);
lean_dec_ref(v_s_1086_);
return v_res_1087_;
}
}
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg(lean_object* v_constName_1088_, lean_object* v___y_1089_){
_start:
{
lean_object* v___x_1091_; lean_object* v_env_1092_; lean_object* v___x_1093_; uint8_t v___x_1094_; lean_object* v_privateEnv_1095_; lean_object* v___x_1096_; lean_object* v___x_1097_; lean_object* v___x_1098_; lean_object* v_s_1099_; lean_object* v___x_1100_; lean_object* v___x_1101_; lean_object* v___x_1102_; lean_object* v___x_1103_; 
v___x_1091_ = lean_st_ref_get(v___y_1089_);
v_env_1092_ = lean_ctor_get(v___x_1091_, 0);
lean_inc_ref_n(v_env_1092_, 2);
lean_dec(v___x_1091_);
v___x_1093_ = l___private_Lean_Util_CollectAxioms_0__Lean_instInhabitedExportedAxiomsState;
v___x_1094_ = 0;
v_privateEnv_1095_ = l_Lean_Environment_setExporting(v_env_1092_, v___x_1094_);
v___x_1096_ = l___private_Lean_Util_CollectAxioms_0__Lean_exportedAxiomsExt;
v___x_1097_ = lean_box(2);
v___x_1098_ = lean_box(0);
v_s_1099_ = l_Lean_PersistentEnvExtension_getState___redArg(v___x_1093_, v___x_1096_, v_env_1092_, v___x_1097_, v___x_1098_);
v___x_1100_ = lean_alloc_closure((void*)(l___private_Lean_Util_CollectAxioms_0__Lean_ExportedAxiomsState_find_x3f___boxed), 3, 1);
lean_closure_set(v___x_1100_, 0, v_s_1099_);
v___x_1101_ = lean_alloc_closure((void*)(l___private_Lean_Util_CollectAxioms_0__Lean_CollectAxioms_collectAndGet___boxed), 4, 2);
lean_closure_set(v___x_1101_, 0, v___x_1100_);
lean_closure_set(v___x_1101_, 1, v_constName_1088_);
v___x_1102_ = l___private_Lean_Util_CollectAxioms_0__Lean_CollectAxioms_runM___redArg(v_privateEnv_1095_, v___x_1101_);
v___x_1103_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1103_, 0, v___x_1102_);
return v___x_1103_;
}
}
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg___boxed(lean_object* v_constName_1104_, lean_object* v___y_1105_, lean_object* v___y_1106_){
_start:
{
lean_object* v_res_1107_; 
v_res_1107_ = l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg(v_constName_1104_, v___y_1105_);
lean_dec(v___y_1105_);
return v_res_1107_;
}
}
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18(lean_object* v_constName_1108_, lean_object* v___y_1109_, lean_object* v___y_1110_){
_start:
{
lean_object* v___x_1112_; 
v___x_1112_ = l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg(v_constName_1108_, v___y_1110_);
return v___x_1112_;
}
}
LEAN_EXPORT lean_object* l_Lean_collectAxioms___at___00NsExport_main_spec__18___boxed(lean_object* v_constName_1113_, lean_object* v___y_1114_, lean_object* v___y_1115_, lean_object* v___y_1116_){
_start:
{
lean_object* v_res_1117_; 
v_res_1117_ = l_Lean_collectAxioms___at___00NsExport_main_spec__18(v_constName_1113_, v___y_1114_, v___y_1115_);
lean_dec(v___y_1115_);
lean_dec_ref(v___y_1114_);
return v_res_1117_;
}
}
LEAN_EXPORT lean_object* l_NsExport_main___lam__0(){
_start:
{
lean_object* v___x_1119_; lean_object* v___x_1120_; 
v___x_1119_ = lean_io_mono_ms_now();
v___x_1120_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1120_, 0, v___x_1119_);
return v___x_1120_;
}
}
LEAN_EXPORT lean_object* l_NsExport_main___lam__0___boxed(lean_object* v___y_1121_){
_start:
{
lean_object* v_res_1122_; 
v_res_1122_ = l_NsExport_main___lam__0();
return v_res_1122_;
}
}
LEAN_EXPORT uint8_t l_NsExport_main___lam__1(lean_object* v_a_1123_, uint8_t v___x_1124_, uint8_t v___x_1125_, lean_object* v___x_1126_, lean_object* v_n_1127_){
_start:
{
lean_object* v___x_1128_; 
v___x_1128_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_1123_, v_n_1127_);
if (lean_obj_tag(v___x_1128_) == 0)
{
return v___x_1124_;
}
else
{
lean_object* v_val_1129_; lean_object* v___x_1130_; lean_object* v___x_1131_; uint8_t v___x_1132_; 
v_val_1129_ = lean_ctor_get(v___x_1128_, 0);
lean_inc(v_val_1129_);
lean_dec_ref_known(v___x_1128_, 1);
v___x_1130_ = lean_box(v___x_1125_);
v___x_1131_ = lean_array_get(v___x_1130_, v___x_1126_, v_val_1129_);
lean_dec(v_val_1129_);
lean_dec(v___x_1130_);
v___x_1132_ = lean_unbox(v___x_1131_);
lean_dec(v___x_1131_);
return v___x_1132_;
}
}
}
LEAN_EXPORT lean_object* l_NsExport_main___lam__1___boxed(lean_object* v_a_1133_, lean_object* v___x_1134_, lean_object* v___x_1135_, lean_object* v___x_1136_, lean_object* v_n_1137_){
_start:
{
uint8_t v___x_72411__boxed_1138_; uint8_t v___x_72412__boxed_1139_; uint8_t v_res_1140_; lean_object* v_r_1141_; 
v___x_72411__boxed_1138_ = lean_unbox(v___x_1134_);
v___x_72412__boxed_1139_ = lean_unbox(v___x_1135_);
v_res_1140_ = l_NsExport_main___lam__1(v_a_1133_, v___x_72411__boxed_1138_, v___x_72412__boxed_1139_, v___x_1136_, v_n_1137_);
lean_dec(v_n_1137_);
lean_dec_ref(v___x_1136_);
lean_dec_ref(v_a_1133_);
v_r_1141_ = lean_box(v_res_1140_);
return v_r_1141_;
}
}
LEAN_EXPORT lean_object* l_panic___at___00Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11_spec__13(lean_object* v_msg_1142_){
_start:
{
lean_object* v___x_1143_; lean_object* v___x_1144_; 
v___x_1143_ = lean_box(0);
v___x_1144_ = lean_panic_fn_borrowed(v___x_1143_, v_msg_1142_);
return v___x_1144_;
}
}
static lean_object* _init_l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__3(void){
_start:
{
lean_object* v___x_1148_; lean_object* v___x_1149_; lean_object* v___x_1150_; lean_object* v___x_1151_; lean_object* v___x_1152_; lean_object* v___x_1153_; 
v___x_1148_ = ((lean_object*)(l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__2));
v___x_1149_ = lean_unsigned_to_nat(11u);
v___x_1150_ = lean_unsigned_to_nat(163u);
v___x_1151_ = ((lean_object*)(l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__1));
v___x_1152_ = ((lean_object*)(l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__0));
v___x_1153_ = l_mkPanicMessageWithDecl(v___x_1152_, v___x_1151_, v___x_1150_, v___x_1149_, v___x_1148_);
return v___x_1153_;
}
}
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11(lean_object* v_a_1154_, lean_object* v_x_1155_){
_start:
{
if (lean_obj_tag(v_x_1155_) == 0)
{
lean_object* v___x_1156_; lean_object* v___x_1157_; 
v___x_1156_ = lean_obj_once(&l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__3, &l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__3_once, _init_l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___closed__3);
v___x_1157_ = l_panic___at___00Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11_spec__13(v___x_1156_);
return v___x_1157_;
}
else
{
lean_object* v_key_1158_; lean_object* v_value_1159_; lean_object* v_tail_1160_; uint8_t v___x_1161_; 
v_key_1158_ = lean_ctor_get(v_x_1155_, 0);
v_value_1159_ = lean_ctor_get(v_x_1155_, 1);
v_tail_1160_ = lean_ctor_get(v_x_1155_, 2);
v___x_1161_ = lean_name_eq(v_key_1158_, v_a_1154_);
if (v___x_1161_ == 0)
{
v_x_1155_ = v_tail_1160_;
goto _start;
}
else
{
lean_inc(v_value_1159_);
return v_value_1159_;
}
}
}
}
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11___boxed(lean_object* v_a_1163_, lean_object* v_x_1164_){
_start:
{
lean_object* v_res_1165_; 
v_res_1165_ = l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11(v_a_1163_, v_x_1164_);
lean_dec(v_x_1164_);
lean_dec(v_a_1163_);
return v_res_1165_;
}
}
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(lean_object* v_m_1166_, lean_object* v_a_1167_){
_start:
{
lean_object* v_buckets_1168_; lean_object* v___x_1169_; uint64_t v___y_1171_; 
v_buckets_1168_ = lean_ctor_get(v_m_1166_, 1);
v___x_1169_ = lean_array_get_size(v_buckets_1168_);
if (lean_obj_tag(v_a_1167_) == 0)
{
uint64_t v___x_1185_; 
v___x_1185_ = 1723ULL;
v___y_1171_ = v___x_1185_;
goto v___jp_1170_;
}
else
{
uint64_t v_hash_1186_; 
v_hash_1186_ = lean_ctor_get_uint64(v_a_1167_, sizeof(void*)*2);
v___y_1171_ = v_hash_1186_;
goto v___jp_1170_;
}
v___jp_1170_:
{
uint64_t v___x_1172_; uint64_t v___x_1173_; uint64_t v_fold_1174_; uint64_t v___x_1175_; uint64_t v___x_1176_; uint64_t v___x_1177_; size_t v___x_1178_; size_t v___x_1179_; size_t v___x_1180_; size_t v___x_1181_; size_t v___x_1182_; lean_object* v___x_1183_; lean_object* v___x_1184_; 
v___x_1172_ = 32ULL;
v___x_1173_ = lean_uint64_shift_right(v___y_1171_, v___x_1172_);
v_fold_1174_ = lean_uint64_xor(v___y_1171_, v___x_1173_);
v___x_1175_ = 16ULL;
v___x_1176_ = lean_uint64_shift_right(v_fold_1174_, v___x_1175_);
v___x_1177_ = lean_uint64_xor(v_fold_1174_, v___x_1176_);
v___x_1178_ = lean_uint64_to_usize(v___x_1177_);
v___x_1179_ = lean_usize_of_nat(v___x_1169_);
v___x_1180_ = ((size_t)1ULL);
v___x_1181_ = lean_usize_sub(v___x_1179_, v___x_1180_);
v___x_1182_ = lean_usize_land(v___x_1178_, v___x_1181_);
v___x_1183_ = lean_array_uget_borrowed(v_buckets_1168_, v___x_1182_);
v___x_1184_ = l_Std_DHashMap_Internal_AssocList_get_x21___at___00Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9_spec__11(v_a_1167_, v___x_1183_);
return v___x_1184_;
}
}
}
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9___boxed(lean_object* v_m_1187_, lean_object* v_a_1188_){
_start:
{
lean_object* v_res_1189_; 
v_res_1189_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_m_1187_, v_a_1188_);
lean_dec(v_a_1188_);
lean_dec_ref(v_m_1187_);
return v_res_1189_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13(lean_object* v_a_1192_, lean_object* v___x_1193_, lean_object* v_as_1194_, size_t v_sz_1195_, size_t v_i_1196_, lean_object* v_b_1197_){
_start:
{
lean_object* v_a_1200_; uint8_t v___x_1204_; 
v___x_1204_ = lean_usize_dec_lt(v_i_1196_, v_sz_1195_);
if (v___x_1204_ == 0)
{
lean_object* v___x_1205_; 
v___x_1205_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1205_, 0, v_b_1197_);
return v___x_1205_;
}
else
{
lean_object* v_a_1206_; lean_object* v_snd_1207_; lean_object* v_snd_1208_; lean_object* v_snd_1209_; lean_object* v_snd_1210_; lean_object* v_snd_1211_; lean_object* v_snd_1212_; lean_object* v_snd_1213_; lean_object* v_snd_1214_; lean_object* v_fst_1215_; lean_object* v___x_1217_; uint8_t v_isShared_1218_; uint8_t v_isSharedCheck_1391_; 
v_a_1206_ = lean_array_uget(v_as_1194_, v_i_1196_);
v_snd_1207_ = lean_ctor_get(v_b_1197_, 1);
lean_inc(v_snd_1207_);
v_snd_1208_ = lean_ctor_get(v_snd_1207_, 1);
lean_inc(v_snd_1208_);
v_snd_1209_ = lean_ctor_get(v_snd_1208_, 1);
lean_inc(v_snd_1209_);
v_snd_1210_ = lean_ctor_get(v_snd_1209_, 1);
lean_inc(v_snd_1210_);
v_snd_1211_ = lean_ctor_get(v_snd_1210_, 1);
lean_inc(v_snd_1211_);
v_snd_1212_ = lean_ctor_get(v_snd_1211_, 1);
lean_inc(v_snd_1212_);
v_snd_1213_ = lean_ctor_get(v_snd_1212_, 1);
lean_inc(v_snd_1213_);
v_snd_1214_ = lean_ctor_get(v_snd_1213_, 1);
lean_inc(v_snd_1214_);
v_fst_1215_ = lean_ctor_get(v_a_1206_, 0);
v_isSharedCheck_1391_ = !lean_is_exclusive(v_a_1206_);
if (v_isSharedCheck_1391_ == 0)
{
lean_object* v_unused_1392_; 
v_unused_1392_ = lean_ctor_get(v_a_1206_, 1);
lean_dec(v_unused_1392_);
v___x_1217_ = v_a_1206_;
v_isShared_1218_ = v_isSharedCheck_1391_;
goto v_resetjp_1216_;
}
else
{
lean_inc(v_fst_1215_);
lean_dec(v_a_1206_);
v___x_1217_ = lean_box(0);
v_isShared_1218_ = v_isSharedCheck_1391_;
goto v_resetjp_1216_;
}
v_resetjp_1216_:
{
lean_object* v_fst_1219_; lean_object* v___x_1221_; uint8_t v_isShared_1222_; uint8_t v_isSharedCheck_1389_; 
v_fst_1219_ = lean_ctor_get(v_b_1197_, 0);
v_isSharedCheck_1389_ = !lean_is_exclusive(v_b_1197_);
if (v_isSharedCheck_1389_ == 0)
{
lean_object* v_unused_1390_; 
v_unused_1390_ = lean_ctor_get(v_b_1197_, 1);
lean_dec(v_unused_1390_);
v___x_1221_ = v_b_1197_;
v_isShared_1222_ = v_isSharedCheck_1389_;
goto v_resetjp_1220_;
}
else
{
lean_inc(v_fst_1219_);
lean_dec(v_b_1197_);
v___x_1221_ = lean_box(0);
v_isShared_1222_ = v_isSharedCheck_1389_;
goto v_resetjp_1220_;
}
v_resetjp_1220_:
{
lean_object* v_fst_1223_; lean_object* v___x_1225_; uint8_t v_isShared_1226_; uint8_t v_isSharedCheck_1387_; 
v_fst_1223_ = lean_ctor_get(v_snd_1207_, 0);
v_isSharedCheck_1387_ = !lean_is_exclusive(v_snd_1207_);
if (v_isSharedCheck_1387_ == 0)
{
lean_object* v_unused_1388_; 
v_unused_1388_ = lean_ctor_get(v_snd_1207_, 1);
lean_dec(v_unused_1388_);
v___x_1225_ = v_snd_1207_;
v_isShared_1226_ = v_isSharedCheck_1387_;
goto v_resetjp_1224_;
}
else
{
lean_inc(v_fst_1223_);
lean_dec(v_snd_1207_);
v___x_1225_ = lean_box(0);
v_isShared_1226_ = v_isSharedCheck_1387_;
goto v_resetjp_1224_;
}
v_resetjp_1224_:
{
lean_object* v_fst_1227_; lean_object* v___x_1229_; uint8_t v_isShared_1230_; uint8_t v_isSharedCheck_1385_; 
v_fst_1227_ = lean_ctor_get(v_snd_1208_, 0);
v_isSharedCheck_1385_ = !lean_is_exclusive(v_snd_1208_);
if (v_isSharedCheck_1385_ == 0)
{
lean_object* v_unused_1386_; 
v_unused_1386_ = lean_ctor_get(v_snd_1208_, 1);
lean_dec(v_unused_1386_);
v___x_1229_ = v_snd_1208_;
v_isShared_1230_ = v_isSharedCheck_1385_;
goto v_resetjp_1228_;
}
else
{
lean_inc(v_fst_1227_);
lean_dec(v_snd_1208_);
v___x_1229_ = lean_box(0);
v_isShared_1230_ = v_isSharedCheck_1385_;
goto v_resetjp_1228_;
}
v_resetjp_1228_:
{
lean_object* v_fst_1231_; lean_object* v___x_1233_; uint8_t v_isShared_1234_; uint8_t v_isSharedCheck_1383_; 
v_fst_1231_ = lean_ctor_get(v_snd_1209_, 0);
v_isSharedCheck_1383_ = !lean_is_exclusive(v_snd_1209_);
if (v_isSharedCheck_1383_ == 0)
{
lean_object* v_unused_1384_; 
v_unused_1384_ = lean_ctor_get(v_snd_1209_, 1);
lean_dec(v_unused_1384_);
v___x_1233_ = v_snd_1209_;
v_isShared_1234_ = v_isSharedCheck_1383_;
goto v_resetjp_1232_;
}
else
{
lean_inc(v_fst_1231_);
lean_dec(v_snd_1209_);
v___x_1233_ = lean_box(0);
v_isShared_1234_ = v_isSharedCheck_1383_;
goto v_resetjp_1232_;
}
v_resetjp_1232_:
{
lean_object* v_fst_1235_; lean_object* v___x_1237_; uint8_t v_isShared_1238_; uint8_t v_isSharedCheck_1381_; 
v_fst_1235_ = lean_ctor_get(v_snd_1210_, 0);
v_isSharedCheck_1381_ = !lean_is_exclusive(v_snd_1210_);
if (v_isSharedCheck_1381_ == 0)
{
lean_object* v_unused_1382_; 
v_unused_1382_ = lean_ctor_get(v_snd_1210_, 1);
lean_dec(v_unused_1382_);
v___x_1237_ = v_snd_1210_;
v_isShared_1238_ = v_isSharedCheck_1381_;
goto v_resetjp_1236_;
}
else
{
lean_inc(v_fst_1235_);
lean_dec(v_snd_1210_);
v___x_1237_ = lean_box(0);
v_isShared_1238_ = v_isSharedCheck_1381_;
goto v_resetjp_1236_;
}
v_resetjp_1236_:
{
lean_object* v_fst_1239_; lean_object* v___x_1241_; uint8_t v_isShared_1242_; uint8_t v_isSharedCheck_1379_; 
v_fst_1239_ = lean_ctor_get(v_snd_1211_, 0);
v_isSharedCheck_1379_ = !lean_is_exclusive(v_snd_1211_);
if (v_isSharedCheck_1379_ == 0)
{
lean_object* v_unused_1380_; 
v_unused_1380_ = lean_ctor_get(v_snd_1211_, 1);
lean_dec(v_unused_1380_);
v___x_1241_ = v_snd_1211_;
v_isShared_1242_ = v_isSharedCheck_1379_;
goto v_resetjp_1240_;
}
else
{
lean_inc(v_fst_1239_);
lean_dec(v_snd_1211_);
v___x_1241_ = lean_box(0);
v_isShared_1242_ = v_isSharedCheck_1379_;
goto v_resetjp_1240_;
}
v_resetjp_1240_:
{
lean_object* v_fst_1243_; lean_object* v___x_1245_; uint8_t v_isShared_1246_; uint8_t v_isSharedCheck_1377_; 
v_fst_1243_ = lean_ctor_get(v_snd_1212_, 0);
v_isSharedCheck_1377_ = !lean_is_exclusive(v_snd_1212_);
if (v_isSharedCheck_1377_ == 0)
{
lean_object* v_unused_1378_; 
v_unused_1378_ = lean_ctor_get(v_snd_1212_, 1);
lean_dec(v_unused_1378_);
v___x_1245_ = v_snd_1212_;
v_isShared_1246_ = v_isSharedCheck_1377_;
goto v_resetjp_1244_;
}
else
{
lean_inc(v_fst_1243_);
lean_dec(v_snd_1212_);
v___x_1245_ = lean_box(0);
v_isShared_1246_ = v_isSharedCheck_1377_;
goto v_resetjp_1244_;
}
v_resetjp_1244_:
{
lean_object* v_fst_1247_; lean_object* v___x_1249_; uint8_t v_isShared_1250_; uint8_t v_isSharedCheck_1375_; 
v_fst_1247_ = lean_ctor_get(v_snd_1213_, 0);
v_isSharedCheck_1375_ = !lean_is_exclusive(v_snd_1213_);
if (v_isSharedCheck_1375_ == 0)
{
lean_object* v_unused_1376_; 
v_unused_1376_ = lean_ctor_get(v_snd_1213_, 1);
lean_dec(v_unused_1376_);
v___x_1249_ = v_snd_1213_;
v_isShared_1250_ = v_isSharedCheck_1375_;
goto v_resetjp_1248_;
}
else
{
lean_inc(v_fst_1247_);
lean_dec(v_snd_1213_);
v___x_1249_ = lean_box(0);
v_isShared_1250_ = v_isSharedCheck_1375_;
goto v_resetjp_1248_;
}
v_resetjp_1248_:
{
lean_object* v_fst_1251_; lean_object* v_snd_1252_; lean_object* v___x_1254_; uint8_t v_isShared_1255_; uint8_t v_isSharedCheck_1374_; 
v_fst_1251_ = lean_ctor_get(v_snd_1214_, 0);
v_snd_1252_ = lean_ctor_get(v_snd_1214_, 1);
v_isSharedCheck_1374_ = !lean_is_exclusive(v_snd_1214_);
if (v_isSharedCheck_1374_ == 0)
{
v___x_1254_ = v_snd_1214_;
v_isShared_1255_ = v_isSharedCheck_1374_;
goto v_resetjp_1253_;
}
else
{
lean_inc(v_snd_1252_);
lean_inc(v_fst_1251_);
lean_dec(v_snd_1214_);
v___x_1254_ = lean_box(0);
v_isShared_1255_ = v_isSharedCheck_1374_;
goto v_resetjp_1253_;
}
v_resetjp_1253_:
{
lean_object* v___x_1256_; uint8_t v___x_1257_; lean_object* v___x_1289_; 
v___x_1256_ = lean_unsigned_to_nat(1u);
v___x_1257_ = 0;
v___x_1289_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_a_1192_, v_fst_1215_);
switch(lean_obj_tag(v___x_1289_))
{
case 0:
{
lean_object* v___x_1290_; lean_object* v___x_1292_; 
lean_del_object(v___x_1254_);
lean_del_object(v___x_1249_);
lean_del_object(v___x_1245_);
lean_del_object(v___x_1241_);
lean_del_object(v___x_1237_);
lean_del_object(v___x_1233_);
lean_del_object(v___x_1229_);
lean_del_object(v___x_1225_);
lean_del_object(v___x_1221_);
lean_dec(v_fst_1215_);
v___x_1290_ = lean_nat_add(v_fst_1227_, v___x_1256_);
lean_dec(v_fst_1227_);
if (v_isShared_1218_ == 0)
{
lean_ctor_set(v___x_1217_, 1, v_snd_1252_);
lean_ctor_set(v___x_1217_, 0, v_fst_1251_);
v___x_1292_ = v___x_1217_;
goto v_reusejp_1291_;
}
else
{
lean_object* v_reuseFailAlloc_1301_; 
v_reuseFailAlloc_1301_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1301_, 0, v_fst_1251_);
lean_ctor_set(v_reuseFailAlloc_1301_, 1, v_snd_1252_);
v___x_1292_ = v_reuseFailAlloc_1301_;
goto v_reusejp_1291_;
}
v_reusejp_1291_:
{
lean_object* v___x_1293_; lean_object* v___x_1294_; lean_object* v___x_1295_; lean_object* v___x_1296_; lean_object* v___x_1297_; lean_object* v___x_1298_; lean_object* v___x_1299_; lean_object* v___x_1300_; 
v___x_1293_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1293_, 0, v_fst_1247_);
lean_ctor_set(v___x_1293_, 1, v___x_1292_);
v___x_1294_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1294_, 0, v_fst_1243_);
lean_ctor_set(v___x_1294_, 1, v___x_1293_);
v___x_1295_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1295_, 0, v_fst_1239_);
lean_ctor_set(v___x_1295_, 1, v___x_1294_);
v___x_1296_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1296_, 0, v_fst_1235_);
lean_ctor_set(v___x_1296_, 1, v___x_1295_);
v___x_1297_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1297_, 0, v_fst_1231_);
lean_ctor_set(v___x_1297_, 1, v___x_1296_);
v___x_1298_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1298_, 0, v___x_1290_);
lean_ctor_set(v___x_1298_, 1, v___x_1297_);
v___x_1299_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1299_, 0, v_fst_1223_);
lean_ctor_set(v___x_1299_, 1, v___x_1298_);
v___x_1300_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1300_, 0, v_fst_1219_);
lean_ctor_set(v___x_1300_, 1, v___x_1299_);
v_a_1200_ = v___x_1300_;
goto v___jp_1199_;
}
}
case 4:
{
lean_object* v___x_1302_; lean_object* v___x_1304_; 
lean_del_object(v___x_1254_);
lean_del_object(v___x_1249_);
lean_del_object(v___x_1245_);
lean_del_object(v___x_1241_);
lean_del_object(v___x_1237_);
lean_del_object(v___x_1233_);
lean_del_object(v___x_1229_);
lean_del_object(v___x_1225_);
lean_del_object(v___x_1221_);
lean_dec(v_fst_1215_);
v___x_1302_ = lean_nat_add(v_fst_1243_, v___x_1256_);
lean_dec(v_fst_1243_);
if (v_isShared_1218_ == 0)
{
lean_ctor_set(v___x_1217_, 1, v_snd_1252_);
lean_ctor_set(v___x_1217_, 0, v_fst_1251_);
v___x_1304_ = v___x_1217_;
goto v_reusejp_1303_;
}
else
{
lean_object* v_reuseFailAlloc_1313_; 
v_reuseFailAlloc_1313_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1313_, 0, v_fst_1251_);
lean_ctor_set(v_reuseFailAlloc_1313_, 1, v_snd_1252_);
v___x_1304_ = v_reuseFailAlloc_1313_;
goto v_reusejp_1303_;
}
v_reusejp_1303_:
{
lean_object* v___x_1305_; lean_object* v___x_1306_; lean_object* v___x_1307_; lean_object* v___x_1308_; lean_object* v___x_1309_; lean_object* v___x_1310_; lean_object* v___x_1311_; lean_object* v___x_1312_; 
v___x_1305_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1305_, 0, v_fst_1247_);
lean_ctor_set(v___x_1305_, 1, v___x_1304_);
v___x_1306_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1306_, 0, v___x_1302_);
lean_ctor_set(v___x_1306_, 1, v___x_1305_);
v___x_1307_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1307_, 0, v_fst_1239_);
lean_ctor_set(v___x_1307_, 1, v___x_1306_);
v___x_1308_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1308_, 0, v_fst_1235_);
lean_ctor_set(v___x_1308_, 1, v___x_1307_);
v___x_1309_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1309_, 0, v_fst_1231_);
lean_ctor_set(v___x_1309_, 1, v___x_1308_);
v___x_1310_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1310_, 0, v_fst_1227_);
lean_ctor_set(v___x_1310_, 1, v___x_1309_);
v___x_1311_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1311_, 0, v_fst_1223_);
lean_ctor_set(v___x_1311_, 1, v___x_1310_);
v___x_1312_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1312_, 0, v_fst_1219_);
lean_ctor_set(v___x_1312_, 1, v___x_1311_);
v_a_1200_ = v___x_1312_;
goto v___jp_1199_;
}
}
case 5:
{
lean_object* v___x_1314_; lean_object* v___x_1316_; 
lean_del_object(v___x_1254_);
lean_del_object(v___x_1249_);
lean_del_object(v___x_1245_);
lean_del_object(v___x_1241_);
lean_del_object(v___x_1237_);
lean_del_object(v___x_1233_);
lean_del_object(v___x_1229_);
lean_del_object(v___x_1225_);
lean_del_object(v___x_1221_);
lean_dec(v_fst_1215_);
v___x_1314_ = lean_nat_add(v_fst_1251_, v___x_1256_);
lean_dec(v_fst_1251_);
if (v_isShared_1218_ == 0)
{
lean_ctor_set(v___x_1217_, 1, v_snd_1252_);
lean_ctor_set(v___x_1217_, 0, v___x_1314_);
v___x_1316_ = v___x_1217_;
goto v_reusejp_1315_;
}
else
{
lean_object* v_reuseFailAlloc_1325_; 
v_reuseFailAlloc_1325_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1325_, 0, v___x_1314_);
lean_ctor_set(v_reuseFailAlloc_1325_, 1, v_snd_1252_);
v___x_1316_ = v_reuseFailAlloc_1325_;
goto v_reusejp_1315_;
}
v_reusejp_1315_:
{
lean_object* v___x_1317_; lean_object* v___x_1318_; lean_object* v___x_1319_; lean_object* v___x_1320_; lean_object* v___x_1321_; lean_object* v___x_1322_; lean_object* v___x_1323_; lean_object* v___x_1324_; 
v___x_1317_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1317_, 0, v_fst_1247_);
lean_ctor_set(v___x_1317_, 1, v___x_1316_);
v___x_1318_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1318_, 0, v_fst_1243_);
lean_ctor_set(v___x_1318_, 1, v___x_1317_);
v___x_1319_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1319_, 0, v_fst_1239_);
lean_ctor_set(v___x_1319_, 1, v___x_1318_);
v___x_1320_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1320_, 0, v_fst_1235_);
lean_ctor_set(v___x_1320_, 1, v___x_1319_);
v___x_1321_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1321_, 0, v_fst_1231_);
lean_ctor_set(v___x_1321_, 1, v___x_1320_);
v___x_1322_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1322_, 0, v_fst_1227_);
lean_ctor_set(v___x_1322_, 1, v___x_1321_);
v___x_1323_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1323_, 0, v_fst_1223_);
lean_ctor_set(v___x_1323_, 1, v___x_1322_);
v___x_1324_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1324_, 0, v_fst_1219_);
lean_ctor_set(v___x_1324_, 1, v___x_1323_);
v_a_1200_ = v___x_1324_;
goto v___jp_1199_;
}
}
case 6:
{
lean_del_object(v___x_1217_);
goto v___jp_1258_;
}
default: 
{
lean_object* v___x_1326_; lean_object* v___x_1327_; 
v___x_1326_ = lean_unsigned_to_nat(64u);
lean_inc(v_fst_1215_);
v___x_1327_ = l_NsExport_resolveRoot(v___x_1193_, v_fst_1215_, v___x_1326_);
if (lean_obj_tag(v___x_1327_) == 0)
{
lean_dec(v___x_1289_);
lean_del_object(v___x_1217_);
goto v___jp_1258_;
}
else
{
lean_del_object(v___x_1254_);
lean_del_object(v___x_1249_);
lean_del_object(v___x_1245_);
lean_del_object(v___x_1241_);
lean_del_object(v___x_1237_);
lean_del_object(v___x_1233_);
lean_del_object(v___x_1229_);
lean_del_object(v___x_1225_);
lean_del_object(v___x_1221_);
switch(lean_obj_tag(v___x_1289_))
{
case 1:
{
lean_object* v_val_1328_; lean_object* v___x_1329_; lean_object* v___x_1330_; lean_object* v___x_1331_; lean_object* v___x_1332_; lean_object* v___x_1333_; lean_object* v___x_1335_; 
lean_dec_ref_known(v___x_1289_, 1);
v_val_1328_ = lean_ctor_get(v___x_1327_, 0);
lean_inc(v_val_1328_);
lean_dec_ref_known(v___x_1327_, 1);
v___x_1329_ = lean_nat_add(v_fst_1231_, v___x_1256_);
lean_dec(v_fst_1231_);
v___x_1330_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___closed__0));
v___x_1331_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(v_fst_1219_, v_val_1328_, v___x_1330_);
v___x_1332_ = lean_array_push(v___x_1331_, v_fst_1215_);
v___x_1333_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_fst_1219_, v_val_1328_, v___x_1332_);
if (v_isShared_1218_ == 0)
{
lean_ctor_set(v___x_1217_, 1, v_snd_1252_);
lean_ctor_set(v___x_1217_, 0, v_fst_1251_);
v___x_1335_ = v___x_1217_;
goto v_reusejp_1334_;
}
else
{
lean_object* v_reuseFailAlloc_1344_; 
v_reuseFailAlloc_1344_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1344_, 0, v_fst_1251_);
lean_ctor_set(v_reuseFailAlloc_1344_, 1, v_snd_1252_);
v___x_1335_ = v_reuseFailAlloc_1344_;
goto v_reusejp_1334_;
}
v_reusejp_1334_:
{
lean_object* v___x_1336_; lean_object* v___x_1337_; lean_object* v___x_1338_; lean_object* v___x_1339_; lean_object* v___x_1340_; lean_object* v___x_1341_; lean_object* v___x_1342_; lean_object* v___x_1343_; 
v___x_1336_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1336_, 0, v_fst_1247_);
lean_ctor_set(v___x_1336_, 1, v___x_1335_);
v___x_1337_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1337_, 0, v_fst_1243_);
lean_ctor_set(v___x_1337_, 1, v___x_1336_);
v___x_1338_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1338_, 0, v_fst_1239_);
lean_ctor_set(v___x_1338_, 1, v___x_1337_);
v___x_1339_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1339_, 0, v_fst_1235_);
lean_ctor_set(v___x_1339_, 1, v___x_1338_);
v___x_1340_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1340_, 0, v___x_1329_);
lean_ctor_set(v___x_1340_, 1, v___x_1339_);
v___x_1341_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1341_, 0, v_fst_1227_);
lean_ctor_set(v___x_1341_, 1, v___x_1340_);
v___x_1342_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1342_, 0, v_fst_1223_);
lean_ctor_set(v___x_1342_, 1, v___x_1341_);
v___x_1343_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1343_, 0, v___x_1333_);
lean_ctor_set(v___x_1343_, 1, v___x_1342_);
v_a_1200_ = v___x_1343_;
goto v___jp_1199_;
}
}
case 2:
{
lean_object* v_val_1345_; lean_object* v___x_1346_; lean_object* v___x_1347_; lean_object* v___x_1348_; lean_object* v___x_1349_; lean_object* v___x_1350_; lean_object* v___x_1352_; 
lean_dec_ref_known(v___x_1289_, 1);
v_val_1345_ = lean_ctor_get(v___x_1327_, 0);
lean_inc(v_val_1345_);
lean_dec_ref_known(v___x_1327_, 1);
v___x_1346_ = lean_nat_add(v_fst_1235_, v___x_1256_);
lean_dec(v_fst_1235_);
v___x_1347_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___closed__0));
v___x_1348_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(v_fst_1223_, v_val_1345_, v___x_1347_);
v___x_1349_ = lean_array_push(v___x_1348_, v_fst_1215_);
v___x_1350_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_fst_1223_, v_val_1345_, v___x_1349_);
if (v_isShared_1218_ == 0)
{
lean_ctor_set(v___x_1217_, 1, v_snd_1252_);
lean_ctor_set(v___x_1217_, 0, v_fst_1251_);
v___x_1352_ = v___x_1217_;
goto v_reusejp_1351_;
}
else
{
lean_object* v_reuseFailAlloc_1361_; 
v_reuseFailAlloc_1361_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1361_, 0, v_fst_1251_);
lean_ctor_set(v_reuseFailAlloc_1361_, 1, v_snd_1252_);
v___x_1352_ = v_reuseFailAlloc_1361_;
goto v_reusejp_1351_;
}
v_reusejp_1351_:
{
lean_object* v___x_1353_; lean_object* v___x_1354_; lean_object* v___x_1355_; lean_object* v___x_1356_; lean_object* v___x_1357_; lean_object* v___x_1358_; lean_object* v___x_1359_; lean_object* v___x_1360_; 
v___x_1353_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1353_, 0, v_fst_1247_);
lean_ctor_set(v___x_1353_, 1, v___x_1352_);
v___x_1354_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1354_, 0, v_fst_1243_);
lean_ctor_set(v___x_1354_, 1, v___x_1353_);
v___x_1355_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1355_, 0, v_fst_1239_);
lean_ctor_set(v___x_1355_, 1, v___x_1354_);
v___x_1356_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1356_, 0, v___x_1346_);
lean_ctor_set(v___x_1356_, 1, v___x_1355_);
v___x_1357_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1357_, 0, v_fst_1231_);
lean_ctor_set(v___x_1357_, 1, v___x_1356_);
v___x_1358_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1358_, 0, v_fst_1227_);
lean_ctor_set(v___x_1358_, 1, v___x_1357_);
v___x_1359_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1359_, 0, v___x_1350_);
lean_ctor_set(v___x_1359_, 1, v___x_1358_);
v___x_1360_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1360_, 0, v_fst_1219_);
lean_ctor_set(v___x_1360_, 1, v___x_1359_);
v_a_1200_ = v___x_1360_;
goto v___jp_1199_;
}
}
default: 
{
lean_object* v___x_1362_; lean_object* v___x_1364_; 
lean_dec_ref_known(v___x_1327_, 1);
lean_dec(v___x_1289_);
lean_dec(v_fst_1215_);
v___x_1362_ = lean_nat_add(v_fst_1239_, v___x_1256_);
lean_dec(v_fst_1239_);
if (v_isShared_1218_ == 0)
{
lean_ctor_set(v___x_1217_, 1, v_snd_1252_);
lean_ctor_set(v___x_1217_, 0, v_fst_1251_);
v___x_1364_ = v___x_1217_;
goto v_reusejp_1363_;
}
else
{
lean_object* v_reuseFailAlloc_1373_; 
v_reuseFailAlloc_1373_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1373_, 0, v_fst_1251_);
lean_ctor_set(v_reuseFailAlloc_1373_, 1, v_snd_1252_);
v___x_1364_ = v_reuseFailAlloc_1373_;
goto v_reusejp_1363_;
}
v_reusejp_1363_:
{
lean_object* v___x_1365_; lean_object* v___x_1366_; lean_object* v___x_1367_; lean_object* v___x_1368_; lean_object* v___x_1369_; lean_object* v___x_1370_; lean_object* v___x_1371_; lean_object* v___x_1372_; 
v___x_1365_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1365_, 0, v_fst_1247_);
lean_ctor_set(v___x_1365_, 1, v___x_1364_);
v___x_1366_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1366_, 0, v_fst_1243_);
lean_ctor_set(v___x_1366_, 1, v___x_1365_);
v___x_1367_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1367_, 0, v___x_1362_);
lean_ctor_set(v___x_1367_, 1, v___x_1366_);
v___x_1368_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1368_, 0, v_fst_1235_);
lean_ctor_set(v___x_1368_, 1, v___x_1367_);
v___x_1369_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1369_, 0, v_fst_1231_);
lean_ctor_set(v___x_1369_, 1, v___x_1368_);
v___x_1370_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1370_, 0, v_fst_1227_);
lean_ctor_set(v___x_1370_, 1, v___x_1369_);
v___x_1371_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1371_, 0, v_fst_1223_);
lean_ctor_set(v___x_1371_, 1, v___x_1370_);
v___x_1372_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1372_, 0, v_fst_1219_);
lean_ctor_set(v___x_1372_, 1, v___x_1371_);
v_a_1200_ = v___x_1372_;
goto v___jp_1199_;
}
}
}
}
}
}
v___jp_1258_:
{
lean_object* v___x_1259_; lean_object* v___x_1260_; lean_object* v___x_1261_; lean_object* v___x_1263_; 
v___x_1259_ = lean_nat_add(v_fst_1247_, v___x_1256_);
lean_dec(v_fst_1247_);
v___x_1260_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_1215_, v___x_1257_);
v___x_1261_ = lean_array_push(v_snd_1252_, v___x_1260_);
if (v_isShared_1255_ == 0)
{
lean_ctor_set(v___x_1254_, 1, v___x_1261_);
v___x_1263_ = v___x_1254_;
goto v_reusejp_1262_;
}
else
{
lean_object* v_reuseFailAlloc_1288_; 
v_reuseFailAlloc_1288_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1288_, 0, v_fst_1251_);
lean_ctor_set(v_reuseFailAlloc_1288_, 1, v___x_1261_);
v___x_1263_ = v_reuseFailAlloc_1288_;
goto v_reusejp_1262_;
}
v_reusejp_1262_:
{
lean_object* v___x_1265_; 
if (v_isShared_1250_ == 0)
{
lean_ctor_set(v___x_1249_, 1, v___x_1263_);
lean_ctor_set(v___x_1249_, 0, v___x_1259_);
v___x_1265_ = v___x_1249_;
goto v_reusejp_1264_;
}
else
{
lean_object* v_reuseFailAlloc_1287_; 
v_reuseFailAlloc_1287_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1287_, 0, v___x_1259_);
lean_ctor_set(v_reuseFailAlloc_1287_, 1, v___x_1263_);
v___x_1265_ = v_reuseFailAlloc_1287_;
goto v_reusejp_1264_;
}
v_reusejp_1264_:
{
lean_object* v___x_1267_; 
if (v_isShared_1246_ == 0)
{
lean_ctor_set(v___x_1245_, 1, v___x_1265_);
v___x_1267_ = v___x_1245_;
goto v_reusejp_1266_;
}
else
{
lean_object* v_reuseFailAlloc_1286_; 
v_reuseFailAlloc_1286_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1286_, 0, v_fst_1243_);
lean_ctor_set(v_reuseFailAlloc_1286_, 1, v___x_1265_);
v___x_1267_ = v_reuseFailAlloc_1286_;
goto v_reusejp_1266_;
}
v_reusejp_1266_:
{
lean_object* v___x_1269_; 
if (v_isShared_1242_ == 0)
{
lean_ctor_set(v___x_1241_, 1, v___x_1267_);
v___x_1269_ = v___x_1241_;
goto v_reusejp_1268_;
}
else
{
lean_object* v_reuseFailAlloc_1285_; 
v_reuseFailAlloc_1285_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1285_, 0, v_fst_1239_);
lean_ctor_set(v_reuseFailAlloc_1285_, 1, v___x_1267_);
v___x_1269_ = v_reuseFailAlloc_1285_;
goto v_reusejp_1268_;
}
v_reusejp_1268_:
{
lean_object* v___x_1271_; 
if (v_isShared_1238_ == 0)
{
lean_ctor_set(v___x_1237_, 1, v___x_1269_);
v___x_1271_ = v___x_1237_;
goto v_reusejp_1270_;
}
else
{
lean_object* v_reuseFailAlloc_1284_; 
v_reuseFailAlloc_1284_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1284_, 0, v_fst_1235_);
lean_ctor_set(v_reuseFailAlloc_1284_, 1, v___x_1269_);
v___x_1271_ = v_reuseFailAlloc_1284_;
goto v_reusejp_1270_;
}
v_reusejp_1270_:
{
lean_object* v___x_1273_; 
if (v_isShared_1234_ == 0)
{
lean_ctor_set(v___x_1233_, 1, v___x_1271_);
v___x_1273_ = v___x_1233_;
goto v_reusejp_1272_;
}
else
{
lean_object* v_reuseFailAlloc_1283_; 
v_reuseFailAlloc_1283_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1283_, 0, v_fst_1231_);
lean_ctor_set(v_reuseFailAlloc_1283_, 1, v___x_1271_);
v___x_1273_ = v_reuseFailAlloc_1283_;
goto v_reusejp_1272_;
}
v_reusejp_1272_:
{
lean_object* v___x_1275_; 
if (v_isShared_1230_ == 0)
{
lean_ctor_set(v___x_1229_, 1, v___x_1273_);
v___x_1275_ = v___x_1229_;
goto v_reusejp_1274_;
}
else
{
lean_object* v_reuseFailAlloc_1282_; 
v_reuseFailAlloc_1282_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1282_, 0, v_fst_1227_);
lean_ctor_set(v_reuseFailAlloc_1282_, 1, v___x_1273_);
v___x_1275_ = v_reuseFailAlloc_1282_;
goto v_reusejp_1274_;
}
v_reusejp_1274_:
{
lean_object* v___x_1277_; 
if (v_isShared_1226_ == 0)
{
lean_ctor_set(v___x_1225_, 1, v___x_1275_);
v___x_1277_ = v___x_1225_;
goto v_reusejp_1276_;
}
else
{
lean_object* v_reuseFailAlloc_1281_; 
v_reuseFailAlloc_1281_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1281_, 0, v_fst_1223_);
lean_ctor_set(v_reuseFailAlloc_1281_, 1, v___x_1275_);
v___x_1277_ = v_reuseFailAlloc_1281_;
goto v_reusejp_1276_;
}
v_reusejp_1276_:
{
lean_object* v___x_1279_; 
if (v_isShared_1222_ == 0)
{
lean_ctor_set(v___x_1221_, 1, v___x_1277_);
v___x_1279_ = v___x_1221_;
goto v_reusejp_1278_;
}
else
{
lean_object* v_reuseFailAlloc_1280_; 
v_reuseFailAlloc_1280_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1280_, 0, v_fst_1219_);
lean_ctor_set(v_reuseFailAlloc_1280_, 1, v___x_1277_);
v___x_1279_ = v_reuseFailAlloc_1280_;
goto v_reusejp_1278_;
}
v_reusejp_1278_:
{
v_a_1200_ = v___x_1279_;
goto v___jp_1199_;
}
}
}
}
}
}
}
}
}
}
}
}
}
}
}
}
}
}
}
}
}
v___jp_1199_:
{
size_t v___x_1201_; size_t v___x_1202_; 
v___x_1201_ = ((size_t)1ULL);
v___x_1202_ = lean_usize_add(v_i_1196_, v___x_1201_);
v_i_1196_ = v___x_1202_;
v_b_1197_ = v_a_1200_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___boxed(lean_object* v_a_1393_, lean_object* v___x_1394_, lean_object* v_as_1395_, lean_object* v_sz_1396_, lean_object* v_i_1397_, lean_object* v_b_1398_, lean_object* v___y_1399_){
_start:
{
size_t v_sz_boxed_1400_; size_t v_i_boxed_1401_; lean_object* v_res_1402_; 
v_sz_boxed_1400_ = lean_unbox_usize(v_sz_1396_);
lean_dec(v_sz_1396_);
v_i_boxed_1401_ = lean_unbox_usize(v_i_1397_);
lean_dec(v_i_1397_);
v_res_1402_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13(v_a_1393_, v___x_1394_, v_as_1395_, v_sz_boxed_1400_, v_i_boxed_1401_, v_b_1398_);
lean_dec_ref(v_as_1395_);
lean_dec_ref(v___x_1394_);
lean_dec_ref(v_a_1393_);
return v_res_1402_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__0(size_t v_sz_1403_, size_t v_i_1404_, lean_object* v_bs_1405_){
_start:
{
uint8_t v___x_1406_; 
v___x_1406_ = lean_usize_dec_lt(v_i_1404_, v_sz_1403_);
if (v___x_1406_ == 0)
{
return v_bs_1405_;
}
else
{
lean_object* v_v_1407_; lean_object* v___x_1408_; lean_object* v_bs_x27_1409_; lean_object* v___x_1410_; size_t v___x_1411_; size_t v___x_1412_; lean_object* v___x_1413_; 
v_v_1407_ = lean_array_uget(v_bs_1405_, v_i_1404_);
v___x_1408_ = lean_unsigned_to_nat(0u);
v_bs_x27_1409_ = lean_array_uset(v_bs_1405_, v_i_1404_, v___x_1408_);
v___x_1410_ = l_String_toName(v_v_1407_);
v___x_1411_ = ((size_t)1ULL);
v___x_1412_ = lean_usize_add(v_i_1404_, v___x_1411_);
v___x_1413_ = lean_array_uset(v_bs_x27_1409_, v_i_1404_, v___x_1410_);
v_i_1404_ = v___x_1412_;
v_bs_1405_ = v___x_1413_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__0___boxed(lean_object* v_sz_1415_, lean_object* v_i_1416_, lean_object* v_bs_1417_){
_start:
{
size_t v_sz_boxed_1418_; size_t v_i_boxed_1419_; lean_object* v_res_1420_; 
v_sz_boxed_1418_ = lean_unbox_usize(v_sz_1415_);
lean_dec(v_sz_1415_);
v_i_boxed_1419_ = lean_unbox_usize(v_i_1416_);
lean_dec(v_i_1416_);
v_res_1420_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__0(v_sz_boxed_1418_, v_i_boxed_1419_, v_bs_1417_);
return v_res_1420_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg(lean_object* v_a_1421_, lean_object* v___x_1422_, lean_object* v_as_x27_1423_, lean_object* v_b_1424_){
_start:
{
if (lean_obj_tag(v_as_x27_1423_) == 0)
{
lean_object* v___x_1426_; 
v___x_1426_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1426_, 0, v_b_1424_);
return v___x_1426_;
}
else
{
lean_object* v_head_1427_; lean_object* v_tail_1428_; lean_object* v_fst_1429_; lean_object* v___x_1430_; 
v_head_1427_ = lean_ctor_get(v_as_x27_1423_, 0);
v_tail_1428_ = lean_ctor_get(v_as_x27_1423_, 1);
v_fst_1429_ = lean_ctor_get(v_head_1427_, 0);
v___x_1430_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_1421_, v_fst_1429_);
if (lean_obj_tag(v___x_1430_) == 0)
{
v_as_x27_1423_ = v_tail_1428_;
goto _start;
}
else
{
lean_object* v_val_1432_; uint8_t v___x_1433_; lean_object* v___x_1434_; lean_object* v___x_1435_; uint8_t v___x_1436_; 
v_val_1432_ = lean_ctor_get(v___x_1430_, 0);
lean_inc(v_val_1432_);
lean_dec_ref_known(v___x_1430_, 1);
v___x_1433_ = 0;
v___x_1434_ = lean_box(v___x_1433_);
v___x_1435_ = lean_array_get(v___x_1434_, v___x_1422_, v_val_1432_);
lean_dec(v_val_1432_);
lean_dec(v___x_1434_);
v___x_1436_ = lean_unbox(v___x_1435_);
lean_dec(v___x_1435_);
if (v___x_1436_ == 0)
{
v_as_x27_1423_ = v_tail_1428_;
goto _start;
}
else
{
lean_object* v___x_1438_; 
lean_inc(v_head_1427_);
v___x_1438_ = lean_array_push(v_b_1424_, v_head_1427_);
v_as_x27_1423_ = v_tail_1428_;
v_b_1424_ = v___x_1438_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg___boxed(lean_object* v_a_1440_, lean_object* v___x_1441_, lean_object* v_as_x27_1442_, lean_object* v_b_1443_, lean_object* v___y_1444_){
_start:
{
lean_object* v_res_1445_; 
v_res_1445_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg(v_a_1440_, v___x_1441_, v_as_x27_1442_, v_b_1443_);
lean_dec(v_as_x27_1442_);
lean_dec_ref(v___x_1441_);
lean_dec_ref(v_a_1440_);
return v_res_1445_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3___redArg(lean_object* v_a_1446_, lean_object* v___x_1447_, lean_object* v_as_1448_, lean_object* v_as_x27_1449_, lean_object* v_b_1450_){
_start:
{
if (lean_obj_tag(v_as_x27_1449_) == 0)
{
lean_object* v___x_1452_; 
v___x_1452_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1452_, 0, v_b_1450_);
return v___x_1452_;
}
else
{
lean_object* v_head_1453_; lean_object* v_tail_1454_; lean_object* v_fst_1455_; lean_object* v___x_1456_; 
v_head_1453_ = lean_ctor_get(v_as_x27_1449_, 0);
v_tail_1454_ = lean_ctor_get(v_as_x27_1449_, 1);
v_fst_1455_ = lean_ctor_get(v_head_1453_, 0);
v___x_1456_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_1446_, v_fst_1455_);
if (lean_obj_tag(v___x_1456_) == 0)
{
lean_object* v___x_1457_; 
v___x_1457_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg(v_a_1446_, v___x_1447_, v_tail_1454_, v_b_1450_);
return v___x_1457_;
}
else
{
lean_object* v_val_1458_; uint8_t v___x_1459_; lean_object* v___x_1460_; lean_object* v___x_1461_; uint8_t v___x_1462_; 
v_val_1458_ = lean_ctor_get(v___x_1456_, 0);
lean_inc(v_val_1458_);
lean_dec_ref_known(v___x_1456_, 1);
v___x_1459_ = 0;
v___x_1460_ = lean_box(v___x_1459_);
v___x_1461_ = lean_array_get(v___x_1460_, v___x_1447_, v_val_1458_);
lean_dec(v_val_1458_);
lean_dec(v___x_1460_);
v___x_1462_ = lean_unbox(v___x_1461_);
lean_dec(v___x_1461_);
if (v___x_1462_ == 0)
{
lean_object* v___x_1463_; 
v___x_1463_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg(v_a_1446_, v___x_1447_, v_tail_1454_, v_b_1450_);
return v___x_1463_;
}
else
{
lean_object* v___x_1464_; lean_object* v___x_1465_; 
lean_inc(v_head_1453_);
v___x_1464_ = lean_array_push(v_b_1450_, v_head_1453_);
v___x_1465_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg(v_a_1446_, v___x_1447_, v_tail_1454_, v___x_1464_);
return v___x_1465_;
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3___redArg___boxed(lean_object* v_a_1466_, lean_object* v___x_1467_, lean_object* v_as_1468_, lean_object* v_as_x27_1469_, lean_object* v_b_1470_, lean_object* v___y_1471_){
_start:
{
lean_object* v_res_1472_; 
v_res_1472_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__3___redArg(v_a_1466_, v___x_1467_, v_as_1468_, v_as_x27_1469_, v_b_1470_);
lean_dec(v_as_x27_1469_);
lean_dec(v_as_1468_);
lean_dec_ref(v___x_1467_);
lean_dec_ref(v_a_1466_);
return v_res_1472_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00__private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2_spec__2(size_t v_sz_1473_, size_t v_i_1474_, lean_object* v_bs_1475_){
_start:
{
uint8_t v___x_1476_; 
v___x_1476_ = lean_usize_dec_lt(v_i_1474_, v_sz_1473_);
if (v___x_1476_ == 0)
{
return v_bs_1475_;
}
else
{
lean_object* v_v_1477_; lean_object* v___x_1478_; lean_object* v_bs_x27_1479_; lean_object* v___x_1480_; lean_object* v___x_1481_; uint8_t v___x_1482_; size_t v___x_1483_; size_t v___x_1484_; lean_object* v___x_1485_; lean_object* v___x_1486_; 
v_v_1477_ = lean_array_uget(v_bs_1475_, v_i_1474_);
v___x_1478_ = lean_unsigned_to_nat(0u);
v_bs_x27_1479_ = lean_array_uset(v_bs_1475_, v_i_1474_, v___x_1478_);
v___x_1480_ = ((lean_object*)(l_NsExport_projectRoots));
v___x_1481_ = l_Lean_Name_getRoot(v_v_1477_);
lean_dec(v_v_1477_);
v___x_1482_ = l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(v___x_1481_, v___x_1480_);
lean_dec(v___x_1481_);
v___x_1483_ = ((size_t)1ULL);
v___x_1484_ = lean_usize_add(v_i_1474_, v___x_1483_);
v___x_1485_ = lean_box(v___x_1482_);
v___x_1486_ = lean_array_uset(v_bs_x27_1479_, v_i_1474_, v___x_1485_);
v_i_1474_ = v___x_1484_;
v_bs_1475_ = v___x_1486_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00__private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2_spec__2___boxed(lean_object* v_sz_1488_, lean_object* v_i_1489_, lean_object* v_bs_1490_){
_start:
{
size_t v_sz_boxed_1491_; size_t v_i_boxed_1492_; lean_object* v_res_1493_; 
v_sz_boxed_1491_ = lean_unbox_usize(v_sz_1488_);
lean_dec(v_sz_1488_);
v_i_boxed_1492_ = lean_unbox_usize(v_i_1489_);
lean_dec(v_i_1489_);
v_res_1493_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00__private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2_spec__2(v_sz_boxed_1491_, v_i_boxed_1492_, v_bs_1490_);
return v_res_1493_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2(size_t v_sz_1494_, size_t v_i_1495_, lean_object* v_bs_1496_){
_start:
{
uint8_t v___x_1497_; 
v___x_1497_ = lean_usize_dec_lt(v_i_1495_, v_sz_1494_);
if (v___x_1497_ == 0)
{
return v_bs_1496_;
}
else
{
lean_object* v_v_1498_; lean_object* v___x_1499_; lean_object* v_bs_x27_1500_; lean_object* v___x_1501_; lean_object* v___x_1502_; uint8_t v___x_1503_; size_t v___x_1504_; size_t v___x_1505_; lean_object* v___x_1506_; lean_object* v___x_1507_; lean_object* v___x_1508_; 
v_v_1498_ = lean_array_uget(v_bs_1496_, v_i_1495_);
v___x_1499_ = lean_unsigned_to_nat(0u);
v_bs_x27_1500_ = lean_array_uset(v_bs_1496_, v_i_1495_, v___x_1499_);
v___x_1501_ = ((lean_object*)(l_NsExport_projectRoots));
v___x_1502_ = l_Lean_Name_getRoot(v_v_1498_);
lean_dec(v_v_1498_);
v___x_1503_ = l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(v___x_1502_, v___x_1501_);
lean_dec(v___x_1502_);
v___x_1504_ = ((size_t)1ULL);
v___x_1505_ = lean_usize_add(v_i_1495_, v___x_1504_);
v___x_1506_ = lean_box(v___x_1503_);
v___x_1507_ = lean_array_uset(v_bs_x27_1500_, v_i_1495_, v___x_1506_);
v___x_1508_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00__private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2_spec__2(v_sz_1494_, v___x_1505_, v___x_1507_);
return v___x_1508_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2___boxed(lean_object* v_sz_1509_, lean_object* v_i_1510_, lean_object* v_bs_1511_){
_start:
{
size_t v_sz_boxed_1512_; size_t v_i_boxed_1513_; lean_object* v_res_1514_; 
v_sz_boxed_1512_ = lean_unbox_usize(v_sz_1509_);
lean_dec(v_sz_1509_);
v_i_boxed_1513_ = lean_unbox_usize(v_i_1510_);
lean_dec(v_i_1510_);
v_res_1514_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2(v_sz_boxed_1512_, v_i_boxed_1513_, v_bs_1511_);
return v_res_1514_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___redArg(lean_object* v_hi_1515_, lean_object* v_pivot_1516_, lean_object* v_as_1517_, lean_object* v_i_1518_, lean_object* v_k_1519_){
_start:
{
uint8_t v___x_1520_; 
v___x_1520_ = lean_nat_dec_lt(v_k_1519_, v_hi_1515_);
if (v___x_1520_ == 0)
{
lean_object* v___x_1521_; lean_object* v___x_1522_; 
lean_dec(v_k_1519_);
lean_dec_ref(v_pivot_1516_);
v___x_1521_ = lean_array_fswap(v_as_1517_, v_i_1518_, v_hi_1515_);
v___x_1522_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1522_, 0, v_i_1518_);
lean_ctor_set(v___x_1522_, 1, v___x_1521_);
return v___x_1522_;
}
else
{
lean_object* v___x_1523_; lean_object* v_fst_1524_; lean_object* v_fst_1525_; lean_object* v___x_1526_; lean_object* v___x_1527_; uint8_t v___x_1528_; 
v___x_1523_ = lean_array_fget_borrowed(v_as_1517_, v_k_1519_);
v_fst_1524_ = lean_ctor_get(v___x_1523_, 0);
v_fst_1525_ = lean_ctor_get(v_pivot_1516_, 0);
lean_inc(v_fst_1524_);
v___x_1526_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_1524_, v___x_1520_);
lean_inc(v_fst_1525_);
v___x_1527_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_1525_, v___x_1520_);
v___x_1528_ = lean_string_dec_lt(v___x_1526_, v___x_1527_);
lean_dec_ref(v___x_1527_);
lean_dec_ref(v___x_1526_);
if (v___x_1528_ == 0)
{
lean_object* v___x_1529_; lean_object* v___x_1530_; 
v___x_1529_ = lean_unsigned_to_nat(1u);
v___x_1530_ = lean_nat_add(v_k_1519_, v___x_1529_);
lean_dec(v_k_1519_);
v_k_1519_ = v___x_1530_;
goto _start;
}
else
{
lean_object* v___x_1532_; lean_object* v___x_1533_; lean_object* v___x_1534_; lean_object* v___x_1535_; 
v___x_1532_ = lean_array_fswap(v_as_1517_, v_i_1518_, v_k_1519_);
v___x_1533_ = lean_unsigned_to_nat(1u);
v___x_1534_ = lean_nat_add(v_i_1518_, v___x_1533_);
lean_dec(v_i_1518_);
v___x_1535_ = lean_nat_add(v_k_1519_, v___x_1533_);
lean_dec(v_k_1519_);
v_as_1517_ = v___x_1532_;
v_i_1518_ = v___x_1534_;
v_k_1519_ = v___x_1535_;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___redArg___boxed(lean_object* v_hi_1537_, lean_object* v_pivot_1538_, lean_object* v_as_1539_, lean_object* v_i_1540_, lean_object* v_k_1541_){
_start:
{
lean_object* v_res_1542_; 
v_res_1542_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___redArg(v_hi_1537_, v_pivot_1538_, v_as_1539_, v_i_1540_, v_k_1541_);
lean_dec(v_hi_1537_);
return v_res_1542_;
}
}
LEAN_EXPORT uint8_t l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0(uint8_t v___x_1543_, lean_object* v_a_1544_, lean_object* v_b_1545_){
_start:
{
lean_object* v_fst_1546_; lean_object* v_fst_1547_; lean_object* v___x_1548_; lean_object* v___x_1549_; uint8_t v___x_1550_; 
v_fst_1546_ = lean_ctor_get(v_a_1544_, 0);
lean_inc(v_fst_1546_);
lean_dec_ref(v_a_1544_);
v_fst_1547_ = lean_ctor_get(v_b_1545_, 0);
lean_inc(v_fst_1547_);
lean_dec_ref(v_b_1545_);
v___x_1548_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_1546_, v___x_1543_);
v___x_1549_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_1547_, v___x_1543_);
v___x_1550_ = lean_string_dec_lt(v___x_1548_, v___x_1549_);
lean_dec_ref(v___x_1549_);
lean_dec_ref(v___x_1548_);
return v___x_1550_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0___boxed(lean_object* v___x_1551_, lean_object* v_a_1552_, lean_object* v_b_1553_){
_start:
{
uint8_t v___x_73044__boxed_1554_; uint8_t v_res_1555_; lean_object* v_r_1556_; 
v___x_73044__boxed_1554_ = lean_unbox(v___x_1551_);
v_res_1555_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0(v___x_73044__boxed_1554_, v_a_1552_, v_b_1553_);
v_r_1556_ = lean_box(v_res_1555_);
return v_r_1556_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg(lean_object* v_n_1557_, lean_object* v_as_1558_, lean_object* v_lo_1559_, lean_object* v_hi_1560_){
_start:
{
lean_object* v___y_1562_; uint8_t v___x_1572_; 
v___x_1572_ = lean_nat_dec_lt(v_lo_1559_, v_hi_1560_);
if (v___x_1572_ == 0)
{
lean_dec(v_lo_1559_);
return v_as_1558_;
}
else
{
lean_object* v___x_1573_; lean_object* v___x_1574_; lean_object* v_mid_1575_; lean_object* v___y_1577_; lean_object* v___y_1583_; lean_object* v___x_1588_; lean_object* v___x_1589_; uint8_t v___x_1590_; 
v___x_1573_ = lean_nat_add(v_lo_1559_, v_hi_1560_);
v___x_1574_ = lean_unsigned_to_nat(1u);
v_mid_1575_ = lean_nat_shiftr(v___x_1573_, v___x_1574_);
lean_dec(v___x_1573_);
v___x_1588_ = lean_array_fget_borrowed(v_as_1558_, v_mid_1575_);
v___x_1589_ = lean_array_fget_borrowed(v_as_1558_, v_lo_1559_);
lean_inc(v___x_1589_);
lean_inc(v___x_1588_);
v___x_1590_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0(v___x_1572_, v___x_1588_, v___x_1589_);
if (v___x_1590_ == 0)
{
v___y_1583_ = v_as_1558_;
goto v___jp_1582_;
}
else
{
lean_object* v___x_1591_; 
v___x_1591_ = lean_array_fswap(v_as_1558_, v_lo_1559_, v_mid_1575_);
v___y_1583_ = v___x_1591_;
goto v___jp_1582_;
}
v___jp_1576_:
{
lean_object* v___x_1578_; lean_object* v___x_1579_; uint8_t v___x_1580_; 
v___x_1578_ = lean_array_fget_borrowed(v___y_1577_, v_mid_1575_);
v___x_1579_ = lean_array_fget_borrowed(v___y_1577_, v_hi_1560_);
lean_inc(v___x_1579_);
lean_inc(v___x_1578_);
v___x_1580_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0(v___x_1572_, v___x_1578_, v___x_1579_);
if (v___x_1580_ == 0)
{
lean_dec(v_mid_1575_);
v___y_1562_ = v___y_1577_;
goto v___jp_1561_;
}
else
{
lean_object* v___x_1581_; 
v___x_1581_ = lean_array_fswap(v___y_1577_, v_mid_1575_, v_hi_1560_);
lean_dec(v_mid_1575_);
v___y_1562_ = v___x_1581_;
goto v___jp_1561_;
}
}
v___jp_1582_:
{
lean_object* v___x_1584_; lean_object* v___x_1585_; uint8_t v___x_1586_; 
v___x_1584_ = lean_array_fget_borrowed(v___y_1583_, v_hi_1560_);
v___x_1585_ = lean_array_fget_borrowed(v___y_1583_, v_lo_1559_);
lean_inc(v___x_1585_);
lean_inc(v___x_1584_);
v___x_1586_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___lam__0(v___x_1572_, v___x_1584_, v___x_1585_);
if (v___x_1586_ == 0)
{
v___y_1577_ = v___y_1583_;
goto v___jp_1576_;
}
else
{
lean_object* v___x_1587_; 
v___x_1587_ = lean_array_fswap(v___y_1583_, v_lo_1559_, v_hi_1560_);
v___y_1577_ = v___x_1587_;
goto v___jp_1576_;
}
}
}
v___jp_1561_:
{
lean_object* v_pivot_1563_; lean_object* v___x_1564_; lean_object* v_fst_1565_; lean_object* v_snd_1566_; uint8_t v___x_1567_; 
v_pivot_1563_ = lean_array_fget(v___y_1562_, v_hi_1560_);
lean_inc_n(v_lo_1559_, 2);
v___x_1564_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___redArg(v_hi_1560_, v_pivot_1563_, v___y_1562_, v_lo_1559_, v_lo_1559_);
v_fst_1565_ = lean_ctor_get(v___x_1564_, 0);
lean_inc(v_fst_1565_);
v_snd_1566_ = lean_ctor_get(v___x_1564_, 1);
lean_inc(v_snd_1566_);
lean_dec_ref(v___x_1564_);
v___x_1567_ = lean_nat_dec_le(v_hi_1560_, v_fst_1565_);
if (v___x_1567_ == 0)
{
lean_object* v___x_1568_; lean_object* v___x_1569_; lean_object* v___x_1570_; 
v___x_1568_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg(v_n_1557_, v_snd_1566_, v_lo_1559_, v_fst_1565_);
v___x_1569_ = lean_unsigned_to_nat(1u);
v___x_1570_ = lean_nat_add(v_fst_1565_, v___x_1569_);
lean_dec(v_fst_1565_);
v_as_1558_ = v___x_1568_;
v_lo_1559_ = v___x_1570_;
goto _start;
}
else
{
lean_dec(v_fst_1565_);
lean_dec(v_lo_1559_);
return v_snd_1566_;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg___boxed(lean_object* v_n_1592_, lean_object* v_as_1593_, lean_object* v_lo_1594_, lean_object* v_hi_1595_){
_start:
{
lean_object* v_res_1596_; 
v_res_1596_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg(v_n_1592_, v_as_1593_, v_lo_1594_, v_hi_1595_);
lean_dec(v_hi_1595_);
lean_dec(v_n_1592_);
return v_res_1596_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0(void){
_start:
{
lean_object* v___x_1597_; lean_object* v___x_1598_; lean_object* v___x_1599_; 
v___x_1597_ = lean_unsigned_to_nat(32u);
v___x_1598_ = lean_mk_empty_array_with_capacity(v___x_1597_);
v___x_1599_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1599_, 0, v___x_1598_);
return v___x_1599_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__1(void){
_start:
{
lean_object* v___x_1600_; 
v___x_1600_ = l_Lean_PersistentHashMap_mkEmptyEntriesArray(lean_box(0), lean_box(0));
return v___x_1600_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2(void){
_start:
{
lean_object* v___x_1601_; lean_object* v___x_1602_; 
v___x_1601_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__1);
v___x_1602_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1602_, 0, v___x_1601_);
return v___x_1602_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3(void){
_start:
{
lean_object* v___x_1603_; lean_object* v___x_1604_; 
v___x_1603_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2);
v___x_1604_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1604_, 0, v___x_1603_);
lean_ctor_set(v___x_1604_, 1, v___x_1603_);
return v___x_1604_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0(lean_object* v___x_1608_, lean_object* v___x_1609_, lean_object* v___x_1610_, uint8_t v___x_1611_, lean_object* v_a_1612_, lean_object* v___x_1613_, lean_object* v___x_1614_, lean_object* v___x_1615_, lean_object* v___x_1616_, lean_object* v___x_1617_, lean_object* v___x_1618_, lean_object* v___x_1619_, uint8_t v___x_1620_, lean_object* v_n_1621_){
_start:
{
lean_object* v___x_1626_; lean_object* v___x_1627_; lean_object* v___x_1628_; size_t v___x_1629_; lean_object* v___x_1630_; lean_object* v___x_1631_; lean_object* v___x_1632_; lean_object* v___x_1633_; lean_object* v___x_1634_; lean_object* v___x_1635_; lean_object* v___x_1636_; lean_object* v___x_1637_; lean_object* v___x_1638_; lean_object* v___x_1639_; lean_object* v___x_1640_; uint64_t v___x_1641_; lean_object* v___x_1642_; lean_object* v___x_1643_; lean_object* v___x_1644_; lean_object* v___x_1645_; lean_object* v___x_1646_; lean_object* v___x_1647_; lean_object* v___x_1648_; lean_object* v___x_1649_; lean_object* v_env_1650_; lean_object* v___x_1651_; uint8_t v___x_1652_; lean_object* v_fileName_1654_; lean_object* v_fileMap_1655_; lean_object* v_currRecDepth_1656_; lean_object* v_ref_1657_; lean_object* v_currNamespace_1658_; lean_object* v_openDecls_1659_; lean_object* v_initHeartbeats_1660_; lean_object* v_maxHeartbeats_1661_; lean_object* v_quotContext_1662_; lean_object* v_currMacroScope_1663_; lean_object* v_cancelTk_x3f_1664_; uint8_t v_suppressElabErrors_1665_; lean_object* v_inheritedTraceOptions_1666_; lean_object* v___y_1667_; uint8_t v___y_1696_; uint8_t v___x_1716_; 
v___x_1626_ = lean_unsigned_to_nat(32u);
v___x_1627_ = lean_mk_empty_array_with_capacity(v___x_1626_);
v___x_1628_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0);
v___x_1629_ = ((size_t)5ULL);
lean_inc_n(v___x_1608_, 2);
v___x_1630_ = lean_alloc_ctor(0, 4, sizeof(size_t)*1);
lean_ctor_set(v___x_1630_, 0, v___x_1628_);
lean_ctor_set(v___x_1630_, 1, v___x_1627_);
lean_ctor_set(v___x_1630_, 2, v___x_1608_);
lean_ctor_set(v___x_1630_, 3, v___x_1608_);
lean_ctor_set_usize(v___x_1630_, 4, v___x_1629_);
v___x_1631_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2);
v___x_1632_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3);
v___x_1633_ = lean_box(1);
lean_inc_ref_n(v___x_1630_, 3);
v___x_1634_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_1634_, 0, v___x_1630_);
lean_ctor_set(v___x_1634_, 1, v___x_1630_);
lean_ctor_set(v___x_1634_, 2, v___x_1633_);
v___x_1635_ = lean_io_get_num_heartbeats();
v___x_1636_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__5));
lean_inc_n(v___x_1609_, 2);
v___x_1637_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1637_, 0, v___x_1636_);
lean_ctor_set(v___x_1637_, 1, v___x_1609_);
v___x_1638_ = lean_unsigned_to_nat(2u);
v___x_1639_ = lean_box(0);
lean_inc(v___x_1610_);
v___x_1640_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_1640_, 0, v___x_1610_);
lean_ctor_set(v___x_1640_, 1, v___x_1609_);
lean_ctor_set(v___x_1640_, 2, v___x_1639_);
v___x_1641_ = 0ULL;
v___x_1642_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_1642_, 0, v___x_1630_);
lean_ctor_set_uint64(v___x_1642_, sizeof(void*)*1, v___x_1641_);
v___x_1643_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_1643_, 0, v___x_1631_);
lean_ctor_set(v___x_1643_, 1, v___x_1631_);
lean_ctor_set(v___x_1643_, 2, v___x_1630_);
lean_ctor_set_uint8(v___x_1643_, sizeof(void*)*3, v___x_1611_);
v___x_1644_ = lean_mk_empty_array_with_capacity(v___x_1608_);
v___x_1645_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_1645_, 0, v_a_1612_);
lean_ctor_set(v___x_1645_, 1, v___x_1638_);
lean_ctor_set(v___x_1645_, 2, v___x_1637_);
lean_ctor_set(v___x_1645_, 3, v___x_1640_);
lean_ctor_set(v___x_1645_, 4, v___x_1642_);
lean_ctor_set(v___x_1645_, 5, v___x_1632_);
lean_ctor_set(v___x_1645_, 6, v___x_1634_);
lean_ctor_set(v___x_1645_, 7, v___x_1643_);
lean_ctor_set(v___x_1645_, 8, v___x_1644_);
v___x_1646_ = lean_st_mk_ref(v___x_1645_);
v___x_1647_ = l_Lean_inheritedTraceOptions;
v___x_1648_ = lean_st_ref_get(v___x_1647_);
v___x_1649_ = lean_st_ref_get(v___x_1646_);
v_env_1650_ = lean_ctor_get(v___x_1649_, 0);
lean_inc_ref(v_env_1650_);
lean_dec(v___x_1649_);
v___x_1651_ = l_Lean_diagnostics;
v___x_1652_ = l_Lean_Option_get___at___00Lean_Elab_addMacroStack___at___00Lean_throwError___at___00Lean_throwErrorAt___at___00Lean_throwUnknownIdentifierAt___at___00Lean_throwUnknownConstantAt___at___00Lean_throwUnknownConstant___at___00Lean_getConstVal___at___00Lean_mkConstWithLevelParams___at___00Lean_Elab_addConstInfo___at___00Lean_Elab_PostprocessTraces_elabStoreTraceAs_spec__3_spec__5_spec__6_spec__9_spec__12_spec__14_spec__16_spec__18_spec__20_spec__21(v___x_1613_, v___x_1651_);
v___x_1716_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_1650_);
lean_dec_ref(v_env_1650_);
if (v___x_1716_ == 0)
{
if (v___x_1652_ == 0)
{
lean_inc(v___x_1646_);
lean_inc(v___x_1610_);
v_fileName_1654_ = v___x_1614_;
v_fileMap_1655_ = v___x_1615_;
v_currRecDepth_1656_ = v___x_1608_;
v_ref_1657_ = v___x_1616_;
v_currNamespace_1658_ = v___x_1610_;
v_openDecls_1659_ = v___x_1617_;
v_initHeartbeats_1660_ = v___x_1635_;
v_maxHeartbeats_1661_ = v___x_1618_;
v_quotContext_1662_ = v___x_1610_;
v_currMacroScope_1663_ = v___x_1609_;
v_cancelTk_x3f_1664_ = v___x_1619_;
v_suppressElabErrors_1665_ = v___x_1620_;
v_inheritedTraceOptions_1666_ = v___x_1648_;
v___y_1667_ = v___x_1646_;
goto v___jp_1653_;
}
else
{
v___y_1696_ = v___x_1716_;
goto v___jp_1695_;
}
}
else
{
v___y_1696_ = v___x_1652_;
goto v___jp_1695_;
}
v___jp_1623_:
{
lean_object* v___x_1624_; lean_object* v___x_1625_; 
v___x_1624_ = lean_box(0);
v___x_1625_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1625_, 0, v___x_1624_);
return v___x_1625_;
}
v___jp_1653_:
{
lean_object* v___x_1668_; lean_object* v___x_1669_; lean_object* v___x_1670_; lean_object* v___x_1671_; 
v___x_1668_ = l_Lean_maxRecDepth;
v___x_1669_ = l_Lean_Option_get___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0(v___x_1613_, v___x_1668_);
v___x_1670_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_1670_, 0, v_fileName_1654_);
lean_ctor_set(v___x_1670_, 1, v_fileMap_1655_);
lean_ctor_set(v___x_1670_, 2, v___x_1613_);
lean_ctor_set(v___x_1670_, 3, v_currRecDepth_1656_);
lean_ctor_set(v___x_1670_, 4, v___x_1669_);
lean_ctor_set(v___x_1670_, 5, v_ref_1657_);
lean_ctor_set(v___x_1670_, 6, v_currNamespace_1658_);
lean_ctor_set(v___x_1670_, 7, v_openDecls_1659_);
lean_ctor_set(v___x_1670_, 8, v_initHeartbeats_1660_);
lean_ctor_set(v___x_1670_, 9, v_maxHeartbeats_1661_);
lean_ctor_set(v___x_1670_, 10, v_quotContext_1662_);
lean_ctor_set(v___x_1670_, 11, v_currMacroScope_1663_);
lean_ctor_set(v___x_1670_, 12, v_cancelTk_x3f_1664_);
lean_ctor_set(v___x_1670_, 13, v_inheritedTraceOptions_1666_);
lean_ctor_set_uint8(v___x_1670_, sizeof(void*)*14, v___x_1652_);
lean_ctor_set_uint8(v___x_1670_, sizeof(void*)*14 + 1, v_suppressElabErrors_1665_);
v___x_1671_ = l_Lean_findDeclarationRanges_x3f___at___00Lean_Linter_EnvLinter_sortResults_spec__0(v_n_1621_, v___x_1670_, v___y_1667_);
lean_dec(v___y_1667_);
lean_dec_ref_known(v___x_1670_, 14);
if (lean_obj_tag(v___x_1671_) == 0)
{
lean_object* v_a_1672_; lean_object* v___x_1674_; uint8_t v_isShared_1675_; uint8_t v_isSharedCheck_1689_; 
v_a_1672_ = lean_ctor_get(v___x_1671_, 0);
v_isSharedCheck_1689_ = !lean_is_exclusive(v___x_1671_);
if (v_isSharedCheck_1689_ == 0)
{
v___x_1674_ = v___x_1671_;
v_isShared_1675_ = v_isSharedCheck_1689_;
goto v_resetjp_1673_;
}
else
{
lean_inc(v_a_1672_);
lean_dec(v___x_1671_);
v___x_1674_ = lean_box(0);
v_isShared_1675_ = v_isSharedCheck_1689_;
goto v_resetjp_1673_;
}
v_resetjp_1673_:
{
lean_object* v___x_1676_; 
v___x_1676_ = lean_st_ref_get(v___x_1646_);
lean_dec(v___x_1646_);
lean_dec(v___x_1676_);
if (lean_obj_tag(v_a_1672_) == 0)
{
lean_del_object(v___x_1674_);
goto v___jp_1623_;
}
else
{
lean_object* v_val_1677_; lean_object* v___x_1679_; uint8_t v_isShared_1680_; uint8_t v_isSharedCheck_1688_; 
v_val_1677_ = lean_ctor_get(v_a_1672_, 0);
v_isSharedCheck_1688_ = !lean_is_exclusive(v_a_1672_);
if (v_isSharedCheck_1688_ == 0)
{
v___x_1679_ = v_a_1672_;
v_isShared_1680_ = v_isSharedCheck_1688_;
goto v_resetjp_1678_;
}
else
{
lean_inc(v_val_1677_);
lean_dec(v_a_1672_);
v___x_1679_ = lean_box(0);
v_isShared_1680_ = v_isSharedCheck_1688_;
goto v_resetjp_1678_;
}
v_resetjp_1678_:
{
lean_object* v_range_1681_; lean_object* v___x_1683_; 
v_range_1681_ = lean_ctor_get(v_val_1677_, 0);
lean_inc_ref(v_range_1681_);
lean_dec(v_val_1677_);
if (v_isShared_1680_ == 0)
{
lean_ctor_set(v___x_1679_, 0, v_range_1681_);
v___x_1683_ = v___x_1679_;
goto v_reusejp_1682_;
}
else
{
lean_object* v_reuseFailAlloc_1687_; 
v_reuseFailAlloc_1687_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1687_, 0, v_range_1681_);
v___x_1683_ = v_reuseFailAlloc_1687_;
goto v_reusejp_1682_;
}
v_reusejp_1682_:
{
lean_object* v___x_1685_; 
if (v_isShared_1675_ == 0)
{
lean_ctor_set(v___x_1674_, 0, v___x_1683_);
v___x_1685_ = v___x_1674_;
goto v_reusejp_1684_;
}
else
{
lean_object* v_reuseFailAlloc_1686_; 
v_reuseFailAlloc_1686_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1686_, 0, v___x_1683_);
v___x_1685_ = v_reuseFailAlloc_1686_;
goto v_reusejp_1684_;
}
v_reusejp_1684_:
{
return v___x_1685_;
}
}
}
}
}
}
else
{
lean_object* v_a_1690_; 
lean_dec(v___x_1646_);
v_a_1690_ = lean_ctor_get(v___x_1671_, 0);
lean_inc(v_a_1690_);
lean_dec_ref_known(v___x_1671_, 1);
if (lean_obj_tag(v_a_1690_) == 0)
{
lean_object* v_msg_1691_; lean_object* v___x_1692_; 
v_msg_1691_ = lean_ctor_get(v_a_1690_, 1);
lean_inc_ref(v_msg_1691_);
lean_dec_ref_known(v_a_1690_, 2);
v___x_1692_ = l_Lean_MessageData_toString(v_msg_1691_);
lean_dec_ref(v___x_1692_);
goto v___jp_1623_;
}
else
{
lean_object* v_id_1693_; lean_object* v___x_1694_; 
v_id_1693_ = lean_ctor_get(v_a_1690_, 0);
lean_inc(v_id_1693_);
lean_dec_ref_known(v_a_1690_, 2);
v___x_1694_ = l_Lean_InternalExceptionId_getName(v_id_1693_);
lean_dec(v_id_1693_);
lean_dec_ref(v___x_1694_);
goto v___jp_1623_;
}
}
}
v___jp_1695_:
{
if (v___y_1696_ == 0)
{
lean_object* v___x_1697_; lean_object* v_env_1698_; lean_object* v_nextMacroScope_1699_; lean_object* v_ngen_1700_; lean_object* v_auxDeclNGen_1701_; lean_object* v_traceState_1702_; lean_object* v_messages_1703_; lean_object* v_infoState_1704_; lean_object* v_snapshotTasks_1705_; lean_object* v___x_1707_; uint8_t v_isShared_1708_; uint8_t v_isSharedCheck_1714_; 
v___x_1697_ = lean_st_ref_take(v___x_1646_);
v_env_1698_ = lean_ctor_get(v___x_1697_, 0);
v_nextMacroScope_1699_ = lean_ctor_get(v___x_1697_, 1);
v_ngen_1700_ = lean_ctor_get(v___x_1697_, 2);
v_auxDeclNGen_1701_ = lean_ctor_get(v___x_1697_, 3);
v_traceState_1702_ = lean_ctor_get(v___x_1697_, 4);
v_messages_1703_ = lean_ctor_get(v___x_1697_, 6);
v_infoState_1704_ = lean_ctor_get(v___x_1697_, 7);
v_snapshotTasks_1705_ = lean_ctor_get(v___x_1697_, 8);
v_isSharedCheck_1714_ = !lean_is_exclusive(v___x_1697_);
if (v_isSharedCheck_1714_ == 0)
{
lean_object* v_unused_1715_; 
v_unused_1715_ = lean_ctor_get(v___x_1697_, 5);
lean_dec(v_unused_1715_);
v___x_1707_ = v___x_1697_;
v_isShared_1708_ = v_isSharedCheck_1714_;
goto v_resetjp_1706_;
}
else
{
lean_inc(v_snapshotTasks_1705_);
lean_inc(v_infoState_1704_);
lean_inc(v_messages_1703_);
lean_inc(v_traceState_1702_);
lean_inc(v_auxDeclNGen_1701_);
lean_inc(v_ngen_1700_);
lean_inc(v_nextMacroScope_1699_);
lean_inc(v_env_1698_);
lean_dec(v___x_1697_);
v___x_1707_ = lean_box(0);
v_isShared_1708_ = v_isSharedCheck_1714_;
goto v_resetjp_1706_;
}
v_resetjp_1706_:
{
lean_object* v___x_1709_; lean_object* v___x_1711_; 
v___x_1709_ = l_Lean_Kernel_enableDiag(v_env_1698_, v___x_1652_);
if (v_isShared_1708_ == 0)
{
lean_ctor_set(v___x_1707_, 5, v___x_1632_);
lean_ctor_set(v___x_1707_, 0, v___x_1709_);
v___x_1711_ = v___x_1707_;
goto v_reusejp_1710_;
}
else
{
lean_object* v_reuseFailAlloc_1713_; 
v_reuseFailAlloc_1713_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_1713_, 0, v___x_1709_);
lean_ctor_set(v_reuseFailAlloc_1713_, 1, v_nextMacroScope_1699_);
lean_ctor_set(v_reuseFailAlloc_1713_, 2, v_ngen_1700_);
lean_ctor_set(v_reuseFailAlloc_1713_, 3, v_auxDeclNGen_1701_);
lean_ctor_set(v_reuseFailAlloc_1713_, 4, v_traceState_1702_);
lean_ctor_set(v_reuseFailAlloc_1713_, 5, v___x_1632_);
lean_ctor_set(v_reuseFailAlloc_1713_, 6, v_messages_1703_);
lean_ctor_set(v_reuseFailAlloc_1713_, 7, v_infoState_1704_);
lean_ctor_set(v_reuseFailAlloc_1713_, 8, v_snapshotTasks_1705_);
v___x_1711_ = v_reuseFailAlloc_1713_;
goto v_reusejp_1710_;
}
v_reusejp_1710_:
{
lean_object* v___x_1712_; 
v___x_1712_ = lean_st_ref_set(v___x_1646_, v___x_1711_);
lean_inc(v___x_1646_);
lean_inc(v___x_1610_);
v_fileName_1654_ = v___x_1614_;
v_fileMap_1655_ = v___x_1615_;
v_currRecDepth_1656_ = v___x_1608_;
v_ref_1657_ = v___x_1616_;
v_currNamespace_1658_ = v___x_1610_;
v_openDecls_1659_ = v___x_1617_;
v_initHeartbeats_1660_ = v___x_1635_;
v_maxHeartbeats_1661_ = v___x_1618_;
v_quotContext_1662_ = v___x_1610_;
v_currMacroScope_1663_ = v___x_1609_;
v_cancelTk_x3f_1664_ = v___x_1619_;
v_suppressElabErrors_1665_ = v___x_1620_;
v_inheritedTraceOptions_1666_ = v___x_1648_;
v___y_1667_ = v___x_1646_;
goto v___jp_1653_;
}
}
}
else
{
lean_inc(v___x_1646_);
lean_inc(v___x_1610_);
v_fileName_1654_ = v___x_1614_;
v_fileMap_1655_ = v___x_1615_;
v_currRecDepth_1656_ = v___x_1608_;
v_ref_1657_ = v___x_1616_;
v_currNamespace_1658_ = v___x_1610_;
v_openDecls_1659_ = v___x_1617_;
v_initHeartbeats_1660_ = v___x_1635_;
v_maxHeartbeats_1661_ = v___x_1618_;
v_quotContext_1662_ = v___x_1610_;
v_currMacroScope_1663_ = v___x_1609_;
v_cancelTk_x3f_1664_ = v___x_1619_;
v_suppressElabErrors_1665_ = v___x_1620_;
v_inheritedTraceOptions_1666_ = v___x_1648_;
v___y_1667_ = v___x_1646_;
goto v___jp_1653_;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___boxed(lean_object* v___x_1717_, lean_object* v___x_1718_, lean_object* v___x_1719_, lean_object* v___x_1720_, lean_object* v_a_1721_, lean_object* v___x_1722_, lean_object* v___x_1723_, lean_object* v___x_1724_, lean_object* v___x_1725_, lean_object* v___x_1726_, lean_object* v___x_1727_, lean_object* v___x_1728_, lean_object* v___x_1729_, lean_object* v_n_1730_, lean_object* v___y_1731_){
_start:
{
uint8_t v___x_73138__boxed_1732_; uint8_t v___x_73147__boxed_1733_; lean_object* v_res_1734_; 
v___x_73138__boxed_1732_ = lean_unbox(v___x_1720_);
v___x_73147__boxed_1733_ = lean_unbox(v___x_1729_);
v_res_1734_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0(v___x_1717_, v___x_1718_, v___x_1719_, v___x_73138__boxed_1732_, v_a_1721_, v___x_1722_, v___x_1723_, v___x_1724_, v___x_1725_, v___x_1726_, v___x_1727_, v___x_1728_, v___x_73147__boxed_1733_, v_n_1730_);
return v_res_1734_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4(void){
_start:
{
lean_object* v___x_1741_; lean_object* v___x_1742_; lean_object* v___x_1743_; lean_object* v___x_1744_; 
v___x_1741_ = lean_unsigned_to_nat(100u);
v___x_1742_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__3));
v___x_1743_ = l_Lean_Options_empty;
v___x_1744_ = l_Lean_Options_set___at___00Lean_Option_set___at___00__private_Lean_Shell_0__Lean_ShellOptions_process_spec__2_spec__3(v___x_1743_, v___x_1742_, v___x_1741_);
return v___x_1744_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5(void){
_start:
{
lean_object* v___x_1745_; lean_object* v___x_1746_; 
v___x_1745_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_1746_ = l_Lean_Core_getMaxHeartbeats(v___x_1745_);
return v___x_1746_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7(void){
_start:
{
lean_object* v___x_1748_; lean_object* v___x_1749_; 
v___x_1748_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__6));
v___x_1749_ = lean_string_utf8_byte_size(v___x_1748_);
return v___x_1749_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9(void){
_start:
{
lean_object* v___x_1751_; lean_object* v___x_1752_; 
v___x_1751_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__8));
v___x_1752_ = lean_string_utf8_byte_size(v___x_1751_);
return v___x_1752_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11(void){
_start:
{
lean_object* v___x_1754_; lean_object* v___x_1755_; 
v___x_1754_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__10));
v___x_1755_ = lean_string_utf8_byte_size(v___x_1754_);
return v___x_1755_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15(lean_object* v_a_1756_, lean_object* v___x_1757_, lean_object* v_as_1758_, size_t v_sz_1759_, size_t v_i_1760_, lean_object* v_b_1761_){
_start:
{
uint8_t v___x_1763_; 
v___x_1763_ = lean_usize_dec_lt(v_i_1760_, v_sz_1759_);
if (v___x_1763_ == 0)
{
lean_object* v___x_1764_; 
lean_dec_ref(v_a_1756_);
v___x_1764_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1764_, 0, v_b_1761_);
return v___x_1764_;
}
else
{
lean_object* v_a_1765_; lean_object* v_fst_1766_; lean_object* v_snd_1767_; lean_object* v_c_1769_; lean_object* v___y_1775_; uint8_t v___y_1780_; lean_object* v___y_1781_; uint8_t v___y_1785_; lean_object* v___y_1786_; uint8_t v___y_1787_; lean_object* v___x_1793_; lean_object* v___x_1794_; lean_object* v___x_1795_; lean_object* v___x_1796_; lean_object* v___x_1797_; lean_object* v___x_1798_; lean_object* v___x_1799_; lean_object* v___x_1800_; lean_object* v___x_1801_; uint8_t v___x_1802_; lean_object* v___x_1803_; uint8_t v___y_1805_; uint8_t v___y_1806_; lean_object* v___y_1807_; uint8_t v___y_1808_; uint8_t v___y_1848_; lean_object* v___y_1849_; uint8_t v___y_1850_; lean_object* v___y_1851_; uint8_t v___y_1856_; uint8_t v___y_1857_; lean_object* v___y_1858_; lean_object* v___y_1859_; uint8_t v___y_1866_; lean_object* v___y_1867_; uint8_t v___y_1868_; lean_object* v___y_1869_; uint8_t v___y_1870_; uint8_t v___y_1877_; lean_object* v___y_1878_; uint8_t v___y_1879_; lean_object* v___y_1928_; uint8_t v___y_1929_; lean_object* v___y_1932_; lean_object* v___y_1941_; 
v_a_1765_ = lean_array_uget_borrowed(v_as_1758_, v_i_1760_);
v_fst_1766_ = lean_ctor_get(v_a_1765_, 0);
v_snd_1767_ = lean_ctor_get(v_a_1765_, 1);
lean_inc(v_snd_1767_);
v___x_1793_ = lean_unsigned_to_nat(1u);
v___x_1794_ = lean_unsigned_to_nat(0u);
v___x_1795_ = lean_box(0);
v___x_1796_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_1797_ = l_Lean_instInhabitedFileMap_default;
v___x_1798_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_1799_ = lean_box(0);
v___x_1800_ = lean_box(0);
v___x_1801_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_1802_ = 0;
v___x_1803_ = lean_box(0);
if (lean_obj_tag(v_fst_1766_) == 0)
{
v___y_1941_ = v_fst_1766_;
goto v___jp_1940_;
}
else
{
lean_object* v_pre_1946_; 
v_pre_1946_ = lean_ctor_get(v_fst_1766_, 0);
lean_inc(v_pre_1946_);
v___y_1941_ = v_pre_1946_;
goto v___jp_1940_;
}
v___jp_1768_:
{
lean_object* v___x_1770_; size_t v___x_1771_; size_t v___x_1772_; 
lean_inc(v_fst_1766_);
v___x_1770_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_b_1761_, v_fst_1766_, v_c_1769_);
v___x_1771_ = ((size_t)1ULL);
v___x_1772_ = lean_usize_add(v_i_1760_, v___x_1771_);
v_i_1760_ = v___x_1772_;
v_b_1761_ = v___x_1770_;
goto _start;
}
v___jp_1774_:
{
lean_object* v___x_1776_; 
v___x_1776_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1776_, 0, v___y_1775_);
v_c_1769_ = v___x_1776_;
goto v___jp_1768_;
}
v___jp_1777_:
{
lean_object* v___x_1778_; 
v___x_1778_ = lean_box(0);
v_c_1769_ = v___x_1778_;
goto v___jp_1768_;
}
v___jp_1779_:
{
if (v___y_1780_ == 0)
{
lean_object* v___x_1782_; 
v___x_1782_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1782_, 0, v___y_1781_);
v_c_1769_ = v___x_1782_;
goto v___jp_1768_;
}
else
{
lean_object* v___x_1783_; 
lean_dec(v___y_1781_);
v___x_1783_ = lean_box(5);
v_c_1769_ = v___x_1783_;
goto v___jp_1768_;
}
}
v___jp_1784_:
{
if (v___y_1787_ == 0)
{
lean_dec(v___y_1786_);
if (v___y_1785_ == 0)
{
lean_object* v___x_1788_; 
v___x_1788_ = lean_box(6);
v_c_1769_ = v___x_1788_;
goto v___jp_1768_;
}
else
{
lean_object* v___x_1789_; 
v___x_1789_ = lean_box(5);
v_c_1769_ = v___x_1789_;
goto v___jp_1768_;
}
}
else
{
lean_object* v___x_1790_; 
v___x_1790_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_1790_, 0, v___y_1786_);
v_c_1769_ = v___x_1790_;
goto v___jp_1768_;
}
}
v___jp_1791_:
{
lean_object* v___x_1792_; 
v___x_1792_ = lean_box(0);
v_c_1769_ = v___x_1792_;
goto v___jp_1768_;
}
v___jp_1804_:
{
if (v___y_1808_ == 0)
{
lean_dec(v___y_1807_);
goto v___jp_1777_;
}
else
{
if (v___y_1805_ == 0)
{
if (v___y_1806_ == 0)
{
lean_dec(v___y_1807_);
goto v___jp_1777_;
}
else
{
lean_object* v___x_1809_; 
lean_inc(v_fst_1766_);
lean_inc_ref(v_a_1756_);
v___x_1809_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0(v___x_1794_, v___x_1793_, v___x_1795_, v___x_1763_, v_a_1756_, v___x_1798_, v___x_1796_, v___x_1797_, v___x_1799_, v___x_1800_, v___x_1801_, v___x_1803_, v___x_1802_, v_fst_1766_);
if (lean_obj_tag(v___x_1809_) == 0)
{
lean_object* v_a_1810_; lean_object* v___x_1811_; 
v_a_1810_ = lean_ctor_get(v___x_1809_, 0);
lean_inc(v_a_1810_);
lean_dec_ref_known(v___x_1809_, 1);
lean_inc(v___y_1807_);
lean_inc_ref(v_a_1756_);
v___x_1811_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0(v___x_1794_, v___x_1793_, v___x_1795_, v___x_1763_, v_a_1756_, v___x_1798_, v___x_1796_, v___x_1797_, v___x_1799_, v___x_1800_, v___x_1801_, v___x_1803_, v___x_1802_, v___y_1807_);
if (lean_obj_tag(v___x_1811_) == 0)
{
if (lean_obj_tag(v_a_1810_) == 0)
{
lean_object* v___x_1812_; 
lean_dec_ref_known(v___x_1811_, 1);
v___x_1812_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1812_, 0, v___y_1807_);
v_c_1769_ = v___x_1812_;
goto v___jp_1768_;
}
else
{
lean_object* v_a_1813_; 
v_a_1813_ = lean_ctor_get(v___x_1811_, 0);
lean_inc(v_a_1813_);
lean_dec_ref_known(v___x_1811_, 1);
if (lean_obj_tag(v_a_1813_) == 0)
{
lean_object* v___x_1814_; 
lean_dec_ref_known(v_a_1810_, 1);
lean_dec(v___y_1807_);
v___x_1814_ = lean_box(0);
v_c_1769_ = v___x_1814_;
goto v___jp_1768_;
}
else
{
lean_object* v_val_1815_; lean_object* v_val_1816_; lean_object* v___x_1818_; uint8_t v_isShared_1819_; uint8_t v_isSharedCheck_1829_; 
v_val_1815_ = lean_ctor_get(v_a_1810_, 0);
lean_inc(v_val_1815_);
lean_dec_ref_known(v_a_1810_, 1);
v_val_1816_ = lean_ctor_get(v_a_1813_, 0);
v_isSharedCheck_1829_ = !lean_is_exclusive(v_a_1813_);
if (v_isSharedCheck_1829_ == 0)
{
v___x_1818_ = v_a_1813_;
v_isShared_1819_ = v_isSharedCheck_1829_;
goto v_resetjp_1817_;
}
else
{
lean_inc(v_val_1816_);
lean_dec(v_a_1813_);
v___x_1818_ = lean_box(0);
v_isShared_1819_ = v_isSharedCheck_1829_;
goto v_resetjp_1817_;
}
v_resetjp_1817_:
{
lean_object* v_pos_1820_; lean_object* v_endPos_1821_; lean_object* v_pos_1822_; lean_object* v_endPos_1823_; uint8_t v___x_1824_; 
v_pos_1820_ = lean_ctor_get(v_val_1815_, 0);
lean_inc_ref(v_pos_1820_);
v_endPos_1821_ = lean_ctor_get(v_val_1815_, 2);
lean_inc_ref(v_endPos_1821_);
lean_dec(v_val_1815_);
v_pos_1822_ = lean_ctor_get(v_val_1816_, 0);
lean_inc_ref(v_pos_1822_);
v_endPos_1823_ = lean_ctor_get(v_val_1816_, 2);
lean_inc_ref(v_endPos_1823_);
lean_dec(v_val_1816_);
v___x_1824_ = l_Lean_instDecidableEqPosition_decEq(v_pos_1820_, v_pos_1822_);
lean_dec_ref(v_pos_1822_);
lean_dec_ref(v_pos_1820_);
if (v___x_1824_ == 0)
{
lean_dec_ref(v_endPos_1823_);
lean_dec_ref(v_endPos_1821_);
lean_del_object(v___x_1818_);
lean_dec(v___y_1807_);
goto v___jp_1791_;
}
else
{
uint8_t v___x_1825_; 
v___x_1825_ = l_Lean_instDecidableEqPosition_decEq(v_endPos_1821_, v_endPos_1823_);
lean_dec_ref(v_endPos_1823_);
lean_dec_ref(v_endPos_1821_);
if (v___x_1825_ == 0)
{
lean_del_object(v___x_1818_);
lean_dec(v___y_1807_);
goto v___jp_1791_;
}
else
{
lean_object* v___x_1827_; 
if (v_isShared_1819_ == 0)
{
lean_ctor_set_tag(v___x_1818_, 3);
lean_ctor_set(v___x_1818_, 0, v___y_1807_);
v___x_1827_ = v___x_1818_;
goto v_reusejp_1826_;
}
else
{
lean_object* v_reuseFailAlloc_1828_; 
v_reuseFailAlloc_1828_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1828_, 0, v___y_1807_);
v___x_1827_ = v_reuseFailAlloc_1828_;
goto v_reusejp_1826_;
}
v_reusejp_1826_:
{
v_c_1769_ = v___x_1827_;
goto v___jp_1768_;
}
}
}
}
}
}
}
else
{
lean_object* v_a_1830_; lean_object* v___x_1832_; uint8_t v_isShared_1833_; uint8_t v_isSharedCheck_1837_; 
lean_dec(v_a_1810_);
lean_dec(v___y_1807_);
lean_dec_ref(v_b_1761_);
lean_dec_ref(v_a_1756_);
v_a_1830_ = lean_ctor_get(v___x_1811_, 0);
v_isSharedCheck_1837_ = !lean_is_exclusive(v___x_1811_);
if (v_isSharedCheck_1837_ == 0)
{
v___x_1832_ = v___x_1811_;
v_isShared_1833_ = v_isSharedCheck_1837_;
goto v_resetjp_1831_;
}
else
{
lean_inc(v_a_1830_);
lean_dec(v___x_1811_);
v___x_1832_ = lean_box(0);
v_isShared_1833_ = v_isSharedCheck_1837_;
goto v_resetjp_1831_;
}
v_resetjp_1831_:
{
lean_object* v___x_1835_; 
if (v_isShared_1833_ == 0)
{
v___x_1835_ = v___x_1832_;
goto v_reusejp_1834_;
}
else
{
lean_object* v_reuseFailAlloc_1836_; 
v_reuseFailAlloc_1836_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1836_, 0, v_a_1830_);
v___x_1835_ = v_reuseFailAlloc_1836_;
goto v_reusejp_1834_;
}
v_reusejp_1834_:
{
return v___x_1835_;
}
}
}
}
else
{
lean_object* v_a_1838_; lean_object* v___x_1840_; uint8_t v_isShared_1841_; uint8_t v_isSharedCheck_1845_; 
lean_dec(v___y_1807_);
lean_dec_ref(v_b_1761_);
lean_dec_ref(v_a_1756_);
v_a_1838_ = lean_ctor_get(v___x_1809_, 0);
v_isSharedCheck_1845_ = !lean_is_exclusive(v___x_1809_);
if (v_isSharedCheck_1845_ == 0)
{
v___x_1840_ = v___x_1809_;
v_isShared_1841_ = v_isSharedCheck_1845_;
goto v_resetjp_1839_;
}
else
{
lean_inc(v_a_1838_);
lean_dec(v___x_1809_);
v___x_1840_ = lean_box(0);
v_isShared_1841_ = v_isSharedCheck_1845_;
goto v_resetjp_1839_;
}
v_resetjp_1839_:
{
lean_object* v___x_1843_; 
if (v_isShared_1841_ == 0)
{
v___x_1843_ = v___x_1840_;
goto v_reusejp_1842_;
}
else
{
lean_object* v_reuseFailAlloc_1844_; 
v_reuseFailAlloc_1844_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1844_, 0, v_a_1838_);
v___x_1843_ = v_reuseFailAlloc_1844_;
goto v_reusejp_1842_;
}
v_reusejp_1842_:
{
return v___x_1843_;
}
}
}
}
}
else
{
lean_object* v___x_1846_; 
lean_dec(v___y_1807_);
v___x_1846_ = lean_box(5);
v_c_1769_ = v___x_1846_;
goto v___jp_1768_;
}
}
}
v___jp_1847_:
{
lean_object* v___x_1852_; uint8_t v___x_1853_; 
v___x_1852_ = ((lean_object*)(l_NsExport_softNames));
v___x_1853_ = l_List_elem___at___00Lean_Linter_List_indexLinter_spec__1(v___y_1851_, v___x_1852_);
if (v___x_1853_ == 0)
{
uint8_t v___x_1854_; 
v___x_1854_ = l_NsExport_isEqNum(v___y_1851_);
v___y_1805_ = v___y_1848_;
v___y_1806_ = v___y_1850_;
v___y_1807_ = v___y_1849_;
v___y_1808_ = v___x_1854_;
goto v___jp_1804_;
}
else
{
lean_dec_ref(v___y_1851_);
v___y_1805_ = v___y_1848_;
v___y_1806_ = v___y_1850_;
v___y_1807_ = v___y_1849_;
v___y_1808_ = v___x_1763_;
goto v___jp_1804_;
}
}
v___jp_1855_:
{
lean_object* v___x_1860_; lean_object* v___x_1861_; lean_object* v___x_1862_; uint8_t v___x_1863_; 
v___x_1860_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__6));
v___x_1861_ = lean_string_utf8_byte_size(v___y_1859_);
v___x_1862_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7);
v___x_1863_ = lean_nat_dec_le(v___x_1862_, v___x_1861_);
if (v___x_1863_ == 0)
{
v___y_1848_ = v___y_1856_;
v___y_1849_ = v___y_1858_;
v___y_1850_ = v___y_1857_;
v___y_1851_ = v___y_1859_;
goto v___jp_1847_;
}
else
{
uint8_t v___x_1864_; 
v___x_1864_ = lean_string_memcmp(v___y_1859_, v___x_1860_, v___x_1794_, v___x_1794_, v___x_1862_);
if (v___x_1864_ == 0)
{
v___y_1848_ = v___y_1856_;
v___y_1849_ = v___y_1858_;
v___y_1850_ = v___y_1857_;
v___y_1851_ = v___y_1859_;
goto v___jp_1847_;
}
else
{
lean_dec_ref(v___y_1859_);
v___y_1785_ = v___y_1856_;
v___y_1786_ = v___y_1858_;
v___y_1787_ = v___y_1857_;
goto v___jp_1784_;
}
}
}
v___jp_1865_:
{
if (v___y_1870_ == 0)
{
lean_object* v___x_1871_; lean_object* v___x_1872_; lean_object* v___x_1873_; uint8_t v___x_1874_; 
v___x_1871_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__8));
v___x_1872_ = lean_string_utf8_byte_size(v___y_1869_);
v___x_1873_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9);
v___x_1874_ = lean_nat_dec_le(v___x_1873_, v___x_1872_);
if (v___x_1874_ == 0)
{
v___y_1856_ = v___y_1866_;
v___y_1857_ = v___y_1868_;
v___y_1858_ = v___y_1867_;
v___y_1859_ = v___y_1869_;
goto v___jp_1855_;
}
else
{
uint8_t v___x_1875_; 
v___x_1875_ = lean_string_memcmp(v___y_1869_, v___x_1871_, v___x_1794_, v___x_1794_, v___x_1873_);
if (v___x_1875_ == 0)
{
v___y_1856_ = v___y_1866_;
v___y_1857_ = v___y_1868_;
v___y_1858_ = v___y_1867_;
v___y_1859_ = v___y_1869_;
goto v___jp_1855_;
}
else
{
lean_dec_ref(v___y_1869_);
v___y_1785_ = v___y_1866_;
v___y_1786_ = v___y_1867_;
v___y_1787_ = v___y_1868_;
goto v___jp_1784_;
}
}
}
else
{
lean_dec_ref(v___y_1869_);
v___y_1785_ = v___y_1866_;
v___y_1786_ = v___y_1867_;
v___y_1787_ = v___y_1868_;
goto v___jp_1784_;
}
}
v___jp_1876_:
{
switch(lean_obj_tag(v_snd_1767_))
{
case 6:
{
lean_object* v_val_1880_; lean_object* v___x_1882_; uint8_t v_isShared_1883_; uint8_t v_isSharedCheck_1888_; 
lean_dec(v___y_1878_);
v_val_1880_ = lean_ctor_get(v_snd_1767_, 0);
v_isSharedCheck_1888_ = !lean_is_exclusive(v_snd_1767_);
if (v_isSharedCheck_1888_ == 0)
{
v___x_1882_ = v_snd_1767_;
v_isShared_1883_ = v_isSharedCheck_1888_;
goto v_resetjp_1881_;
}
else
{
lean_inc(v_val_1880_);
lean_dec(v_snd_1767_);
v___x_1882_ = lean_box(0);
v_isShared_1883_ = v_isSharedCheck_1888_;
goto v_resetjp_1881_;
}
v_resetjp_1881_:
{
lean_object* v_induct_1884_; lean_object* v___x_1886_; 
v_induct_1884_ = lean_ctor_get(v_val_1880_, 1);
lean_inc(v_induct_1884_);
lean_dec_ref(v_val_1880_);
if (v_isShared_1883_ == 0)
{
lean_ctor_set_tag(v___x_1882_, 2);
lean_ctor_set(v___x_1882_, 0, v_induct_1884_);
v___x_1886_ = v___x_1882_;
goto v_reusejp_1885_;
}
else
{
lean_object* v_reuseFailAlloc_1887_; 
v_reuseFailAlloc_1887_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1887_, 0, v_induct_1884_);
v___x_1886_ = v_reuseFailAlloc_1887_;
goto v_reusejp_1885_;
}
v_reusejp_1885_:
{
v_c_1769_ = v___x_1886_;
goto v___jp_1768_;
}
}
}
case 7:
{
lean_object* v___x_1890_; uint8_t v_isShared_1891_; uint8_t v_isSharedCheck_1895_; 
v_isSharedCheck_1895_ = !lean_is_exclusive(v_snd_1767_);
if (v_isSharedCheck_1895_ == 0)
{
lean_object* v_unused_1896_; 
v_unused_1896_ = lean_ctor_get(v_snd_1767_, 0);
lean_dec(v_unused_1896_);
v___x_1890_ = v_snd_1767_;
v_isShared_1891_ = v_isSharedCheck_1895_;
goto v_resetjp_1889_;
}
else
{
lean_dec(v_snd_1767_);
v___x_1890_ = lean_box(0);
v_isShared_1891_ = v_isSharedCheck_1895_;
goto v_resetjp_1889_;
}
v_resetjp_1889_:
{
lean_object* v___x_1893_; 
if (v_isShared_1891_ == 0)
{
lean_ctor_set_tag(v___x_1890_, 3);
lean_ctor_set(v___x_1890_, 0, v___y_1878_);
v___x_1893_ = v___x_1890_;
goto v_reusejp_1892_;
}
else
{
lean_object* v_reuseFailAlloc_1894_; 
v_reuseFailAlloc_1894_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1894_, 0, v___y_1878_);
v___x_1893_ = v_reuseFailAlloc_1894_;
goto v_reusejp_1892_;
}
v_reusejp_1892_:
{
v_c_1769_ = v___x_1893_;
goto v___jp_1768_;
}
}
}
case 4:
{
lean_object* v___x_1897_; 
lean_dec_ref_known(v_snd_1767_, 1);
lean_dec(v___y_1878_);
v___x_1897_ = lean_box(4);
v_c_1769_ = v___x_1897_;
goto v___jp_1768_;
}
default: 
{
lean_object* v___x_1898_; lean_object* v___x_1899_; lean_object* v___x_1900_; lean_object* v___x_1901_; lean_object* v___x_1902_; uint8_t v___x_1903_; 
v___x_1898_ = ((lean_object*)(l_NsExport_droppedTypeHeads));
v___x_1899_ = l_Lean_ConstantInfo_type(v_snd_1767_);
lean_dec(v_snd_1767_);
v___x_1900_ = l_Lean_Expr_getForallBody(v___x_1899_);
lean_dec_ref(v___x_1899_);
v___x_1901_ = l_Lean_Expr_getAppFn(v___x_1900_);
lean_dec_ref(v___x_1900_);
v___x_1902_ = l_Lean_Expr_constName(v___x_1901_);
lean_dec_ref(v___x_1901_);
v___x_1903_ = l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(v___x_1902_, v___x_1898_);
lean_dec(v___x_1902_);
if (v___x_1903_ == 0)
{
lean_object* v___x_1904_; 
lean_inc(v_fst_1766_);
lean_inc_ref(v_a_1756_);
v___x_1904_ = l_Lean_Environment_getProjectionFnInfo_x3f(v_a_1756_, v_fst_1766_);
if (lean_obj_tag(v___x_1904_) == 1)
{
lean_object* v_val_1905_; lean_object* v_ctorName_1906_; 
lean_dec(v___y_1878_);
v_val_1905_ = lean_ctor_get(v___x_1904_, 0);
lean_inc(v_val_1905_);
lean_dec_ref_known(v___x_1904_, 1);
v_ctorName_1906_ = lean_ctor_get(v_val_1905_, 0);
lean_inc(v_ctorName_1906_);
lean_dec(v_val_1905_);
if (lean_obj_tag(v_ctorName_1906_) == 0)
{
v___y_1775_ = v_ctorName_1906_;
goto v___jp_1774_;
}
else
{
lean_object* v_pre_1907_; 
v_pre_1907_ = lean_ctor_get(v_ctorName_1906_, 0);
lean_inc(v_pre_1907_);
lean_dec(v_ctorName_1906_);
v___y_1775_ = v_pre_1907_;
goto v___jp_1774_;
}
}
else
{
uint8_t v___x_1908_; 
lean_dec(v___x_1904_);
v___x_1908_ = l_Lean_Name_hasMacroScopes(v_fst_1766_);
if (v___x_1908_ == 0)
{
uint8_t v___x_1909_; 
lean_inc(v_fst_1766_);
lean_inc_ref(v_a_1756_);
v___x_1909_ = l_Lean_Meta_isMatcherCore(v_a_1756_, v_fst_1766_);
if (v___x_1909_ == 0)
{
uint8_t v___x_1910_; 
lean_inc(v_fst_1766_);
lean_inc_ref(v_a_1756_);
v___x_1910_ = l_Lean_isAuxRecursor(v_a_1756_, v_fst_1766_);
if (v___x_1910_ == 0)
{
uint8_t v___x_1911_; 
lean_inc(v_fst_1766_);
lean_inc_ref(v_a_1756_);
v___x_1911_ = l_Lean_isNoConfusion(v_a_1756_, v_fst_1766_);
if (v___x_1911_ == 0)
{
switch(lean_obj_tag(v_fst_1766_))
{
case 0:
{
lean_object* v___x_1912_; 
lean_dec(v___y_1878_);
v___x_1912_ = lean_box(4);
v_c_1769_ = v___x_1912_;
goto v___jp_1768_;
}
case 1:
{
lean_object* v_str_1913_; lean_object* v___x_1914_; lean_object* v___x_1915_; lean_object* v___x_1916_; uint8_t v___x_1917_; 
v_str_1913_ = lean_ctor_get(v_fst_1766_, 1);
v___x_1914_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__10));
v___x_1915_ = lean_string_utf8_byte_size(v_str_1913_);
v___x_1916_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11);
v___x_1917_ = lean_nat_dec_le(v___x_1916_, v___x_1915_);
if (v___x_1917_ == 0)
{
lean_inc_ref(v_str_1913_);
v___y_1866_ = v___y_1879_;
v___y_1867_ = v___y_1878_;
v___y_1868_ = v___y_1877_;
v___y_1869_ = v_str_1913_;
v___y_1870_ = v___x_1911_;
goto v___jp_1865_;
}
else
{
uint8_t v___x_1918_; 
v___x_1918_ = lean_string_memcmp(v_str_1913_, v___x_1914_, v___x_1794_, v___x_1794_, v___x_1916_);
lean_inc_ref(v_str_1913_);
v___y_1866_ = v___y_1879_;
v___y_1867_ = v___y_1878_;
v___y_1868_ = v___y_1877_;
v___y_1869_ = v_str_1913_;
v___y_1870_ = v___x_1918_;
goto v___jp_1865_;
}
}
default: 
{
if (v___y_1877_ == 0)
{
lean_dec(v___y_1878_);
if (v___y_1879_ == 0)
{
lean_object* v___x_1919_; 
v___x_1919_ = lean_box(6);
v_c_1769_ = v___x_1919_;
goto v___jp_1768_;
}
else
{
lean_object* v___x_1920_; 
v___x_1920_ = lean_box(5);
v_c_1769_ = v___x_1920_;
goto v___jp_1768_;
}
}
else
{
lean_object* v___x_1921_; 
v___x_1921_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_1921_, 0, v___y_1878_);
v_c_1769_ = v___x_1921_;
goto v___jp_1768_;
}
}
}
}
else
{
v___y_1780_ = v___y_1879_;
v___y_1781_ = v___y_1878_;
goto v___jp_1779_;
}
}
else
{
v___y_1780_ = v___y_1879_;
v___y_1781_ = v___y_1878_;
goto v___jp_1779_;
}
}
else
{
if (v___y_1877_ == 0)
{
lean_dec(v___y_1878_);
if (v___y_1879_ == 0)
{
lean_object* v___x_1922_; 
v___x_1922_ = lean_box(6);
v_c_1769_ = v___x_1922_;
goto v___jp_1768_;
}
else
{
lean_object* v___x_1923_; 
v___x_1923_ = lean_box(5);
v_c_1769_ = v___x_1923_;
goto v___jp_1768_;
}
}
else
{
lean_object* v___x_1924_; 
v___x_1924_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_1924_, 0, v___y_1878_);
v_c_1769_ = v___x_1924_;
goto v___jp_1768_;
}
}
}
else
{
lean_object* v___x_1925_; 
lean_dec(v___y_1878_);
v___x_1925_ = lean_box(6);
v_c_1769_ = v___x_1925_;
goto v___jp_1768_;
}
}
}
else
{
lean_object* v___x_1926_; 
lean_dec(v___y_1878_);
v___x_1926_ = lean_box(4);
v_c_1769_ = v___x_1926_;
goto v___jp_1768_;
}
}
}
}
v___jp_1927_:
{
uint8_t v___x_1930_; 
lean_inc(v___y_1928_);
lean_inc_ref(v_a_1756_);
v___x_1930_ = l_Lean_Environment_contains(v_a_1756_, v___y_1928_, v___x_1763_);
v___y_1877_ = v___y_1929_;
v___y_1878_ = v___y_1928_;
v___y_1879_ = v___x_1930_;
goto v___jp_1876_;
}
v___jp_1931_:
{
lean_object* v___x_1933_; 
v___x_1933_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_1756_, v___y_1932_);
if (lean_obj_tag(v___x_1933_) == 0)
{
v___y_1928_ = v___y_1932_;
v___y_1929_ = v___x_1802_;
goto v___jp_1927_;
}
else
{
lean_object* v_val_1934_; lean_object* v___x_1935_; lean_object* v___x_1936_; uint8_t v___x_1937_; 
v_val_1934_ = lean_ctor_get(v___x_1933_, 0);
lean_inc(v_val_1934_);
lean_dec_ref_known(v___x_1933_, 1);
v___x_1935_ = lean_box(v___x_1802_);
v___x_1936_ = lean_array_get(v___x_1935_, v___x_1757_, v_val_1934_);
lean_dec(v_val_1934_);
lean_dec(v___x_1935_);
v___x_1937_ = lean_unbox(v___x_1936_);
if (v___x_1937_ == 0)
{
uint8_t v___x_1938_; 
v___x_1938_ = lean_unbox(v___x_1936_);
lean_dec(v___x_1936_);
v___y_1928_ = v___y_1932_;
v___y_1929_ = v___x_1938_;
goto v___jp_1927_;
}
else
{
uint8_t v___x_1939_; 
v___x_1939_ = lean_unbox(v___x_1936_);
lean_dec(v___x_1936_);
v___y_1877_ = v___x_1939_;
v___y_1878_ = v___y_1932_;
v___y_1879_ = v___x_1802_;
goto v___jp_1876_;
}
}
}
v___jp_1940_:
{
uint8_t v___x_1942_; 
lean_inc(v___y_1941_);
lean_inc_ref(v_a_1756_);
v___x_1942_ = l_Lean_Environment_contains(v_a_1756_, v___y_1941_, v___x_1763_);
if (v___x_1942_ == 0)
{
uint8_t v___x_1943_; 
v___x_1943_ = l_Lean_isPrivateName(v___y_1941_);
if (v___x_1943_ == 0)
{
v___y_1932_ = v___y_1941_;
goto v___jp_1931_;
}
else
{
lean_object* v___x_1944_; uint8_t v___x_1945_; 
lean_inc(v___y_1941_);
v___x_1944_ = l_Lean_privateToUserName(v___y_1941_);
lean_inc(v___x_1944_);
lean_inc_ref(v_a_1756_);
v___x_1945_ = l_Lean_Environment_contains(v_a_1756_, v___x_1944_, v___x_1763_);
if (v___x_1945_ == 0)
{
lean_dec(v___x_1944_);
v___y_1932_ = v___y_1941_;
goto v___jp_1931_;
}
else
{
lean_dec(v___y_1941_);
v___y_1932_ = v___x_1944_;
goto v___jp_1931_;
}
}
}
else
{
v___y_1932_ = v___y_1941_;
goto v___jp_1931_;
}
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___boxed(lean_object* v_a_1947_, lean_object* v___x_1948_, lean_object* v_as_1949_, lean_object* v_sz_1950_, lean_object* v_i_1951_, lean_object* v_b_1952_, lean_object* v___y_1953_){
_start:
{
size_t v_sz_boxed_1954_; size_t v_i_boxed_1955_; lean_object* v_res_1956_; 
v_sz_boxed_1954_ = lean_unbox_usize(v_sz_1950_);
lean_dec(v_sz_1950_);
v_i_boxed_1955_ = lean_unbox_usize(v_i_1951_);
lean_dec(v_i_1951_);
v_res_1956_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15(v_a_1947_, v___x_1948_, v_as_1949_, v_sz_boxed_1954_, v_i_boxed_1955_, v_b_1952_);
lean_dec_ref(v_as_1949_);
lean_dec_ref(v___x_1948_);
return v_res_1956_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11(lean_object* v_a_1957_, lean_object* v___x_1958_, lean_object* v_as_1959_, size_t v_sz_1960_, size_t v_i_1961_, lean_object* v_b_1962_){
_start:
{
uint8_t v___x_1964_; 
v___x_1964_ = lean_usize_dec_lt(v_i_1961_, v_sz_1960_);
if (v___x_1964_ == 0)
{
lean_object* v___x_1965_; 
lean_dec_ref(v_a_1957_);
v___x_1965_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1965_, 0, v_b_1962_);
return v___x_1965_;
}
else
{
lean_object* v_a_1966_; lean_object* v_fst_1967_; lean_object* v_snd_1968_; lean_object* v_c_1970_; uint8_t v___y_1978_; lean_object* v___y_1979_; uint8_t v___y_1980_; lean_object* v___y_1985_; uint8_t v___y_1986_; lean_object* v___y_1992_; uint8_t v___x_1994_; lean_object* v___x_1995_; lean_object* v___x_1996_; lean_object* v___x_1997_; lean_object* v___x_1998_; lean_object* v___x_1999_; lean_object* v___x_2000_; lean_object* v___x_2001_; lean_object* v___x_2002_; lean_object* v___x_2003_; lean_object* v___x_2004_; uint8_t v___y_2006_; lean_object* v___y_2007_; uint8_t v___y_2008_; uint8_t v___y_2009_; uint8_t v___y_2049_; lean_object* v___y_2050_; lean_object* v___y_2051_; uint8_t v___y_2052_; uint8_t v___y_2057_; lean_object* v___y_2058_; lean_object* v___y_2059_; uint8_t v___y_2060_; uint8_t v___y_2067_; lean_object* v___y_2068_; lean_object* v___y_2069_; uint8_t v___y_2070_; uint8_t v___y_2071_; uint8_t v___y_2078_; lean_object* v___y_2079_; uint8_t v___y_2080_; lean_object* v___y_2129_; uint8_t v___y_2130_; lean_object* v___y_2133_; lean_object* v___y_2142_; 
v_a_1966_ = lean_array_uget_borrowed(v_as_1959_, v_i_1961_);
v_fst_1967_ = lean_ctor_get(v_a_1966_, 0);
v_snd_1968_ = lean_ctor_get(v_a_1966_, 1);
lean_inc(v_snd_1968_);
v___x_1994_ = 0;
v___x_1995_ = lean_unsigned_to_nat(1u);
v___x_1996_ = lean_unsigned_to_nat(0u);
v___x_1997_ = lean_box(0);
v___x_1998_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_1999_ = l_Lean_instInhabitedFileMap_default;
v___x_2000_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_2001_ = lean_box(0);
v___x_2002_ = lean_box(0);
v___x_2003_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_2004_ = lean_box(0);
if (lean_obj_tag(v_fst_1967_) == 0)
{
v___y_2142_ = v_fst_1967_;
goto v___jp_2141_;
}
else
{
lean_object* v_pre_2147_; 
v_pre_2147_ = lean_ctor_get(v_fst_1967_, 0);
lean_inc(v_pre_2147_);
v___y_2142_ = v_pre_2147_;
goto v___jp_2141_;
}
v___jp_1969_:
{
lean_object* v___x_1971_; size_t v___x_1972_; size_t v___x_1973_; lean_object* v___x_1974_; 
lean_inc(v_fst_1967_);
v___x_1971_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_b_1962_, v_fst_1967_, v_c_1970_);
v___x_1972_ = ((size_t)1ULL);
v___x_1973_ = lean_usize_add(v_i_1961_, v___x_1972_);
v___x_1974_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15(v_a_1957_, v___x_1958_, v_as_1959_, v_sz_1960_, v___x_1973_, v___x_1971_);
return v___x_1974_;
}
v___jp_1975_:
{
lean_object* v___x_1976_; 
v___x_1976_ = lean_box(0);
v_c_1970_ = v___x_1976_;
goto v___jp_1969_;
}
v___jp_1977_:
{
if (v___y_1978_ == 0)
{
lean_dec(v___y_1979_);
if (v___y_1980_ == 0)
{
lean_object* v___x_1981_; 
v___x_1981_ = lean_box(6);
v_c_1970_ = v___x_1981_;
goto v___jp_1969_;
}
else
{
lean_object* v___x_1982_; 
v___x_1982_ = lean_box(5);
v_c_1970_ = v___x_1982_;
goto v___jp_1969_;
}
}
else
{
lean_object* v___x_1983_; 
v___x_1983_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_1983_, 0, v___y_1979_);
v_c_1970_ = v___x_1983_;
goto v___jp_1969_;
}
}
v___jp_1984_:
{
if (v___y_1986_ == 0)
{
lean_object* v___x_1987_; 
v___x_1987_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1987_, 0, v___y_1985_);
v_c_1970_ = v___x_1987_;
goto v___jp_1969_;
}
else
{
lean_object* v___x_1988_; 
lean_dec(v___y_1985_);
v___x_1988_ = lean_box(5);
v_c_1970_ = v___x_1988_;
goto v___jp_1969_;
}
}
v___jp_1989_:
{
lean_object* v___x_1990_; 
v___x_1990_ = lean_box(0);
v_c_1970_ = v___x_1990_;
goto v___jp_1969_;
}
v___jp_1991_:
{
lean_object* v___x_1993_; 
v___x_1993_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1993_, 0, v___y_1992_);
v_c_1970_ = v___x_1993_;
goto v___jp_1969_;
}
v___jp_2005_:
{
if (v___y_2009_ == 0)
{
lean_dec(v___y_2007_);
goto v___jp_1989_;
}
else
{
if (v___y_2008_ == 0)
{
if (v___y_2006_ == 0)
{
lean_dec(v___y_2007_);
goto v___jp_1989_;
}
else
{
lean_object* v___x_2010_; 
lean_inc(v_fst_1967_);
lean_inc_ref(v_a_1957_);
v___x_2010_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0(v___x_1996_, v___x_1995_, v___x_1997_, v___x_1964_, v_a_1957_, v___x_2000_, v___x_1998_, v___x_1999_, v___x_2001_, v___x_2002_, v___x_2003_, v___x_2004_, v___x_1994_, v_fst_1967_);
if (lean_obj_tag(v___x_2010_) == 0)
{
lean_object* v_a_2011_; lean_object* v___x_2012_; 
v_a_2011_ = lean_ctor_get(v___x_2010_, 0);
lean_inc(v_a_2011_);
lean_dec_ref_known(v___x_2010_, 1);
lean_inc(v___y_2007_);
lean_inc_ref(v_a_1957_);
v___x_2012_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0(v___x_1996_, v___x_1995_, v___x_1997_, v___x_1964_, v_a_1957_, v___x_2000_, v___x_1998_, v___x_1999_, v___x_2001_, v___x_2002_, v___x_2003_, v___x_2004_, v___x_1994_, v___y_2007_);
if (lean_obj_tag(v___x_2012_) == 0)
{
if (lean_obj_tag(v_a_2011_) == 0)
{
lean_object* v___x_2013_; 
lean_dec_ref_known(v___x_2012_, 1);
v___x_2013_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_2013_, 0, v___y_2007_);
v_c_1970_ = v___x_2013_;
goto v___jp_1969_;
}
else
{
lean_object* v_a_2014_; 
v_a_2014_ = lean_ctor_get(v___x_2012_, 0);
lean_inc(v_a_2014_);
lean_dec_ref_known(v___x_2012_, 1);
if (lean_obj_tag(v_a_2014_) == 0)
{
lean_object* v___x_2015_; 
lean_dec_ref_known(v_a_2011_, 1);
lean_dec(v___y_2007_);
v___x_2015_ = lean_box(0);
v_c_1970_ = v___x_2015_;
goto v___jp_1969_;
}
else
{
lean_object* v_val_2016_; lean_object* v_val_2017_; lean_object* v___x_2019_; uint8_t v_isShared_2020_; uint8_t v_isSharedCheck_2030_; 
v_val_2016_ = lean_ctor_get(v_a_2011_, 0);
lean_inc(v_val_2016_);
lean_dec_ref_known(v_a_2011_, 1);
v_val_2017_ = lean_ctor_get(v_a_2014_, 0);
v_isSharedCheck_2030_ = !lean_is_exclusive(v_a_2014_);
if (v_isSharedCheck_2030_ == 0)
{
v___x_2019_ = v_a_2014_;
v_isShared_2020_ = v_isSharedCheck_2030_;
goto v_resetjp_2018_;
}
else
{
lean_inc(v_val_2017_);
lean_dec(v_a_2014_);
v___x_2019_ = lean_box(0);
v_isShared_2020_ = v_isSharedCheck_2030_;
goto v_resetjp_2018_;
}
v_resetjp_2018_:
{
lean_object* v_pos_2021_; lean_object* v_endPos_2022_; lean_object* v_pos_2023_; lean_object* v_endPos_2024_; uint8_t v___x_2025_; 
v_pos_2021_ = lean_ctor_get(v_val_2016_, 0);
lean_inc_ref(v_pos_2021_);
v_endPos_2022_ = lean_ctor_get(v_val_2016_, 2);
lean_inc_ref(v_endPos_2022_);
lean_dec(v_val_2016_);
v_pos_2023_ = lean_ctor_get(v_val_2017_, 0);
lean_inc_ref(v_pos_2023_);
v_endPos_2024_ = lean_ctor_get(v_val_2017_, 2);
lean_inc_ref(v_endPos_2024_);
lean_dec(v_val_2017_);
v___x_2025_ = l_Lean_instDecidableEqPosition_decEq(v_pos_2021_, v_pos_2023_);
lean_dec_ref(v_pos_2023_);
lean_dec_ref(v_pos_2021_);
if (v___x_2025_ == 0)
{
lean_dec_ref(v_endPos_2024_);
lean_dec_ref(v_endPos_2022_);
lean_del_object(v___x_2019_);
lean_dec(v___y_2007_);
goto v___jp_1975_;
}
else
{
uint8_t v___x_2026_; 
v___x_2026_ = l_Lean_instDecidableEqPosition_decEq(v_endPos_2022_, v_endPos_2024_);
lean_dec_ref(v_endPos_2024_);
lean_dec_ref(v_endPos_2022_);
if (v___x_2026_ == 0)
{
lean_del_object(v___x_2019_);
lean_dec(v___y_2007_);
goto v___jp_1975_;
}
else
{
lean_object* v___x_2028_; 
if (v_isShared_2020_ == 0)
{
lean_ctor_set_tag(v___x_2019_, 3);
lean_ctor_set(v___x_2019_, 0, v___y_2007_);
v___x_2028_ = v___x_2019_;
goto v_reusejp_2027_;
}
else
{
lean_object* v_reuseFailAlloc_2029_; 
v_reuseFailAlloc_2029_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2029_, 0, v___y_2007_);
v___x_2028_ = v_reuseFailAlloc_2029_;
goto v_reusejp_2027_;
}
v_reusejp_2027_:
{
v_c_1970_ = v___x_2028_;
goto v___jp_1969_;
}
}
}
}
}
}
}
else
{
lean_object* v_a_2031_; lean_object* v___x_2033_; uint8_t v_isShared_2034_; uint8_t v_isSharedCheck_2038_; 
lean_dec(v_a_2011_);
lean_dec(v___y_2007_);
lean_dec_ref(v_b_1962_);
lean_dec_ref(v_a_1957_);
v_a_2031_ = lean_ctor_get(v___x_2012_, 0);
v_isSharedCheck_2038_ = !lean_is_exclusive(v___x_2012_);
if (v_isSharedCheck_2038_ == 0)
{
v___x_2033_ = v___x_2012_;
v_isShared_2034_ = v_isSharedCheck_2038_;
goto v_resetjp_2032_;
}
else
{
lean_inc(v_a_2031_);
lean_dec(v___x_2012_);
v___x_2033_ = lean_box(0);
v_isShared_2034_ = v_isSharedCheck_2038_;
goto v_resetjp_2032_;
}
v_resetjp_2032_:
{
lean_object* v___x_2036_; 
if (v_isShared_2034_ == 0)
{
v___x_2036_ = v___x_2033_;
goto v_reusejp_2035_;
}
else
{
lean_object* v_reuseFailAlloc_2037_; 
v_reuseFailAlloc_2037_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2037_, 0, v_a_2031_);
v___x_2036_ = v_reuseFailAlloc_2037_;
goto v_reusejp_2035_;
}
v_reusejp_2035_:
{
return v___x_2036_;
}
}
}
}
else
{
lean_object* v_a_2039_; lean_object* v___x_2041_; uint8_t v_isShared_2042_; uint8_t v_isSharedCheck_2046_; 
lean_dec(v___y_2007_);
lean_dec_ref(v_b_1962_);
lean_dec_ref(v_a_1957_);
v_a_2039_ = lean_ctor_get(v___x_2010_, 0);
v_isSharedCheck_2046_ = !lean_is_exclusive(v___x_2010_);
if (v_isSharedCheck_2046_ == 0)
{
v___x_2041_ = v___x_2010_;
v_isShared_2042_ = v_isSharedCheck_2046_;
goto v_resetjp_2040_;
}
else
{
lean_inc(v_a_2039_);
lean_dec(v___x_2010_);
v___x_2041_ = lean_box(0);
v_isShared_2042_ = v_isSharedCheck_2046_;
goto v_resetjp_2040_;
}
v_resetjp_2040_:
{
lean_object* v___x_2044_; 
if (v_isShared_2042_ == 0)
{
v___x_2044_ = v___x_2041_;
goto v_reusejp_2043_;
}
else
{
lean_object* v_reuseFailAlloc_2045_; 
v_reuseFailAlloc_2045_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2045_, 0, v_a_2039_);
v___x_2044_ = v_reuseFailAlloc_2045_;
goto v_reusejp_2043_;
}
v_reusejp_2043_:
{
return v___x_2044_;
}
}
}
}
}
else
{
lean_object* v___x_2047_; 
lean_dec(v___y_2007_);
v___x_2047_ = lean_box(5);
v_c_1970_ = v___x_2047_;
goto v___jp_1969_;
}
}
}
v___jp_2048_:
{
lean_object* v___x_2053_; uint8_t v___x_2054_; 
v___x_2053_ = ((lean_object*)(l_NsExport_softNames));
v___x_2054_ = l_List_elem___at___00Lean_Linter_List_indexLinter_spec__1(v___y_2051_, v___x_2053_);
if (v___x_2054_ == 0)
{
uint8_t v___x_2055_; 
v___x_2055_ = l_NsExport_isEqNum(v___y_2051_);
v___y_2006_ = v___y_2049_;
v___y_2007_ = v___y_2050_;
v___y_2008_ = v___y_2052_;
v___y_2009_ = v___x_2055_;
goto v___jp_2005_;
}
else
{
lean_dec_ref(v___y_2051_);
v___y_2006_ = v___y_2049_;
v___y_2007_ = v___y_2050_;
v___y_2008_ = v___y_2052_;
v___y_2009_ = v___x_1964_;
goto v___jp_2005_;
}
}
v___jp_2056_:
{
lean_object* v___x_2061_; lean_object* v___x_2062_; lean_object* v___x_2063_; uint8_t v___x_2064_; 
v___x_2061_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__6));
v___x_2062_ = lean_string_utf8_byte_size(v___y_2059_);
v___x_2063_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__7);
v___x_2064_ = lean_nat_dec_le(v___x_2063_, v___x_2062_);
if (v___x_2064_ == 0)
{
v___y_2049_ = v___y_2057_;
v___y_2050_ = v___y_2058_;
v___y_2051_ = v___y_2059_;
v___y_2052_ = v___y_2060_;
goto v___jp_2048_;
}
else
{
uint8_t v___x_2065_; 
v___x_2065_ = lean_string_memcmp(v___y_2059_, v___x_2061_, v___x_1996_, v___x_1996_, v___x_2063_);
if (v___x_2065_ == 0)
{
v___y_2049_ = v___y_2057_;
v___y_2050_ = v___y_2058_;
v___y_2051_ = v___y_2059_;
v___y_2052_ = v___y_2060_;
goto v___jp_2048_;
}
else
{
lean_dec_ref(v___y_2059_);
v___y_1978_ = v___y_2057_;
v___y_1979_ = v___y_2058_;
v___y_1980_ = v___y_2060_;
goto v___jp_1977_;
}
}
}
v___jp_2066_:
{
if (v___y_2071_ == 0)
{
lean_object* v___x_2072_; lean_object* v___x_2073_; lean_object* v___x_2074_; uint8_t v___x_2075_; 
v___x_2072_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__8));
v___x_2073_ = lean_string_utf8_byte_size(v___y_2069_);
v___x_2074_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__9);
v___x_2075_ = lean_nat_dec_le(v___x_2074_, v___x_2073_);
if (v___x_2075_ == 0)
{
v___y_2057_ = v___y_2067_;
v___y_2058_ = v___y_2068_;
v___y_2059_ = v___y_2069_;
v___y_2060_ = v___y_2070_;
goto v___jp_2056_;
}
else
{
uint8_t v___x_2076_; 
v___x_2076_ = lean_string_memcmp(v___y_2069_, v___x_2072_, v___x_1996_, v___x_1996_, v___x_2074_);
if (v___x_2076_ == 0)
{
v___y_2057_ = v___y_2067_;
v___y_2058_ = v___y_2068_;
v___y_2059_ = v___y_2069_;
v___y_2060_ = v___y_2070_;
goto v___jp_2056_;
}
else
{
lean_dec_ref(v___y_2069_);
v___y_1978_ = v___y_2067_;
v___y_1979_ = v___y_2068_;
v___y_1980_ = v___y_2070_;
goto v___jp_1977_;
}
}
}
else
{
lean_dec_ref(v___y_2069_);
v___y_1978_ = v___y_2067_;
v___y_1979_ = v___y_2068_;
v___y_1980_ = v___y_2070_;
goto v___jp_1977_;
}
}
v___jp_2077_:
{
switch(lean_obj_tag(v_snd_1968_))
{
case 6:
{
lean_object* v_val_2081_; lean_object* v___x_2083_; uint8_t v_isShared_2084_; uint8_t v_isSharedCheck_2089_; 
lean_dec(v___y_2079_);
v_val_2081_ = lean_ctor_get(v_snd_1968_, 0);
v_isSharedCheck_2089_ = !lean_is_exclusive(v_snd_1968_);
if (v_isSharedCheck_2089_ == 0)
{
v___x_2083_ = v_snd_1968_;
v_isShared_2084_ = v_isSharedCheck_2089_;
goto v_resetjp_2082_;
}
else
{
lean_inc(v_val_2081_);
lean_dec(v_snd_1968_);
v___x_2083_ = lean_box(0);
v_isShared_2084_ = v_isSharedCheck_2089_;
goto v_resetjp_2082_;
}
v_resetjp_2082_:
{
lean_object* v_induct_2085_; lean_object* v___x_2087_; 
v_induct_2085_ = lean_ctor_get(v_val_2081_, 1);
lean_inc(v_induct_2085_);
lean_dec_ref(v_val_2081_);
if (v_isShared_2084_ == 0)
{
lean_ctor_set_tag(v___x_2083_, 2);
lean_ctor_set(v___x_2083_, 0, v_induct_2085_);
v___x_2087_ = v___x_2083_;
goto v_reusejp_2086_;
}
else
{
lean_object* v_reuseFailAlloc_2088_; 
v_reuseFailAlloc_2088_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2088_, 0, v_induct_2085_);
v___x_2087_ = v_reuseFailAlloc_2088_;
goto v_reusejp_2086_;
}
v_reusejp_2086_:
{
v_c_1970_ = v___x_2087_;
goto v___jp_1969_;
}
}
}
case 7:
{
lean_object* v___x_2091_; uint8_t v_isShared_2092_; uint8_t v_isSharedCheck_2096_; 
v_isSharedCheck_2096_ = !lean_is_exclusive(v_snd_1968_);
if (v_isSharedCheck_2096_ == 0)
{
lean_object* v_unused_2097_; 
v_unused_2097_ = lean_ctor_get(v_snd_1968_, 0);
lean_dec(v_unused_2097_);
v___x_2091_ = v_snd_1968_;
v_isShared_2092_ = v_isSharedCheck_2096_;
goto v_resetjp_2090_;
}
else
{
lean_dec(v_snd_1968_);
v___x_2091_ = lean_box(0);
v_isShared_2092_ = v_isSharedCheck_2096_;
goto v_resetjp_2090_;
}
v_resetjp_2090_:
{
lean_object* v___x_2094_; 
if (v_isShared_2092_ == 0)
{
lean_ctor_set_tag(v___x_2091_, 3);
lean_ctor_set(v___x_2091_, 0, v___y_2079_);
v___x_2094_ = v___x_2091_;
goto v_reusejp_2093_;
}
else
{
lean_object* v_reuseFailAlloc_2095_; 
v_reuseFailAlloc_2095_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2095_, 0, v___y_2079_);
v___x_2094_ = v_reuseFailAlloc_2095_;
goto v_reusejp_2093_;
}
v_reusejp_2093_:
{
v_c_1970_ = v___x_2094_;
goto v___jp_1969_;
}
}
}
case 4:
{
lean_object* v___x_2098_; 
lean_dec_ref_known(v_snd_1968_, 1);
lean_dec(v___y_2079_);
v___x_2098_ = lean_box(4);
v_c_1970_ = v___x_2098_;
goto v___jp_1969_;
}
default: 
{
lean_object* v___x_2099_; lean_object* v___x_2100_; lean_object* v___x_2101_; lean_object* v___x_2102_; lean_object* v___x_2103_; uint8_t v___x_2104_; 
v___x_2099_ = ((lean_object*)(l_NsExport_droppedTypeHeads));
v___x_2100_ = l_Lean_ConstantInfo_type(v_snd_1968_);
lean_dec(v_snd_1968_);
v___x_2101_ = l_Lean_Expr_getForallBody(v___x_2100_);
lean_dec_ref(v___x_2100_);
v___x_2102_ = l_Lean_Expr_getAppFn(v___x_2101_);
lean_dec_ref(v___x_2101_);
v___x_2103_ = l_Lean_Expr_constName(v___x_2102_);
lean_dec_ref(v___x_2102_);
v___x_2104_ = l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(v___x_2103_, v___x_2099_);
lean_dec(v___x_2103_);
if (v___x_2104_ == 0)
{
lean_object* v___x_2105_; 
lean_inc(v_fst_1967_);
lean_inc_ref(v_a_1957_);
v___x_2105_ = l_Lean_Environment_getProjectionFnInfo_x3f(v_a_1957_, v_fst_1967_);
if (lean_obj_tag(v___x_2105_) == 1)
{
lean_object* v_val_2106_; lean_object* v_ctorName_2107_; 
lean_dec(v___y_2079_);
v_val_2106_ = lean_ctor_get(v___x_2105_, 0);
lean_inc(v_val_2106_);
lean_dec_ref_known(v___x_2105_, 1);
v_ctorName_2107_ = lean_ctor_get(v_val_2106_, 0);
lean_inc(v_ctorName_2107_);
lean_dec(v_val_2106_);
if (lean_obj_tag(v_ctorName_2107_) == 0)
{
v___y_1992_ = v_ctorName_2107_;
goto v___jp_1991_;
}
else
{
lean_object* v_pre_2108_; 
v_pre_2108_ = lean_ctor_get(v_ctorName_2107_, 0);
lean_inc(v_pre_2108_);
lean_dec(v_ctorName_2107_);
v___y_1992_ = v_pre_2108_;
goto v___jp_1991_;
}
}
else
{
uint8_t v___x_2109_; 
lean_dec(v___x_2105_);
v___x_2109_ = l_Lean_Name_hasMacroScopes(v_fst_1967_);
if (v___x_2109_ == 0)
{
uint8_t v___x_2110_; 
lean_inc(v_fst_1967_);
lean_inc_ref(v_a_1957_);
v___x_2110_ = l_Lean_Meta_isMatcherCore(v_a_1957_, v_fst_1967_);
if (v___x_2110_ == 0)
{
uint8_t v___x_2111_; 
lean_inc(v_fst_1967_);
lean_inc_ref(v_a_1957_);
v___x_2111_ = l_Lean_isAuxRecursor(v_a_1957_, v_fst_1967_);
if (v___x_2111_ == 0)
{
uint8_t v___x_2112_; 
lean_inc(v_fst_1967_);
lean_inc_ref(v_a_1957_);
v___x_2112_ = l_Lean_isNoConfusion(v_a_1957_, v_fst_1967_);
if (v___x_2112_ == 0)
{
switch(lean_obj_tag(v_fst_1967_))
{
case 0:
{
lean_object* v___x_2113_; 
lean_dec(v___y_2079_);
v___x_2113_ = lean_box(4);
v_c_1970_ = v___x_2113_;
goto v___jp_1969_;
}
case 1:
{
lean_object* v_str_2114_; lean_object* v___x_2115_; lean_object* v___x_2116_; lean_object* v___x_2117_; uint8_t v___x_2118_; 
v_str_2114_ = lean_ctor_get(v_fst_1967_, 1);
v___x_2115_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__10));
v___x_2116_ = lean_string_utf8_byte_size(v_str_2114_);
v___x_2117_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__11);
v___x_2118_ = lean_nat_dec_le(v___x_2117_, v___x_2116_);
if (v___x_2118_ == 0)
{
lean_inc_ref(v_str_2114_);
v___y_2067_ = v___y_2078_;
v___y_2068_ = v___y_2079_;
v___y_2069_ = v_str_2114_;
v___y_2070_ = v___y_2080_;
v___y_2071_ = v___x_2112_;
goto v___jp_2066_;
}
else
{
uint8_t v___x_2119_; 
v___x_2119_ = lean_string_memcmp(v_str_2114_, v___x_2115_, v___x_1996_, v___x_1996_, v___x_2117_);
lean_inc_ref(v_str_2114_);
v___y_2067_ = v___y_2078_;
v___y_2068_ = v___y_2079_;
v___y_2069_ = v_str_2114_;
v___y_2070_ = v___y_2080_;
v___y_2071_ = v___x_2119_;
goto v___jp_2066_;
}
}
default: 
{
if (v___y_2078_ == 0)
{
lean_dec(v___y_2079_);
if (v___y_2080_ == 0)
{
lean_object* v___x_2120_; 
v___x_2120_ = lean_box(6);
v_c_1970_ = v___x_2120_;
goto v___jp_1969_;
}
else
{
lean_object* v___x_2121_; 
v___x_2121_ = lean_box(5);
v_c_1970_ = v___x_2121_;
goto v___jp_1969_;
}
}
else
{
lean_object* v___x_2122_; 
v___x_2122_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_2122_, 0, v___y_2079_);
v_c_1970_ = v___x_2122_;
goto v___jp_1969_;
}
}
}
}
else
{
v___y_1985_ = v___y_2079_;
v___y_1986_ = v___y_2080_;
goto v___jp_1984_;
}
}
else
{
v___y_1985_ = v___y_2079_;
v___y_1986_ = v___y_2080_;
goto v___jp_1984_;
}
}
else
{
if (v___y_2078_ == 0)
{
lean_dec(v___y_2079_);
if (v___y_2080_ == 0)
{
lean_object* v___x_2123_; 
v___x_2123_ = lean_box(6);
v_c_1970_ = v___x_2123_;
goto v___jp_1969_;
}
else
{
lean_object* v___x_2124_; 
v___x_2124_ = lean_box(5);
v_c_1970_ = v___x_2124_;
goto v___jp_1969_;
}
}
else
{
lean_object* v___x_2125_; 
v___x_2125_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_2125_, 0, v___y_2079_);
v_c_1970_ = v___x_2125_;
goto v___jp_1969_;
}
}
}
else
{
lean_object* v___x_2126_; 
lean_dec(v___y_2079_);
v___x_2126_ = lean_box(6);
v_c_1970_ = v___x_2126_;
goto v___jp_1969_;
}
}
}
else
{
lean_object* v___x_2127_; 
lean_dec(v___y_2079_);
v___x_2127_ = lean_box(4);
v_c_1970_ = v___x_2127_;
goto v___jp_1969_;
}
}
}
}
v___jp_2128_:
{
uint8_t v___x_2131_; 
lean_inc(v___y_2129_);
lean_inc_ref(v_a_1957_);
v___x_2131_ = l_Lean_Environment_contains(v_a_1957_, v___y_2129_, v___x_1964_);
v___y_2078_ = v___y_2130_;
v___y_2079_ = v___y_2129_;
v___y_2080_ = v___x_2131_;
goto v___jp_2077_;
}
v___jp_2132_:
{
lean_object* v___x_2134_; 
v___x_2134_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_1957_, v___y_2133_);
if (lean_obj_tag(v___x_2134_) == 0)
{
v___y_2129_ = v___y_2133_;
v___y_2130_ = v___x_1994_;
goto v___jp_2128_;
}
else
{
lean_object* v_val_2135_; lean_object* v___x_2136_; lean_object* v___x_2137_; uint8_t v___x_2138_; 
v_val_2135_ = lean_ctor_get(v___x_2134_, 0);
lean_inc(v_val_2135_);
lean_dec_ref_known(v___x_2134_, 1);
v___x_2136_ = lean_box(v___x_1994_);
v___x_2137_ = lean_array_get(v___x_2136_, v___x_1958_, v_val_2135_);
lean_dec(v_val_2135_);
lean_dec(v___x_2136_);
v___x_2138_ = lean_unbox(v___x_2137_);
if (v___x_2138_ == 0)
{
uint8_t v___x_2139_; 
v___x_2139_ = lean_unbox(v___x_2137_);
lean_dec(v___x_2137_);
v___y_2129_ = v___y_2133_;
v___y_2130_ = v___x_2139_;
goto v___jp_2128_;
}
else
{
uint8_t v___x_2140_; 
v___x_2140_ = lean_unbox(v___x_2137_);
lean_dec(v___x_2137_);
v___y_2078_ = v___x_2140_;
v___y_2079_ = v___y_2133_;
v___y_2080_ = v___x_1994_;
goto v___jp_2077_;
}
}
}
v___jp_2141_:
{
uint8_t v___x_2143_; 
lean_inc(v___y_2142_);
lean_inc_ref(v_a_1957_);
v___x_2143_ = l_Lean_Environment_contains(v_a_1957_, v___y_2142_, v___x_1964_);
if (v___x_2143_ == 0)
{
uint8_t v___x_2144_; 
v___x_2144_ = l_Lean_isPrivateName(v___y_2142_);
if (v___x_2144_ == 0)
{
v___y_2133_ = v___y_2142_;
goto v___jp_2132_;
}
else
{
lean_object* v___x_2145_; uint8_t v___x_2146_; 
lean_inc(v___y_2142_);
v___x_2145_ = l_Lean_privateToUserName(v___y_2142_);
lean_inc(v___x_2145_);
lean_inc_ref(v_a_1957_);
v___x_2146_ = l_Lean_Environment_contains(v_a_1957_, v___x_2145_, v___x_1964_);
if (v___x_2146_ == 0)
{
lean_dec(v___x_2145_);
v___y_2133_ = v___y_2142_;
goto v___jp_2132_;
}
else
{
lean_dec(v___y_2142_);
v___y_2133_ = v___x_2145_;
goto v___jp_2132_;
}
}
}
else
{
v___y_2133_ = v___y_2142_;
goto v___jp_2132_;
}
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___boxed(lean_object* v_a_2148_, lean_object* v___x_2149_, lean_object* v_as_2150_, lean_object* v_sz_2151_, lean_object* v_i_2152_, lean_object* v_b_2153_, lean_object* v___y_2154_){
_start:
{
size_t v_sz_boxed_2155_; size_t v_i_boxed_2156_; lean_object* v_res_2157_; 
v_sz_boxed_2155_ = lean_unbox_usize(v_sz_2151_);
lean_dec(v_sz_2151_);
v_i_boxed_2156_ = lean_unbox_usize(v_i_2152_);
lean_dec(v_i_2152_);
v_res_2157_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11(v_a_2148_, v___x_2149_, v_as_2150_, v_sz_boxed_2155_, v_i_boxed_2156_, v_b_2153_);
lean_dec_ref(v_as_2150_);
lean_dec_ref(v___x_2149_);
return v_res_2157_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__0(void){
_start:
{
lean_object* v___x_2158_; 
v___x_2158_ = l_Lean_PersistentHashMap_mkEmptyEntriesArray(lean_box(0), lean_box(0));
return v___x_2158_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1(void){
_start:
{
lean_object* v___x_2159_; lean_object* v___x_2160_; 
v___x_2159_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__0);
v___x_2160_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2160_, 0, v___x_2159_);
return v___x_2160_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__2(void){
_start:
{
lean_object* v___x_2161_; lean_object* v___x_2162_; lean_object* v___x_2163_; 
v___x_2161_ = lean_unsigned_to_nat(32u);
v___x_2162_ = lean_mk_empty_array_with_capacity(v___x_2161_);
v___x_2163_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2163_, 0, v___x_2162_);
return v___x_2163_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3(void){
_start:
{
size_t v___x_2164_; lean_object* v___x_2165_; lean_object* v___x_2166_; lean_object* v___x_2167_; lean_object* v___x_2168_; lean_object* v___x_2169_; 
v___x_2164_ = ((size_t)5ULL);
v___x_2165_ = lean_unsigned_to_nat(0u);
v___x_2166_ = lean_unsigned_to_nat(32u);
v___x_2167_ = lean_mk_empty_array_with_capacity(v___x_2166_);
v___x_2168_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__2, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__2_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__2);
v___x_2169_ = lean_alloc_ctor(0, 4, sizeof(size_t)*1);
lean_ctor_set(v___x_2169_, 0, v___x_2168_);
lean_ctor_set(v___x_2169_, 1, v___x_2167_);
lean_ctor_set(v___x_2169_, 2, v___x_2165_);
lean_ctor_set(v___x_2169_, 3, v___x_2165_);
lean_ctor_set_usize(v___x_2169_, 4, v___x_2164_);
return v___x_2169_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4(void){
_start:
{
lean_object* v___x_2170_; lean_object* v___x_2171_; lean_object* v___x_2172_; lean_object* v___x_2173_; 
v___x_2170_ = lean_box(1);
v___x_2171_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3);
v___x_2172_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1);
v___x_2173_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_2173_, 0, v___x_2172_);
lean_ctor_set(v___x_2173_, 1, v___x_2171_);
lean_ctor_set(v___x_2173_, 2, v___x_2170_);
return v___x_2173_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__6(void){
_start:
{
lean_object* v___x_2176_; lean_object* v___x_2177_; lean_object* v___x_2178_; 
v___x_2176_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1);
v___x_2177_ = lean_unsigned_to_nat(0u);
v___x_2178_ = lean_alloc_ctor(0, 10, 0);
lean_ctor_set(v___x_2178_, 0, v___x_2177_);
lean_ctor_set(v___x_2178_, 1, v___x_2177_);
lean_ctor_set(v___x_2178_, 2, v___x_2177_);
lean_ctor_set(v___x_2178_, 3, v___x_2177_);
lean_ctor_set(v___x_2178_, 4, v___x_2176_);
lean_ctor_set(v___x_2178_, 5, v___x_2176_);
lean_ctor_set(v___x_2178_, 6, v___x_2176_);
lean_ctor_set(v___x_2178_, 7, v___x_2176_);
lean_ctor_set(v___x_2178_, 8, v___x_2176_);
lean_ctor_set(v___x_2178_, 9, v___x_2176_);
return v___x_2178_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__7(void){
_start:
{
lean_object* v___x_2179_; lean_object* v___x_2180_; 
v___x_2179_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1);
v___x_2180_ = lean_alloc_ctor(0, 6, 0);
lean_ctor_set(v___x_2180_, 0, v___x_2179_);
lean_ctor_set(v___x_2180_, 1, v___x_2179_);
lean_ctor_set(v___x_2180_, 2, v___x_2179_);
lean_ctor_set(v___x_2180_, 3, v___x_2179_);
lean_ctor_set(v___x_2180_, 4, v___x_2179_);
lean_ctor_set(v___x_2180_, 5, v___x_2179_);
return v___x_2180_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__8(void){
_start:
{
lean_object* v___x_2181_; lean_object* v___x_2182_; 
v___x_2181_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1);
v___x_2182_ = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(v___x_2182_, 0, v___x_2181_);
lean_ctor_set(v___x_2182_, 1, v___x_2181_);
lean_ctor_set(v___x_2182_, 2, v___x_2181_);
lean_ctor_set(v___x_2182_, 3, v___x_2181_);
lean_ctor_set(v___x_2182_, 4, v___x_2181_);
return v___x_2182_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9(void){
_start:
{
lean_object* v___x_2183_; lean_object* v___x_2184_; 
v___x_2183_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1);
v___x_2184_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2184_, 0, v___x_2183_);
lean_ctor_set(v___x_2184_, 1, v___x_2183_);
return v___x_2184_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10(void){
_start:
{
lean_object* v___x_2185_; lean_object* v___x_2186_; lean_object* v___x_2187_; 
v___x_2185_ = lean_box(1);
v___x_2186_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3);
v___x_2187_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_2187_, 0, v___x_2186_);
lean_ctor_set(v___x_2187_, 1, v___x_2186_);
lean_ctor_set(v___x_2187_, 2, v___x_2185_);
return v___x_2187_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13(void){
_start:
{
lean_object* v___x_2195_; uint64_t v___x_2196_; lean_object* v___x_2197_; 
v___x_2195_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3);
v___x_2196_ = 0ULL;
v___x_2197_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_2197_, 0, v___x_2195_);
lean_ctor_set_uint64(v___x_2197_, sizeof(void*)*1, v___x_2196_);
return v___x_2197_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16(void){
_start:
{
lean_object* v___x_2200_; lean_object* v___x_2201_; lean_object* v___x_2202_; lean_object* v___x_2203_; lean_object* v___x_2204_; lean_object* v___x_2205_; 
v___x_2200_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__8, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__8_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__8);
v___x_2201_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3);
v___x_2202_ = lean_box(1);
v___x_2203_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__7, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__7_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__7);
v___x_2204_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__6, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__6_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__6);
v___x_2205_ = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(v___x_2205_, 0, v___x_2204_);
lean_ctor_set(v___x_2205_, 1, v___x_2203_);
lean_ctor_set(v___x_2205_, 2, v___x_2202_);
lean_ctor_set(v___x_2205_, 3, v___x_2201_);
lean_ctor_set(v___x_2205_, 4, v___x_2200_);
return v___x_2205_;
}
}
static uint8_t _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17(void){
_start:
{
lean_object* v___x_2206_; lean_object* v___x_2207_; uint8_t v___x_2208_; 
v___x_2206_ = l_Lean_diagnostics;
v___x_2207_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_2208_ = l_Lean_Option_get___at___00Lean_Elab_addMacroStack___at___00Lean_throwError___at___00Lean_throwErrorAt___at___00Lean_throwUnknownIdentifierAt___at___00Lean_throwUnknownConstantAt___at___00Lean_throwUnknownConstant___at___00Lean_getConstVal___at___00Lean_mkConstWithLevelParams___at___00Lean_Elab_addConstInfo___at___00Lean_Elab_PostprocessTraces_elabStoreTraceAs_spec__3_spec__5_spec__6_spec__9_spec__12_spec__14_spec__16_spec__18_spec__20_spec__21(v___x_2207_, v___x_2206_);
return v___x_2208_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18(void){
_start:
{
lean_object* v___x_2209_; lean_object* v___x_2210_; lean_object* v___x_2211_; 
v___x_2209_ = l_Lean_maxRecDepth;
v___x_2210_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_2211_ = l_Lean_Option_get___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0(v___x_2210_, v___x_2209_);
return v___x_2211_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21(lean_object* v_a_2212_, lean_object* v___x_2213_, lean_object* v_shard_2214_, lean_object* v_as_2215_, size_t v_sz_2216_, size_t v_i_2217_, lean_object* v_b_2218_){
_start:
{
lean_object* v_a_2221_; uint8_t v___x_2225_; 
v___x_2225_ = lean_usize_dec_lt(v_i_2217_, v_sz_2216_);
if (v___x_2225_ == 0)
{
lean_object* v___x_2226_; 
lean_dec_ref(v_a_2212_);
v___x_2226_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2226_, 0, v_b_2218_);
return v___x_2226_;
}
else
{
lean_object* v_fst_2227_; lean_object* v_snd_2228_; lean_object* v___x_2230_; uint8_t v_isShared_2231_; uint8_t v_isSharedCheck_2348_; 
v_fst_2227_ = lean_ctor_get(v_b_2218_, 0);
v_snd_2228_ = lean_ctor_get(v_b_2218_, 1);
v_isSharedCheck_2348_ = !lean_is_exclusive(v_b_2218_);
if (v_isSharedCheck_2348_ == 0)
{
v___x_2230_ = v_b_2218_;
v_isShared_2231_ = v_isSharedCheck_2348_;
goto v_resetjp_2229_;
}
else
{
lean_inc(v_snd_2228_);
lean_inc(v_fst_2227_);
lean_dec(v_b_2218_);
v___x_2230_ = lean_box(0);
v_isShared_2231_ = v_isSharedCheck_2348_;
goto v_resetjp_2229_;
}
v_resetjp_2229_:
{
lean_object* v___x_2232_; lean_object* v___x_2233_; uint8_t v___x_2234_; 
v___x_2232_ = lean_unsigned_to_nat(2000u);
v___x_2233_ = lean_string_length(v_fst_2227_);
v___x_2234_ = lean_nat_dec_lt(v___x_2232_, v___x_2233_);
if (v___x_2234_ == 0)
{
lean_object* v_a_2240_; lean_object* v___x_2241_; 
v_a_2240_ = lean_array_uget_borrowed(v_as_2215_, v_i_2217_);
lean_inc(v_a_2240_);
lean_inc_ref(v_a_2212_);
v___x_2241_ = l_Lean_Environment_find_x3f(v_a_2212_, v_a_2240_, v___x_2234_);
if (lean_obj_tag(v___x_2241_) == 1)
{
lean_object* v_val_2242_; uint8_t v___x_2243_; lean_object* v___x_2244_; uint8_t v___x_2245_; uint8_t v___x_2246_; uint8_t v___x_2247_; lean_object* v___x_2248_; uint64_t v___x_2249_; lean_object* v___x_2250_; lean_object* v___x_2251_; lean_object* v___x_2252_; lean_object* v___x_2253_; lean_object* v___x_2254_; lean_object* v___x_2255_; lean_object* v___x_2256_; lean_object* v___x_2257_; lean_object* v___x_2258_; lean_object* v___x_2259_; lean_object* v___x_2260_; lean_object* v___x_2261_; lean_object* v___x_2262_; lean_object* v___x_2263_; lean_object* v___x_2264_; lean_object* v___x_2265_; lean_object* v___x_2266_; lean_object* v___x_2267_; lean_object* v___x_2268_; lean_object* v___x_2269_; lean_object* v___x_2270_; lean_object* v___x_2271_; lean_object* v___x_2272_; lean_object* v___x_2273_; lean_object* v_env_2274_; lean_object* v___x_2275_; lean_object* v___x_2276_; lean_object* v___x_2277_; lean_object* v_a_2279_; lean_object* v___x_2290_; lean_object* v___x_2291_; lean_object* v___x_2292_; lean_object* v___x_2293_; lean_object* v___x_2294_; uint8_t v___x_2295_; lean_object* v_fileName_2297_; lean_object* v_fileMap_2298_; lean_object* v_currRecDepth_2299_; lean_object* v_ref_2300_; lean_object* v_currNamespace_2301_; lean_object* v_openDecls_2302_; lean_object* v_initHeartbeats_2303_; lean_object* v_maxHeartbeats_2304_; lean_object* v_quotContext_2305_; lean_object* v_currMacroScope_2306_; lean_object* v_cancelTk_x3f_2307_; uint8_t v_suppressElabErrors_2308_; lean_object* v_inheritedTraceOptions_2309_; lean_object* v___y_2310_; uint8_t v___y_2324_; uint8_t v___x_2344_; 
v_val_2242_ = lean_ctor_get(v___x_2241_, 0);
lean_inc(v_val_2242_);
lean_dec_ref_known(v___x_2241_, 1);
v___x_2243_ = lean_nat_dec_eq(v___x_2213_, v_shard_2214_);
v___x_2244_ = lean_unsigned_to_nat(0u);
v___x_2245_ = 1;
v___x_2246_ = 0;
v___x_2247_ = 2;
v___x_2248_ = lean_alloc_ctor(0, 0, 20);
lean_ctor_set_uint8(v___x_2248_, 0, v___x_2234_);
lean_ctor_set_uint8(v___x_2248_, 1, v___x_2234_);
lean_ctor_set_uint8(v___x_2248_, 2, v___x_2234_);
lean_ctor_set_uint8(v___x_2248_, 3, v___x_2234_);
lean_ctor_set_uint8(v___x_2248_, 4, v___x_2234_);
lean_ctor_set_uint8(v___x_2248_, 5, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 6, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 7, v___x_2234_);
lean_ctor_set_uint8(v___x_2248_, 8, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 9, v___x_2245_);
lean_ctor_set_uint8(v___x_2248_, 10, v___x_2246_);
lean_ctor_set_uint8(v___x_2248_, 11, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 12, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 13, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 14, v___x_2247_);
lean_ctor_set_uint8(v___x_2248_, 15, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 16, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 17, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 18, v___x_2243_);
lean_ctor_set_uint8(v___x_2248_, 19, v___x_2234_);
v___x_2249_ = l___private_Lean_Meta_Basic_0__Lean_Meta_Config_toKey(v___x_2248_);
v___x_2250_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_2250_, 0, v___x_2248_);
lean_ctor_set_uint64(v___x_2250_, sizeof(void*)*1, v___x_2249_);
v___x_2251_ = lean_box(1);
v___x_2252_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1);
v___x_2253_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3);
v___x_2254_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4);
v___x_2255_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__5));
v___x_2256_ = lean_box(0);
v___x_2257_ = lean_alloc_ctor(0, 7, 4);
lean_ctor_set(v___x_2257_, 0, v___x_2250_);
lean_ctor_set(v___x_2257_, 1, v___x_2251_);
lean_ctor_set(v___x_2257_, 2, v___x_2254_);
lean_ctor_set(v___x_2257_, 3, v___x_2255_);
lean_ctor_set(v___x_2257_, 4, v___x_2256_);
lean_ctor_set(v___x_2257_, 5, v___x_2244_);
lean_ctor_set(v___x_2257_, 6, v___x_2256_);
lean_ctor_set_uint8(v___x_2257_, sizeof(void*)*7, v___x_2234_);
lean_ctor_set_uint8(v___x_2257_, sizeof(void*)*7 + 1, v___x_2234_);
lean_ctor_set_uint8(v___x_2257_, sizeof(void*)*7 + 2, v___x_2234_);
lean_ctor_set_uint8(v___x_2257_, sizeof(void*)*7 + 3, v___x_2225_);
v___x_2258_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9);
v___x_2259_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10);
v___x_2260_ = lean_io_get_num_heartbeats();
v___x_2261_ = lean_unsigned_to_nat(1u);
v___x_2262_ = lean_box(0);
v___x_2263_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11));
v___x_2264_ = lean_unsigned_to_nat(2u);
v___x_2265_ = lean_box(0);
v___x_2266_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__12));
v___x_2267_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13);
v___x_2268_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_2268_, 0, v___x_2252_);
lean_ctor_set(v___x_2268_, 1, v___x_2252_);
lean_ctor_set(v___x_2268_, 2, v___x_2253_);
lean_ctor_set_uint8(v___x_2268_, sizeof(void*)*3, v___x_2225_);
lean_inc_ref(v_a_2212_);
v___x_2269_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_2269_, 0, v_a_2212_);
lean_ctor_set(v___x_2269_, 1, v___x_2264_);
lean_ctor_set(v___x_2269_, 2, v___x_2263_);
lean_ctor_set(v___x_2269_, 3, v___x_2266_);
lean_ctor_set(v___x_2269_, 4, v___x_2267_);
lean_ctor_set(v___x_2269_, 5, v___x_2258_);
lean_ctor_set(v___x_2269_, 6, v___x_2259_);
lean_ctor_set(v___x_2269_, 7, v___x_2268_);
lean_ctor_set(v___x_2269_, 8, v___x_2255_);
v___x_2270_ = lean_st_mk_ref(v___x_2269_);
v___x_2271_ = l_Lean_inheritedTraceOptions;
v___x_2272_ = lean_st_ref_get(v___x_2271_);
v___x_2273_ = lean_st_ref_get(v___x_2270_);
v_env_2274_ = lean_ctor_get(v___x_2273_, 0);
lean_inc_ref(v_env_2274_);
lean_dec(v___x_2273_);
v___x_2275_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_2276_ = l_Lean_instInhabitedFileMap_default;
v___x_2277_ = lean_unsigned_to_nat(100u);
v___x_2290_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_2291_ = lean_box(0);
v___x_2292_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_2293_ = l_Lean_ConstantInfo_type(v_val_2242_);
lean_dec(v_val_2242_);
v___x_2294_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16);
v___x_2295_ = lean_uint8_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17);
v___x_2344_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_2274_);
lean_dec_ref(v_env_2274_);
if (v___x_2344_ == 0)
{
if (v___x_2295_ == 0)
{
v___y_2324_ = v___x_2225_;
goto v___jp_2323_;
}
else
{
v___y_2324_ = v___x_2344_;
goto v___jp_2323_;
}
}
else
{
v___y_2324_ = v___x_2295_;
goto v___jp_2323_;
}
v___jp_2278_:
{
lean_object* v___x_2280_; lean_object* v___x_2281_; lean_object* v___x_2282_; lean_object* v___x_2283_; lean_object* v___x_2284_; lean_object* v___x_2285_; lean_object* v___x_2286_; lean_object* v___x_2287_; lean_object* v___x_2288_; lean_object* v___x_2289_; 
v___x_2280_ = l_Std_Format_pretty(v_a_2279_, v___x_2277_, v___x_2244_, v___x_2244_);
v___x_2281_ = lean_st_ref_get(v___x_2270_);
lean_dec(v___x_2270_);
lean_dec(v___x_2281_);
v___x_2282_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__14));
v___x_2283_ = lean_string_append(v_fst_2227_, v___x_2282_);
lean_inc(v_a_2240_);
v___x_2284_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_a_2240_, v___x_2234_);
v___x_2285_ = lean_string_append(v___x_2283_, v___x_2284_);
lean_dec_ref(v___x_2284_);
v___x_2286_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__15));
v___x_2287_ = lean_string_append(v___x_2285_, v___x_2286_);
v___x_2288_ = lean_string_append(v___x_2287_, v___x_2280_);
lean_dec_ref(v___x_2280_);
v___x_2289_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2289_, 0, v___x_2288_);
lean_ctor_set(v___x_2289_, 1, v_snd_2228_);
v_a_2221_ = v___x_2289_;
goto v___jp_2220_;
}
v___jp_2296_:
{
lean_object* v___x_2311_; lean_object* v___x_2312_; lean_object* v___x_2313_; lean_object* v___x_2314_; 
v___x_2311_ = lean_st_mk_ref(v___x_2294_);
v___x_2312_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18);
lean_inc(v_cancelTk_x3f_2307_);
lean_inc(v_quotContext_2305_);
lean_inc(v_maxHeartbeats_2304_);
lean_inc(v_openDecls_2302_);
lean_inc(v_currNamespace_2301_);
lean_inc(v_ref_2300_);
lean_inc_ref(v_fileMap_2298_);
lean_inc_ref(v_fileName_2297_);
v___x_2313_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_2313_, 0, v_fileName_2297_);
lean_ctor_set(v___x_2313_, 1, v_fileMap_2298_);
lean_ctor_set(v___x_2313_, 2, v___x_2290_);
lean_ctor_set(v___x_2313_, 3, v_currRecDepth_2299_);
lean_ctor_set(v___x_2313_, 4, v___x_2312_);
lean_ctor_set(v___x_2313_, 5, v_ref_2300_);
lean_ctor_set(v___x_2313_, 6, v_currNamespace_2301_);
lean_ctor_set(v___x_2313_, 7, v_openDecls_2302_);
lean_ctor_set(v___x_2313_, 8, v_initHeartbeats_2303_);
lean_ctor_set(v___x_2313_, 9, v_maxHeartbeats_2304_);
lean_ctor_set(v___x_2313_, 10, v_quotContext_2305_);
lean_ctor_set(v___x_2313_, 11, v_currMacroScope_2306_);
lean_ctor_set(v___x_2313_, 12, v_cancelTk_x3f_2307_);
lean_ctor_set(v___x_2313_, 13, v_inheritedTraceOptions_2309_);
lean_ctor_set_uint8(v___x_2313_, sizeof(void*)*14, v___x_2295_);
lean_ctor_set_uint8(v___x_2313_, sizeof(void*)*14 + 1, v_suppressElabErrors_2308_);
v___x_2314_ = l_Lean_Meta_ppExpr(v___x_2293_, v___x_2257_, v___x_2311_, v___x_2313_, v___y_2310_);
lean_dec(v___y_2310_);
lean_dec_ref_known(v___x_2313_, 14);
lean_dec_ref_known(v___x_2257_, 7);
if (lean_obj_tag(v___x_2314_) == 0)
{
lean_object* v_a_2315_; lean_object* v___x_2316_; 
lean_del_object(v___x_2230_);
v_a_2315_ = lean_ctor_get(v___x_2314_, 0);
lean_inc(v_a_2315_);
lean_dec_ref_known(v___x_2314_, 1);
v___x_2316_ = lean_st_ref_get(v___x_2311_);
lean_dec(v___x_2311_);
lean_dec(v___x_2316_);
v_a_2279_ = v_a_2315_;
goto v___jp_2278_;
}
else
{
lean_dec(v___x_2311_);
if (lean_obj_tag(v___x_2314_) == 0)
{
lean_object* v_a_2317_; 
lean_del_object(v___x_2230_);
v_a_2317_ = lean_ctor_get(v___x_2314_, 0);
lean_inc(v_a_2317_);
lean_dec_ref_known(v___x_2314_, 1);
v_a_2279_ = v_a_2317_;
goto v___jp_2278_;
}
else
{
lean_object* v_a_2318_; 
lean_dec(v___x_2270_);
lean_dec(v_snd_2228_);
v_a_2318_ = lean_ctor_get(v___x_2314_, 0);
lean_inc(v_a_2318_);
lean_dec_ref_known(v___x_2314_, 1);
if (lean_obj_tag(v_a_2318_) == 0)
{
lean_object* v_msg_2319_; lean_object* v___x_2320_; 
v_msg_2319_ = lean_ctor_get(v_a_2318_, 1);
lean_inc_ref(v_msg_2319_);
lean_dec_ref_known(v_a_2318_, 2);
v___x_2320_ = l_Lean_MessageData_toString(v_msg_2319_);
lean_dec_ref(v___x_2320_);
goto v___jp_2235_;
}
else
{
lean_object* v_id_2321_; lean_object* v___x_2322_; 
v_id_2321_ = lean_ctor_get(v_a_2318_, 0);
lean_inc(v_id_2321_);
lean_dec_ref_known(v_a_2318_, 2);
v___x_2322_ = l_Lean_InternalExceptionId_getName(v_id_2321_);
lean_dec(v_id_2321_);
lean_dec_ref(v___x_2322_);
goto v___jp_2235_;
}
}
}
}
v___jp_2323_:
{
if (v___y_2324_ == 0)
{
lean_object* v___x_2325_; lean_object* v_env_2326_; lean_object* v_nextMacroScope_2327_; lean_object* v_ngen_2328_; lean_object* v_auxDeclNGen_2329_; lean_object* v_traceState_2330_; lean_object* v_messages_2331_; lean_object* v_infoState_2332_; lean_object* v_snapshotTasks_2333_; lean_object* v___x_2335_; uint8_t v_isShared_2336_; uint8_t v_isSharedCheck_2342_; 
v___x_2325_ = lean_st_ref_take(v___x_2270_);
v_env_2326_ = lean_ctor_get(v___x_2325_, 0);
v_nextMacroScope_2327_ = lean_ctor_get(v___x_2325_, 1);
v_ngen_2328_ = lean_ctor_get(v___x_2325_, 2);
v_auxDeclNGen_2329_ = lean_ctor_get(v___x_2325_, 3);
v_traceState_2330_ = lean_ctor_get(v___x_2325_, 4);
v_messages_2331_ = lean_ctor_get(v___x_2325_, 6);
v_infoState_2332_ = lean_ctor_get(v___x_2325_, 7);
v_snapshotTasks_2333_ = lean_ctor_get(v___x_2325_, 8);
v_isSharedCheck_2342_ = !lean_is_exclusive(v___x_2325_);
if (v_isSharedCheck_2342_ == 0)
{
lean_object* v_unused_2343_; 
v_unused_2343_ = lean_ctor_get(v___x_2325_, 5);
lean_dec(v_unused_2343_);
v___x_2335_ = v___x_2325_;
v_isShared_2336_ = v_isSharedCheck_2342_;
goto v_resetjp_2334_;
}
else
{
lean_inc(v_snapshotTasks_2333_);
lean_inc(v_infoState_2332_);
lean_inc(v_messages_2331_);
lean_inc(v_traceState_2330_);
lean_inc(v_auxDeclNGen_2329_);
lean_inc(v_ngen_2328_);
lean_inc(v_nextMacroScope_2327_);
lean_inc(v_env_2326_);
lean_dec(v___x_2325_);
v___x_2335_ = lean_box(0);
v_isShared_2336_ = v_isSharedCheck_2342_;
goto v_resetjp_2334_;
}
v_resetjp_2334_:
{
lean_object* v___x_2337_; lean_object* v___x_2339_; 
v___x_2337_ = l_Lean_Kernel_enableDiag(v_env_2326_, v___x_2295_);
if (v_isShared_2336_ == 0)
{
lean_ctor_set(v___x_2335_, 5, v___x_2258_);
lean_ctor_set(v___x_2335_, 0, v___x_2337_);
v___x_2339_ = v___x_2335_;
goto v_reusejp_2338_;
}
else
{
lean_object* v_reuseFailAlloc_2341_; 
v_reuseFailAlloc_2341_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_2341_, 0, v___x_2337_);
lean_ctor_set(v_reuseFailAlloc_2341_, 1, v_nextMacroScope_2327_);
lean_ctor_set(v_reuseFailAlloc_2341_, 2, v_ngen_2328_);
lean_ctor_set(v_reuseFailAlloc_2341_, 3, v_auxDeclNGen_2329_);
lean_ctor_set(v_reuseFailAlloc_2341_, 4, v_traceState_2330_);
lean_ctor_set(v_reuseFailAlloc_2341_, 5, v___x_2258_);
lean_ctor_set(v_reuseFailAlloc_2341_, 6, v_messages_2331_);
lean_ctor_set(v_reuseFailAlloc_2341_, 7, v_infoState_2332_);
lean_ctor_set(v_reuseFailAlloc_2341_, 8, v_snapshotTasks_2333_);
v___x_2339_ = v_reuseFailAlloc_2341_;
goto v_reusejp_2338_;
}
v_reusejp_2338_:
{
lean_object* v___x_2340_; 
v___x_2340_ = lean_st_ref_set(v___x_2270_, v___x_2339_);
lean_inc(v___x_2270_);
v_fileName_2297_ = v___x_2275_;
v_fileMap_2298_ = v___x_2276_;
v_currRecDepth_2299_ = v___x_2244_;
v_ref_2300_ = v___x_2291_;
v_currNamespace_2301_ = v___x_2262_;
v_openDecls_2302_ = v___x_2265_;
v_initHeartbeats_2303_ = v___x_2260_;
v_maxHeartbeats_2304_ = v___x_2292_;
v_quotContext_2305_ = v___x_2262_;
v_currMacroScope_2306_ = v___x_2261_;
v_cancelTk_x3f_2307_ = v___x_2256_;
v_suppressElabErrors_2308_ = v___x_2234_;
v_inheritedTraceOptions_2309_ = v___x_2272_;
v___y_2310_ = v___x_2270_;
goto v___jp_2296_;
}
}
}
else
{
lean_inc(v___x_2270_);
v_fileName_2297_ = v___x_2275_;
v_fileMap_2298_ = v___x_2276_;
v_currRecDepth_2299_ = v___x_2244_;
v_ref_2300_ = v___x_2291_;
v_currNamespace_2301_ = v___x_2262_;
v_openDecls_2302_ = v___x_2265_;
v_initHeartbeats_2303_ = v___x_2260_;
v_maxHeartbeats_2304_ = v___x_2292_;
v_quotContext_2305_ = v___x_2262_;
v_currMacroScope_2306_ = v___x_2261_;
v_cancelTk_x3f_2307_ = v___x_2256_;
v_suppressElabErrors_2308_ = v___x_2234_;
v_inheritedTraceOptions_2309_ = v___x_2272_;
v___y_2310_ = v___x_2270_;
goto v___jp_2296_;
}
}
}
else
{
lean_object* v___x_2345_; 
lean_dec(v___x_2241_);
lean_del_object(v___x_2230_);
v___x_2345_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2345_, 0, v_fst_2227_);
lean_ctor_set(v___x_2345_, 1, v_snd_2228_);
v_a_2221_ = v___x_2345_;
goto v___jp_2220_;
}
}
else
{
lean_object* v___x_2346_; lean_object* v___x_2347_; 
lean_del_object(v___x_2230_);
lean_dec_ref(v_a_2212_);
v___x_2346_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2346_, 0, v_fst_2227_);
lean_ctor_set(v___x_2346_, 1, v_snd_2228_);
v___x_2347_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2347_, 0, v___x_2346_);
return v___x_2347_;
}
v___jp_2235_:
{
lean_object* v___x_2236_; lean_object* v___x_2238_; 
v___x_2236_ = lean_box(v___x_2234_);
if (v_isShared_2231_ == 0)
{
lean_ctor_set(v___x_2230_, 1, v___x_2236_);
v___x_2238_ = v___x_2230_;
goto v_reusejp_2237_;
}
else
{
lean_object* v_reuseFailAlloc_2239_; 
v_reuseFailAlloc_2239_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2239_, 0, v_fst_2227_);
lean_ctor_set(v_reuseFailAlloc_2239_, 1, v___x_2236_);
v___x_2238_ = v_reuseFailAlloc_2239_;
goto v_reusejp_2237_;
}
v_reusejp_2237_:
{
v_a_2221_ = v___x_2238_;
goto v___jp_2220_;
}
}
}
}
v___jp_2220_:
{
size_t v___x_2222_; size_t v___x_2223_; 
v___x_2222_ = ((size_t)1ULL);
v___x_2223_ = lean_usize_add(v_i_2217_, v___x_2222_);
v_i_2217_ = v___x_2223_;
v_b_2218_ = v_a_2221_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___boxed(lean_object* v_a_2349_, lean_object* v___x_2350_, lean_object* v_shard_2351_, lean_object* v_as_2352_, lean_object* v_sz_2353_, lean_object* v_i_2354_, lean_object* v_b_2355_, lean_object* v___y_2356_){
_start:
{
size_t v_sz_boxed_2357_; size_t v_i_boxed_2358_; lean_object* v_res_2359_; 
v_sz_boxed_2357_ = lean_unbox_usize(v_sz_2353_);
lean_dec(v_sz_2353_);
v_i_boxed_2358_ = lean_unbox_usize(v_i_2354_);
lean_dec(v_i_2354_);
v_res_2359_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21(v_a_2349_, v___x_2350_, v_shard_2351_, v_as_2352_, v_sz_boxed_2357_, v_i_boxed_2358_, v_b_2355_);
lean_dec_ref(v_as_2352_);
lean_dec(v_shard_2351_);
lean_dec(v___x_2350_);
return v_res_2359_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16(lean_object* v_a_2360_, lean_object* v___x_2361_, lean_object* v_shard_2362_, lean_object* v_as_2363_, size_t v_sz_2364_, size_t v_i_2365_, lean_object* v_b_2366_){
_start:
{
lean_object* v_a_2369_; uint8_t v___x_2373_; 
v___x_2373_ = lean_usize_dec_lt(v_i_2365_, v_sz_2364_);
if (v___x_2373_ == 0)
{
lean_object* v___x_2374_; 
lean_dec_ref(v_a_2360_);
v___x_2374_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2374_, 0, v_b_2366_);
return v___x_2374_;
}
else
{
lean_object* v_fst_2375_; lean_object* v_snd_2376_; lean_object* v___x_2378_; uint8_t v_isShared_2379_; uint8_t v_isSharedCheck_2498_; 
v_fst_2375_ = lean_ctor_get(v_b_2366_, 0);
v_snd_2376_ = lean_ctor_get(v_b_2366_, 1);
v_isSharedCheck_2498_ = !lean_is_exclusive(v_b_2366_);
if (v_isSharedCheck_2498_ == 0)
{
v___x_2378_ = v_b_2366_;
v_isShared_2379_ = v_isSharedCheck_2498_;
goto v_resetjp_2377_;
}
else
{
lean_inc(v_snd_2376_);
lean_inc(v_fst_2375_);
lean_dec(v_b_2366_);
v___x_2378_ = lean_box(0);
v_isShared_2379_ = v_isSharedCheck_2498_;
goto v_resetjp_2377_;
}
v_resetjp_2377_:
{
lean_object* v___x_2380_; lean_object* v___x_2381_; uint8_t v___x_2382_; 
v___x_2380_ = lean_unsigned_to_nat(2000u);
v___x_2381_ = lean_string_length(v_fst_2375_);
v___x_2382_ = lean_nat_dec_lt(v___x_2380_, v___x_2381_);
if (v___x_2382_ == 0)
{
lean_object* v_a_2388_; lean_object* v___x_2389_; 
v_a_2388_ = lean_array_uget_borrowed(v_as_2363_, v_i_2365_);
lean_inc(v_a_2388_);
lean_inc_ref(v_a_2360_);
v___x_2389_ = l_Lean_Environment_find_x3f(v_a_2360_, v_a_2388_, v___x_2382_);
if (lean_obj_tag(v___x_2389_) == 1)
{
lean_object* v_val_2390_; uint8_t v___x_2391_; lean_object* v___x_2392_; uint8_t v___x_2393_; uint8_t v___x_2394_; uint8_t v___x_2395_; lean_object* v___x_2396_; uint64_t v___x_2397_; lean_object* v___x_2398_; lean_object* v___x_2399_; lean_object* v___x_2400_; lean_object* v___x_2401_; lean_object* v___x_2402_; lean_object* v___x_2403_; lean_object* v___x_2404_; lean_object* v___x_2405_; lean_object* v___x_2406_; lean_object* v___x_2407_; lean_object* v___x_2408_; lean_object* v___x_2409_; lean_object* v___x_2410_; lean_object* v___x_2411_; lean_object* v___x_2412_; lean_object* v___x_2413_; lean_object* v___x_2414_; lean_object* v___x_2415_; lean_object* v___x_2416_; lean_object* v___x_2417_; lean_object* v___x_2418_; lean_object* v___x_2419_; lean_object* v___x_2420_; lean_object* v___x_2421_; lean_object* v___x_2422_; lean_object* v___x_2423_; lean_object* v_env_2424_; lean_object* v___x_2425_; lean_object* v_a_2427_; lean_object* v___x_2438_; lean_object* v___x_2439_; lean_object* v___x_2440_; lean_object* v___x_2441_; lean_object* v___x_2442_; lean_object* v___x_2443_; lean_object* v___x_2444_; uint8_t v___x_2445_; lean_object* v_fileName_2447_; lean_object* v_fileMap_2448_; lean_object* v_currRecDepth_2449_; lean_object* v_ref_2450_; lean_object* v_currNamespace_2451_; lean_object* v_openDecls_2452_; lean_object* v_initHeartbeats_2453_; lean_object* v_maxHeartbeats_2454_; lean_object* v_quotContext_2455_; lean_object* v_currMacroScope_2456_; lean_object* v_cancelTk_x3f_2457_; uint8_t v_suppressElabErrors_2458_; lean_object* v_inheritedTraceOptions_2459_; lean_object* v___y_2460_; uint8_t v___y_2474_; uint8_t v___x_2494_; 
v_val_2390_ = lean_ctor_get(v___x_2389_, 0);
lean_inc(v_val_2390_);
lean_dec_ref_known(v___x_2389_, 1);
v___x_2391_ = lean_nat_dec_eq(v___x_2361_, v_shard_2362_);
v___x_2392_ = lean_unsigned_to_nat(0u);
v___x_2393_ = 1;
v___x_2394_ = 0;
v___x_2395_ = 2;
v___x_2396_ = lean_alloc_ctor(0, 0, 20);
lean_ctor_set_uint8(v___x_2396_, 0, v___x_2382_);
lean_ctor_set_uint8(v___x_2396_, 1, v___x_2382_);
lean_ctor_set_uint8(v___x_2396_, 2, v___x_2382_);
lean_ctor_set_uint8(v___x_2396_, 3, v___x_2382_);
lean_ctor_set_uint8(v___x_2396_, 4, v___x_2382_);
lean_ctor_set_uint8(v___x_2396_, 5, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 6, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 7, v___x_2382_);
lean_ctor_set_uint8(v___x_2396_, 8, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 9, v___x_2393_);
lean_ctor_set_uint8(v___x_2396_, 10, v___x_2394_);
lean_ctor_set_uint8(v___x_2396_, 11, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 12, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 13, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 14, v___x_2395_);
lean_ctor_set_uint8(v___x_2396_, 15, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 16, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 17, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 18, v___x_2391_);
lean_ctor_set_uint8(v___x_2396_, 19, v___x_2382_);
v___x_2397_ = l___private_Lean_Meta_Basic_0__Lean_Meta_Config_toKey(v___x_2396_);
v___x_2398_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_2398_, 0, v___x_2396_);
lean_ctor_set_uint64(v___x_2398_, sizeof(void*)*1, v___x_2397_);
v___x_2399_ = lean_box(1);
v___x_2400_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__1);
v___x_2401_ = lean_unsigned_to_nat(32u);
v___x_2402_ = lean_mk_empty_array_with_capacity(v___x_2401_);
lean_dec_ref(v___x_2402_);
v___x_2403_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__3);
v___x_2404_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4);
v___x_2405_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__5));
v___x_2406_ = lean_box(0);
v___x_2407_ = lean_alloc_ctor(0, 7, 4);
lean_ctor_set(v___x_2407_, 0, v___x_2398_);
lean_ctor_set(v___x_2407_, 1, v___x_2399_);
lean_ctor_set(v___x_2407_, 2, v___x_2404_);
lean_ctor_set(v___x_2407_, 3, v___x_2405_);
lean_ctor_set(v___x_2407_, 4, v___x_2406_);
lean_ctor_set(v___x_2407_, 5, v___x_2392_);
lean_ctor_set(v___x_2407_, 6, v___x_2406_);
lean_ctor_set_uint8(v___x_2407_, sizeof(void*)*7, v___x_2382_);
lean_ctor_set_uint8(v___x_2407_, sizeof(void*)*7 + 1, v___x_2382_);
lean_ctor_set_uint8(v___x_2407_, sizeof(void*)*7 + 2, v___x_2382_);
lean_ctor_set_uint8(v___x_2407_, sizeof(void*)*7 + 3, v___x_2373_);
v___x_2408_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__9);
v___x_2409_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__10);
v___x_2410_ = lean_io_get_num_heartbeats();
v___x_2411_ = lean_unsigned_to_nat(1u);
v___x_2412_ = lean_box(0);
v___x_2413_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11));
v___x_2414_ = lean_unsigned_to_nat(2u);
v___x_2415_ = lean_box(0);
v___x_2416_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__12));
v___x_2417_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__13);
v___x_2418_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_2418_, 0, v___x_2400_);
lean_ctor_set(v___x_2418_, 1, v___x_2400_);
lean_ctor_set(v___x_2418_, 2, v___x_2403_);
lean_ctor_set_uint8(v___x_2418_, sizeof(void*)*3, v___x_2373_);
lean_inc_ref(v_a_2360_);
v___x_2419_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_2419_, 0, v_a_2360_);
lean_ctor_set(v___x_2419_, 1, v___x_2414_);
lean_ctor_set(v___x_2419_, 2, v___x_2413_);
lean_ctor_set(v___x_2419_, 3, v___x_2416_);
lean_ctor_set(v___x_2419_, 4, v___x_2417_);
lean_ctor_set(v___x_2419_, 5, v___x_2408_);
lean_ctor_set(v___x_2419_, 6, v___x_2409_);
lean_ctor_set(v___x_2419_, 7, v___x_2418_);
lean_ctor_set(v___x_2419_, 8, v___x_2405_);
v___x_2420_ = lean_st_mk_ref(v___x_2419_);
v___x_2421_ = l_Lean_inheritedTraceOptions;
v___x_2422_ = lean_st_ref_get(v___x_2421_);
v___x_2423_ = lean_st_ref_get(v___x_2420_);
v_env_2424_ = lean_ctor_get(v___x_2423_, 0);
lean_inc_ref(v_env_2424_);
lean_dec(v___x_2423_);
v___x_2425_ = lean_unsigned_to_nat(100u);
v___x_2438_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_2439_ = l_Lean_instInhabitedFileMap_default;
v___x_2440_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_2441_ = lean_box(0);
v___x_2442_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_2443_ = l_Lean_ConstantInfo_type(v_val_2390_);
lean_dec(v_val_2390_);
v___x_2444_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16);
v___x_2445_ = lean_uint8_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17);
v___x_2494_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_2424_);
lean_dec_ref(v_env_2424_);
if (v___x_2494_ == 0)
{
if (v___x_2445_ == 0)
{
v___y_2474_ = v___x_2373_;
goto v___jp_2473_;
}
else
{
v___y_2474_ = v___x_2494_;
goto v___jp_2473_;
}
}
else
{
v___y_2474_ = v___x_2445_;
goto v___jp_2473_;
}
v___jp_2426_:
{
lean_object* v___x_2428_; lean_object* v___x_2429_; lean_object* v___x_2430_; lean_object* v___x_2431_; lean_object* v___x_2432_; lean_object* v___x_2433_; lean_object* v___x_2434_; lean_object* v___x_2435_; lean_object* v___x_2436_; lean_object* v___x_2437_; 
v___x_2428_ = l_Std_Format_pretty(v_a_2427_, v___x_2425_, v___x_2392_, v___x_2392_);
v___x_2429_ = lean_st_ref_get(v___x_2420_);
lean_dec(v___x_2420_);
lean_dec(v___x_2429_);
v___x_2430_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__14));
v___x_2431_ = lean_string_append(v_fst_2375_, v___x_2430_);
lean_inc(v_a_2388_);
v___x_2432_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_a_2388_, v___x_2382_);
v___x_2433_ = lean_string_append(v___x_2431_, v___x_2432_);
lean_dec_ref(v___x_2432_);
v___x_2434_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__15));
v___x_2435_ = lean_string_append(v___x_2433_, v___x_2434_);
v___x_2436_ = lean_string_append(v___x_2435_, v___x_2428_);
lean_dec_ref(v___x_2428_);
v___x_2437_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2437_, 0, v___x_2436_);
lean_ctor_set(v___x_2437_, 1, v_snd_2376_);
v_a_2369_ = v___x_2437_;
goto v___jp_2368_;
}
v___jp_2446_:
{
lean_object* v___x_2461_; lean_object* v___x_2462_; lean_object* v___x_2463_; lean_object* v___x_2464_; 
v___x_2461_ = lean_st_mk_ref(v___x_2444_);
v___x_2462_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18);
lean_inc(v_cancelTk_x3f_2457_);
lean_inc(v_quotContext_2455_);
lean_inc(v_maxHeartbeats_2454_);
lean_inc(v_openDecls_2452_);
lean_inc(v_currNamespace_2451_);
lean_inc(v_ref_2450_);
lean_inc_ref(v_fileMap_2448_);
lean_inc_ref(v_fileName_2447_);
v___x_2463_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_2463_, 0, v_fileName_2447_);
lean_ctor_set(v___x_2463_, 1, v_fileMap_2448_);
lean_ctor_set(v___x_2463_, 2, v___x_2440_);
lean_ctor_set(v___x_2463_, 3, v_currRecDepth_2449_);
lean_ctor_set(v___x_2463_, 4, v___x_2462_);
lean_ctor_set(v___x_2463_, 5, v_ref_2450_);
lean_ctor_set(v___x_2463_, 6, v_currNamespace_2451_);
lean_ctor_set(v___x_2463_, 7, v_openDecls_2452_);
lean_ctor_set(v___x_2463_, 8, v_initHeartbeats_2453_);
lean_ctor_set(v___x_2463_, 9, v_maxHeartbeats_2454_);
lean_ctor_set(v___x_2463_, 10, v_quotContext_2455_);
lean_ctor_set(v___x_2463_, 11, v_currMacroScope_2456_);
lean_ctor_set(v___x_2463_, 12, v_cancelTk_x3f_2457_);
lean_ctor_set(v___x_2463_, 13, v_inheritedTraceOptions_2459_);
lean_ctor_set_uint8(v___x_2463_, sizeof(void*)*14, v___x_2445_);
lean_ctor_set_uint8(v___x_2463_, sizeof(void*)*14 + 1, v_suppressElabErrors_2458_);
v___x_2464_ = l_Lean_Meta_ppExpr(v___x_2443_, v___x_2407_, v___x_2461_, v___x_2463_, v___y_2460_);
lean_dec(v___y_2460_);
lean_dec_ref_known(v___x_2463_, 14);
lean_dec_ref_known(v___x_2407_, 7);
if (lean_obj_tag(v___x_2464_) == 0)
{
lean_object* v_a_2465_; lean_object* v___x_2466_; 
lean_del_object(v___x_2378_);
v_a_2465_ = lean_ctor_get(v___x_2464_, 0);
lean_inc(v_a_2465_);
lean_dec_ref_known(v___x_2464_, 1);
v___x_2466_ = lean_st_ref_get(v___x_2461_);
lean_dec(v___x_2461_);
lean_dec(v___x_2466_);
v_a_2427_ = v_a_2465_;
goto v___jp_2426_;
}
else
{
lean_dec(v___x_2461_);
if (lean_obj_tag(v___x_2464_) == 0)
{
lean_object* v_a_2467_; 
lean_del_object(v___x_2378_);
v_a_2467_ = lean_ctor_get(v___x_2464_, 0);
lean_inc(v_a_2467_);
lean_dec_ref_known(v___x_2464_, 1);
v_a_2427_ = v_a_2467_;
goto v___jp_2426_;
}
else
{
lean_object* v_a_2468_; 
lean_dec(v___x_2420_);
lean_dec(v_snd_2376_);
v_a_2468_ = lean_ctor_get(v___x_2464_, 0);
lean_inc(v_a_2468_);
lean_dec_ref_known(v___x_2464_, 1);
if (lean_obj_tag(v_a_2468_) == 0)
{
lean_object* v_msg_2469_; lean_object* v___x_2470_; 
v_msg_2469_ = lean_ctor_get(v_a_2468_, 1);
lean_inc_ref(v_msg_2469_);
lean_dec_ref_known(v_a_2468_, 2);
v___x_2470_ = l_Lean_MessageData_toString(v_msg_2469_);
lean_dec_ref(v___x_2470_);
goto v___jp_2383_;
}
else
{
lean_object* v_id_2471_; lean_object* v___x_2472_; 
v_id_2471_ = lean_ctor_get(v_a_2468_, 0);
lean_inc(v_id_2471_);
lean_dec_ref_known(v_a_2468_, 2);
v___x_2472_ = l_Lean_InternalExceptionId_getName(v_id_2471_);
lean_dec(v_id_2471_);
lean_dec_ref(v___x_2472_);
goto v___jp_2383_;
}
}
}
}
v___jp_2473_:
{
if (v___y_2474_ == 0)
{
lean_object* v___x_2475_; lean_object* v_env_2476_; lean_object* v_nextMacroScope_2477_; lean_object* v_ngen_2478_; lean_object* v_auxDeclNGen_2479_; lean_object* v_traceState_2480_; lean_object* v_messages_2481_; lean_object* v_infoState_2482_; lean_object* v_snapshotTasks_2483_; lean_object* v___x_2485_; uint8_t v_isShared_2486_; uint8_t v_isSharedCheck_2492_; 
v___x_2475_ = lean_st_ref_take(v___x_2420_);
v_env_2476_ = lean_ctor_get(v___x_2475_, 0);
v_nextMacroScope_2477_ = lean_ctor_get(v___x_2475_, 1);
v_ngen_2478_ = lean_ctor_get(v___x_2475_, 2);
v_auxDeclNGen_2479_ = lean_ctor_get(v___x_2475_, 3);
v_traceState_2480_ = lean_ctor_get(v___x_2475_, 4);
v_messages_2481_ = lean_ctor_get(v___x_2475_, 6);
v_infoState_2482_ = lean_ctor_get(v___x_2475_, 7);
v_snapshotTasks_2483_ = lean_ctor_get(v___x_2475_, 8);
v_isSharedCheck_2492_ = !lean_is_exclusive(v___x_2475_);
if (v_isSharedCheck_2492_ == 0)
{
lean_object* v_unused_2493_; 
v_unused_2493_ = lean_ctor_get(v___x_2475_, 5);
lean_dec(v_unused_2493_);
v___x_2485_ = v___x_2475_;
v_isShared_2486_ = v_isSharedCheck_2492_;
goto v_resetjp_2484_;
}
else
{
lean_inc(v_snapshotTasks_2483_);
lean_inc(v_infoState_2482_);
lean_inc(v_messages_2481_);
lean_inc(v_traceState_2480_);
lean_inc(v_auxDeclNGen_2479_);
lean_inc(v_ngen_2478_);
lean_inc(v_nextMacroScope_2477_);
lean_inc(v_env_2476_);
lean_dec(v___x_2475_);
v___x_2485_ = lean_box(0);
v_isShared_2486_ = v_isSharedCheck_2492_;
goto v_resetjp_2484_;
}
v_resetjp_2484_:
{
lean_object* v___x_2487_; lean_object* v___x_2489_; 
v___x_2487_ = l_Lean_Kernel_enableDiag(v_env_2476_, v___x_2445_);
if (v_isShared_2486_ == 0)
{
lean_ctor_set(v___x_2485_, 5, v___x_2408_);
lean_ctor_set(v___x_2485_, 0, v___x_2487_);
v___x_2489_ = v___x_2485_;
goto v_reusejp_2488_;
}
else
{
lean_object* v_reuseFailAlloc_2491_; 
v_reuseFailAlloc_2491_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_2491_, 0, v___x_2487_);
lean_ctor_set(v_reuseFailAlloc_2491_, 1, v_nextMacroScope_2477_);
lean_ctor_set(v_reuseFailAlloc_2491_, 2, v_ngen_2478_);
lean_ctor_set(v_reuseFailAlloc_2491_, 3, v_auxDeclNGen_2479_);
lean_ctor_set(v_reuseFailAlloc_2491_, 4, v_traceState_2480_);
lean_ctor_set(v_reuseFailAlloc_2491_, 5, v___x_2408_);
lean_ctor_set(v_reuseFailAlloc_2491_, 6, v_messages_2481_);
lean_ctor_set(v_reuseFailAlloc_2491_, 7, v_infoState_2482_);
lean_ctor_set(v_reuseFailAlloc_2491_, 8, v_snapshotTasks_2483_);
v___x_2489_ = v_reuseFailAlloc_2491_;
goto v_reusejp_2488_;
}
v_reusejp_2488_:
{
lean_object* v___x_2490_; 
v___x_2490_ = lean_st_ref_set(v___x_2420_, v___x_2489_);
lean_inc(v___x_2420_);
v_fileName_2447_ = v___x_2438_;
v_fileMap_2448_ = v___x_2439_;
v_currRecDepth_2449_ = v___x_2392_;
v_ref_2450_ = v___x_2441_;
v_currNamespace_2451_ = v___x_2412_;
v_openDecls_2452_ = v___x_2415_;
v_initHeartbeats_2453_ = v___x_2410_;
v_maxHeartbeats_2454_ = v___x_2442_;
v_quotContext_2455_ = v___x_2412_;
v_currMacroScope_2456_ = v___x_2411_;
v_cancelTk_x3f_2457_ = v___x_2406_;
v_suppressElabErrors_2458_ = v___x_2382_;
v_inheritedTraceOptions_2459_ = v___x_2422_;
v___y_2460_ = v___x_2420_;
goto v___jp_2446_;
}
}
}
else
{
lean_inc(v___x_2420_);
v_fileName_2447_ = v___x_2438_;
v_fileMap_2448_ = v___x_2439_;
v_currRecDepth_2449_ = v___x_2392_;
v_ref_2450_ = v___x_2441_;
v_currNamespace_2451_ = v___x_2412_;
v_openDecls_2452_ = v___x_2415_;
v_initHeartbeats_2453_ = v___x_2410_;
v_maxHeartbeats_2454_ = v___x_2442_;
v_quotContext_2455_ = v___x_2412_;
v_currMacroScope_2456_ = v___x_2411_;
v_cancelTk_x3f_2457_ = v___x_2406_;
v_suppressElabErrors_2458_ = v___x_2382_;
v_inheritedTraceOptions_2459_ = v___x_2422_;
v___y_2460_ = v___x_2420_;
goto v___jp_2446_;
}
}
}
else
{
lean_object* v___x_2495_; 
lean_dec(v___x_2389_);
lean_del_object(v___x_2378_);
v___x_2495_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2495_, 0, v_fst_2375_);
lean_ctor_set(v___x_2495_, 1, v_snd_2376_);
v_a_2369_ = v___x_2495_;
goto v___jp_2368_;
}
}
else
{
lean_object* v___x_2496_; lean_object* v___x_2497_; 
lean_del_object(v___x_2378_);
lean_dec_ref(v_a_2360_);
v___x_2496_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2496_, 0, v_fst_2375_);
lean_ctor_set(v___x_2496_, 1, v_snd_2376_);
v___x_2497_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2497_, 0, v___x_2496_);
return v___x_2497_;
}
v___jp_2383_:
{
lean_object* v___x_2384_; lean_object* v___x_2386_; 
v___x_2384_ = lean_box(v___x_2382_);
if (v_isShared_2379_ == 0)
{
lean_ctor_set(v___x_2378_, 1, v___x_2384_);
v___x_2386_ = v___x_2378_;
goto v_reusejp_2385_;
}
else
{
lean_object* v_reuseFailAlloc_2387_; 
v_reuseFailAlloc_2387_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2387_, 0, v_fst_2375_);
lean_ctor_set(v_reuseFailAlloc_2387_, 1, v___x_2384_);
v___x_2386_ = v_reuseFailAlloc_2387_;
goto v_reusejp_2385_;
}
v_reusejp_2385_:
{
v_a_2369_ = v___x_2386_;
goto v___jp_2368_;
}
}
}
}
v___jp_2368_:
{
size_t v___x_2370_; size_t v___x_2371_; lean_object* v___x_2372_; 
v___x_2370_ = ((size_t)1ULL);
v___x_2371_ = lean_usize_add(v_i_2365_, v___x_2370_);
v___x_2372_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21(v_a_2360_, v___x_2361_, v_shard_2362_, v_as_2363_, v_sz_2364_, v___x_2371_, v_a_2369_);
return v___x_2372_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16___boxed(lean_object* v_a_2499_, lean_object* v___x_2500_, lean_object* v_shard_2501_, lean_object* v_as_2502_, lean_object* v_sz_2503_, lean_object* v_i_2504_, lean_object* v_b_2505_, lean_object* v___y_2506_){
_start:
{
size_t v_sz_boxed_2507_; size_t v_i_boxed_2508_; lean_object* v_res_2509_; 
v_sz_boxed_2507_ = lean_unbox_usize(v_sz_2503_);
lean_dec(v_sz_2503_);
v_i_boxed_2508_ = lean_unbox_usize(v_i_2504_);
lean_dec(v_i_2504_);
v_res_2509_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16(v_a_2499_, v___x_2500_, v_shard_2501_, v_as_2502_, v_sz_boxed_2507_, v_i_boxed_2508_, v_b_2505_);
lean_dec_ref(v_as_2502_);
lean_dec(v_shard_2501_);
lean_dec(v___x_2500_);
return v_res_2509_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__4(lean_object* v___x_2510_, lean_object* v___x_2511_, lean_object* v___x_2512_, lean_object* v___x_2513_, lean_object* v___x_2514_, lean_object* v___y_2515_, lean_object* v___y_2516_){
_start:
{
lean_object* v_a_2519_; lean_object* v___x_2522_; lean_object* v___x_2523_; 
v___x_2522_ = lean_st_mk_ref(v___x_2510_);
v___x_2523_ = l_Lean_Meta_ppExpr(v___x_2513_, v___x_2514_, v___x_2522_, v___y_2515_, v___y_2516_);
if (lean_obj_tag(v___x_2523_) == 0)
{
lean_object* v_a_2524_; lean_object* v___x_2525_; 
v_a_2524_ = lean_ctor_get(v___x_2523_, 0);
lean_inc(v_a_2524_);
lean_dec_ref_known(v___x_2523_, 1);
v___x_2525_ = lean_st_ref_get(v___x_2522_);
lean_dec(v___x_2522_);
lean_dec(v___x_2525_);
v_a_2519_ = v_a_2524_;
goto v___jp_2518_;
}
else
{
lean_dec(v___x_2522_);
if (lean_obj_tag(v___x_2523_) == 0)
{
lean_object* v_a_2526_; 
v_a_2526_ = lean_ctor_get(v___x_2523_, 0);
lean_inc(v_a_2526_);
lean_dec_ref_known(v___x_2523_, 1);
v_a_2519_ = v_a_2526_;
goto v___jp_2518_;
}
else
{
lean_object* v_a_2527_; lean_object* v___x_2529_; uint8_t v_isShared_2530_; uint8_t v_isSharedCheck_2534_; 
lean_dec(v___x_2512_);
v_a_2527_ = lean_ctor_get(v___x_2523_, 0);
v_isSharedCheck_2534_ = !lean_is_exclusive(v___x_2523_);
if (v_isSharedCheck_2534_ == 0)
{
v___x_2529_ = v___x_2523_;
v_isShared_2530_ = v_isSharedCheck_2534_;
goto v_resetjp_2528_;
}
else
{
lean_inc(v_a_2527_);
lean_dec(v___x_2523_);
v___x_2529_ = lean_box(0);
v_isShared_2530_ = v_isSharedCheck_2534_;
goto v_resetjp_2528_;
}
v_resetjp_2528_:
{
lean_object* v___x_2532_; 
if (v_isShared_2530_ == 0)
{
v___x_2532_ = v___x_2529_;
goto v_reusejp_2531_;
}
else
{
lean_object* v_reuseFailAlloc_2533_; 
v_reuseFailAlloc_2533_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2533_, 0, v_a_2527_);
v___x_2532_ = v_reuseFailAlloc_2533_;
goto v_reusejp_2531_;
}
v_reusejp_2531_:
{
return v___x_2532_;
}
}
}
}
v___jp_2518_:
{
lean_object* v___x_2520_; lean_object* v___x_2521_; 
lean_inc(v___x_2512_);
v___x_2520_ = l_Std_Format_pretty(v_a_2519_, v___x_2511_, v___x_2512_, v___x_2512_);
v___x_2521_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2521_, 0, v___x_2520_);
return v___x_2521_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__4___boxed(lean_object* v___x_2535_, lean_object* v___x_2536_, lean_object* v___x_2537_, lean_object* v___x_2538_, lean_object* v___x_2539_, lean_object* v___y_2540_, lean_object* v___y_2541_, lean_object* v___y_2542_){
_start:
{
lean_object* v_res_2543_; 
v_res_2543_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__4(v___x_2535_, v___x_2536_, v___x_2537_, v___x_2538_, v___x_2539_, v___y_2540_, v___y_2541_);
lean_dec(v___y_2541_);
lean_dec_ref(v___y_2540_);
lean_dec_ref(v___x_2539_);
lean_dec(v___x_2536_);
return v_res_2543_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__15(lean_object* v_a_2544_, lean_object* v_as_2545_, size_t v_sz_2546_, size_t v_i_2547_, lean_object* v_b_2548_){
_start:
{
lean_object* v_a_2551_; uint8_t v___x_2555_; 
v___x_2555_ = lean_usize_dec_lt(v_i_2547_, v_sz_2546_);
if (v___x_2555_ == 0)
{
lean_object* v___x_2556_; 
lean_dec_ref(v_a_2544_);
v___x_2556_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2556_, 0, v_b_2548_);
return v___x_2556_;
}
else
{
lean_object* v_fst_2557_; lean_object* v_snd_2558_; lean_object* v___x_2560_; uint8_t v_isShared_2561_; uint8_t v_isSharedCheck_2601_; 
v_fst_2557_ = lean_ctor_get(v_b_2548_, 0);
v_snd_2558_ = lean_ctor_get(v_b_2548_, 1);
v_isSharedCheck_2601_ = !lean_is_exclusive(v_b_2548_);
if (v_isSharedCheck_2601_ == 0)
{
v___x_2560_ = v_b_2548_;
v_isShared_2561_ = v_isSharedCheck_2601_;
goto v_resetjp_2559_;
}
else
{
lean_inc(v_snd_2558_);
lean_inc(v_fst_2557_);
lean_dec(v_b_2548_);
v___x_2560_ = lean_box(0);
v_isShared_2561_ = v_isSharedCheck_2601_;
goto v_resetjp_2559_;
}
v_resetjp_2559_:
{
uint8_t v___x_2562_; lean_object* v_a_2563_; lean_object* v___x_2564_; 
v___x_2562_ = 0;
v_a_2563_ = lean_array_uget_borrowed(v_as_2545_, v_i_2547_);
lean_inc(v_a_2563_);
lean_inc_ref(v_a_2544_);
v___x_2564_ = l_Lean_Environment_find_x3f(v_a_2544_, v_a_2563_, v___x_2562_);
if (lean_obj_tag(v___x_2564_) == 1)
{
lean_object* v_val_2565_; lean_object* v___x_2566_; lean_object* v___x_2567_; lean_object* v___x_2568_; lean_object* v_snd_2569_; lean_object* v_fst_2570_; lean_object* v___x_2572_; uint8_t v_isShared_2573_; uint8_t v_isSharedCheck_2596_; 
lean_del_object(v___x_2560_);
v_val_2565_ = lean_ctor_get(v___x_2564_, 0);
lean_inc(v_val_2565_);
lean_dec_ref_known(v___x_2564_, 1);
v___x_2566_ = l_Lean_ConstantInfo_levelParams(v_val_2565_);
v___x_2567_ = l_Lean_ConstantInfo_type(v_val_2565_);
lean_inc_ref(v___x_2567_);
v___x_2568_ = l_NsExport_sizes(v___x_2566_, v___x_2567_);
v_snd_2569_ = lean_ctor_get(v___x_2568_, 1);
lean_inc(v_snd_2569_);
lean_dec_ref(v___x_2568_);
v_fst_2570_ = lean_ctor_get(v_snd_2569_, 0);
v_isSharedCheck_2596_ = !lean_is_exclusive(v_snd_2569_);
if (v_isSharedCheck_2596_ == 0)
{
lean_object* v_unused_2597_; 
v_unused_2597_ = lean_ctor_get(v_snd_2569_, 1);
lean_dec(v_unused_2597_);
v___x_2572_ = v_snd_2569_;
v_isShared_2573_ = v_isSharedCheck_2596_;
goto v_resetjp_2571_;
}
else
{
lean_inc(v_fst_2570_);
lean_dec(v_snd_2569_);
v___x_2572_ = lean_box(0);
v_isShared_2573_ = v_isSharedCheck_2596_;
goto v_resetjp_2571_;
}
v_resetjp_2571_:
{
lean_object* v___x_2574_; lean_object* v___x_2575_; lean_object* v___x_2576_; lean_object* v___x_2577_; 
v___x_2574_ = lean_nat_add(v_snd_2558_, v_fst_2570_);
lean_dec(v_fst_2570_);
lean_dec(v_snd_2558_);
v___x_2575_ = l_Lean_Expr_getUsedConstants(v___x_2567_);
v___x_2576_ = l_Array_append___redArg(v_fst_2557_, v___x_2575_);
lean_dec_ref(v___x_2575_);
v___x_2577_ = l_NsExport_valueOf_x3f(v_val_2565_);
if (lean_obj_tag(v___x_2577_) == 1)
{
lean_object* v_val_2578_; lean_object* v___x_2579_; lean_object* v_snd_2580_; lean_object* v_fst_2581_; lean_object* v___x_2583_; uint8_t v_isShared_2584_; uint8_t v_isSharedCheck_2591_; 
lean_del_object(v___x_2572_);
v_val_2578_ = lean_ctor_get(v___x_2577_, 0);
lean_inc_n(v_val_2578_, 2);
lean_dec_ref_known(v___x_2577_, 1);
v___x_2579_ = l_NsExport_sizes(v___x_2566_, v_val_2578_);
lean_dec(v___x_2566_);
v_snd_2580_ = lean_ctor_get(v___x_2579_, 1);
lean_inc(v_snd_2580_);
lean_dec_ref(v___x_2579_);
v_fst_2581_ = lean_ctor_get(v_snd_2580_, 0);
v_isSharedCheck_2591_ = !lean_is_exclusive(v_snd_2580_);
if (v_isSharedCheck_2591_ == 0)
{
lean_object* v_unused_2592_; 
v_unused_2592_ = lean_ctor_get(v_snd_2580_, 1);
lean_dec(v_unused_2592_);
v___x_2583_ = v_snd_2580_;
v_isShared_2584_ = v_isSharedCheck_2591_;
goto v_resetjp_2582_;
}
else
{
lean_inc(v_fst_2581_);
lean_dec(v_snd_2580_);
v___x_2583_ = lean_box(0);
v_isShared_2584_ = v_isSharedCheck_2591_;
goto v_resetjp_2582_;
}
v_resetjp_2582_:
{
lean_object* v___x_2585_; lean_object* v___x_2586_; lean_object* v___x_2587_; lean_object* v___x_2589_; 
v___x_2585_ = lean_nat_add(v___x_2574_, v_fst_2581_);
lean_dec(v_fst_2581_);
lean_dec(v___x_2574_);
v___x_2586_ = l_Lean_Expr_getUsedConstants(v_val_2578_);
v___x_2587_ = l_Array_append___redArg(v___x_2576_, v___x_2586_);
lean_dec_ref(v___x_2586_);
if (v_isShared_2584_ == 0)
{
lean_ctor_set(v___x_2583_, 1, v___x_2585_);
lean_ctor_set(v___x_2583_, 0, v___x_2587_);
v___x_2589_ = v___x_2583_;
goto v_reusejp_2588_;
}
else
{
lean_object* v_reuseFailAlloc_2590_; 
v_reuseFailAlloc_2590_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2590_, 0, v___x_2587_);
lean_ctor_set(v_reuseFailAlloc_2590_, 1, v___x_2585_);
v___x_2589_ = v_reuseFailAlloc_2590_;
goto v_reusejp_2588_;
}
v_reusejp_2588_:
{
v_a_2551_ = v___x_2589_;
goto v___jp_2550_;
}
}
}
else
{
lean_object* v___x_2594_; 
lean_dec(v___x_2577_);
lean_dec(v___x_2566_);
if (v_isShared_2573_ == 0)
{
lean_ctor_set(v___x_2572_, 1, v___x_2574_);
lean_ctor_set(v___x_2572_, 0, v___x_2576_);
v___x_2594_ = v___x_2572_;
goto v_reusejp_2593_;
}
else
{
lean_object* v_reuseFailAlloc_2595_; 
v_reuseFailAlloc_2595_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2595_, 0, v___x_2576_);
lean_ctor_set(v_reuseFailAlloc_2595_, 1, v___x_2574_);
v___x_2594_ = v_reuseFailAlloc_2595_;
goto v_reusejp_2593_;
}
v_reusejp_2593_:
{
v_a_2551_ = v___x_2594_;
goto v___jp_2550_;
}
}
}
}
else
{
lean_object* v___x_2599_; 
lean_dec(v___x_2564_);
if (v_isShared_2561_ == 0)
{
v___x_2599_ = v___x_2560_;
goto v_reusejp_2598_;
}
else
{
lean_object* v_reuseFailAlloc_2600_; 
v_reuseFailAlloc_2600_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2600_, 0, v_fst_2557_);
lean_ctor_set(v_reuseFailAlloc_2600_, 1, v_snd_2558_);
v___x_2599_ = v_reuseFailAlloc_2600_;
goto v_reusejp_2598_;
}
v_reusejp_2598_:
{
v_a_2551_ = v___x_2599_;
goto v___jp_2550_;
}
}
}
}
v___jp_2550_:
{
size_t v___x_2552_; size_t v___x_2553_; 
v___x_2552_ = ((size_t)1ULL);
v___x_2553_ = lean_usize_add(v_i_2547_, v___x_2552_);
v_i_2547_ = v___x_2553_;
v_b_2548_ = v_a_2551_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__15___boxed(lean_object* v_a_2602_, lean_object* v_as_2603_, lean_object* v_sz_2604_, lean_object* v_i_2605_, lean_object* v_b_2606_, lean_object* v___y_2607_){
_start:
{
size_t v_sz_boxed_2608_; size_t v_i_boxed_2609_; lean_object* v_res_2610_; 
v_sz_boxed_2608_ = lean_unbox_usize(v_sz_2604_);
lean_dec(v_sz_2604_);
v_i_boxed_2609_ = lean_unbox_usize(v_i_2605_);
lean_dec(v_i_2605_);
v_res_2610_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__15(v_a_2602_, v_as_2603_, v_sz_boxed_2608_, v_i_boxed_2609_, v_b_2606_);
lean_dec_ref(v_as_2603_);
return v_res_2610_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__14(lean_object* v_a_2611_, lean_object* v_as_2612_, size_t v_sz_2613_, size_t v_i_2614_, lean_object* v_b_2615_){
_start:
{
lean_object* v_a_2618_; uint8_t v___x_2622_; 
v___x_2622_ = lean_usize_dec_lt(v_i_2614_, v_sz_2613_);
if (v___x_2622_ == 0)
{
lean_object* v___x_2623_; 
lean_dec_ref(v_a_2611_);
v___x_2623_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2623_, 0, v_b_2615_);
return v___x_2623_;
}
else
{
lean_object* v_snd_2624_; lean_object* v_fst_2625_; lean_object* v___x_2627_; uint8_t v_isShared_2628_; uint8_t v_isSharedCheck_2670_; 
v_snd_2624_ = lean_ctor_get(v_b_2615_, 1);
v_fst_2625_ = lean_ctor_get(v_b_2615_, 0);
v_isSharedCheck_2670_ = !lean_is_exclusive(v_b_2615_);
if (v_isSharedCheck_2670_ == 0)
{
v___x_2627_ = v_b_2615_;
v_isShared_2628_ = v_isSharedCheck_2670_;
goto v_resetjp_2626_;
}
else
{
lean_inc(v_snd_2624_);
lean_inc(v_fst_2625_);
lean_dec(v_b_2615_);
v___x_2627_ = lean_box(0);
v_isShared_2628_ = v_isSharedCheck_2670_;
goto v_resetjp_2626_;
}
v_resetjp_2626_:
{
lean_object* v_fst_2629_; lean_object* v_snd_2630_; lean_object* v___x_2632_; uint8_t v_isShared_2633_; uint8_t v_isSharedCheck_2669_; 
v_fst_2629_ = lean_ctor_get(v_snd_2624_, 0);
v_snd_2630_ = lean_ctor_get(v_snd_2624_, 1);
v_isSharedCheck_2669_ = !lean_is_exclusive(v_snd_2624_);
if (v_isSharedCheck_2669_ == 0)
{
v___x_2632_ = v_snd_2624_;
v_isShared_2633_ = v_isSharedCheck_2669_;
goto v_resetjp_2631_;
}
else
{
lean_inc(v_snd_2630_);
lean_inc(v_fst_2629_);
lean_dec(v_snd_2624_);
v___x_2632_ = lean_box(0);
v_isShared_2633_ = v_isSharedCheck_2669_;
goto v_resetjp_2631_;
}
v_resetjp_2631_:
{
uint8_t v___x_2634_; lean_object* v_a_2635_; lean_object* v___x_2636_; 
v___x_2634_ = 0;
v_a_2635_ = lean_array_uget_borrowed(v_as_2612_, v_i_2614_);
lean_inc(v_a_2635_);
lean_inc_ref(v_a_2611_);
v___x_2636_ = l_Lean_Environment_find_x3f(v_a_2611_, v_a_2635_, v___x_2634_);
if (lean_obj_tag(v___x_2636_) == 1)
{
lean_object* v_val_2637_; lean_object* v___x_2638_; lean_object* v___x_2639_; lean_object* v___x_2640_; lean_object* v_snd_2641_; lean_object* v_fst_2642_; lean_object* v___x_2644_; uint8_t v_isShared_2645_; uint8_t v_isSharedCheck_2662_; 
lean_del_object(v___x_2632_);
lean_del_object(v___x_2627_);
v_val_2637_ = lean_ctor_get(v___x_2636_, 0);
lean_inc(v_val_2637_);
lean_dec_ref_known(v___x_2636_, 1);
v___x_2638_ = l_Lean_ConstantInfo_levelParams(v_val_2637_);
v___x_2639_ = l_Lean_ConstantInfo_type(v_val_2637_);
lean_dec(v_val_2637_);
lean_inc_ref(v___x_2639_);
v___x_2640_ = l_NsExport_sizes(v___x_2638_, v___x_2639_);
lean_dec(v___x_2638_);
v_snd_2641_ = lean_ctor_get(v___x_2640_, 1);
v_fst_2642_ = lean_ctor_get(v___x_2640_, 0);
v_isSharedCheck_2662_ = !lean_is_exclusive(v___x_2640_);
if (v_isSharedCheck_2662_ == 0)
{
v___x_2644_ = v___x_2640_;
v_isShared_2645_ = v_isSharedCheck_2662_;
goto v_resetjp_2643_;
}
else
{
lean_inc(v_snd_2641_);
lean_inc(v_fst_2642_);
lean_dec(v___x_2640_);
v___x_2644_ = lean_box(0);
v_isShared_2645_ = v_isSharedCheck_2662_;
goto v_resetjp_2643_;
}
v_resetjp_2643_:
{
lean_object* v_fst_2646_; lean_object* v___x_2648_; uint8_t v_isShared_2649_; uint8_t v_isSharedCheck_2660_; 
v_fst_2646_ = lean_ctor_get(v_snd_2641_, 0);
v_isSharedCheck_2660_ = !lean_is_exclusive(v_snd_2641_);
if (v_isSharedCheck_2660_ == 0)
{
lean_object* v_unused_2661_; 
v_unused_2661_ = lean_ctor_get(v_snd_2641_, 1);
lean_dec(v_unused_2661_);
v___x_2648_ = v_snd_2641_;
v_isShared_2649_ = v_isSharedCheck_2660_;
goto v_resetjp_2647_;
}
else
{
lean_inc(v_fst_2646_);
lean_dec(v_snd_2641_);
v___x_2648_ = lean_box(0);
v_isShared_2649_ = v_isSharedCheck_2660_;
goto v_resetjp_2647_;
}
v_resetjp_2647_:
{
lean_object* v___x_2650_; lean_object* v___x_2651_; lean_object* v___x_2652_; lean_object* v___x_2653_; lean_object* v___x_2655_; 
v___x_2650_ = lean_nat_add(v_fst_2629_, v_fst_2642_);
lean_dec(v_fst_2642_);
lean_dec(v_fst_2629_);
v___x_2651_ = lean_nat_add(v_snd_2630_, v_fst_2646_);
lean_dec(v_fst_2646_);
lean_dec(v_snd_2630_);
v___x_2652_ = l_Lean_Expr_getUsedConstants(v___x_2639_);
v___x_2653_ = l_Array_append___redArg(v_fst_2625_, v___x_2652_);
lean_dec_ref(v___x_2652_);
if (v_isShared_2649_ == 0)
{
lean_ctor_set(v___x_2648_, 1, v___x_2651_);
lean_ctor_set(v___x_2648_, 0, v___x_2650_);
v___x_2655_ = v___x_2648_;
goto v_reusejp_2654_;
}
else
{
lean_object* v_reuseFailAlloc_2659_; 
v_reuseFailAlloc_2659_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2659_, 0, v___x_2650_);
lean_ctor_set(v_reuseFailAlloc_2659_, 1, v___x_2651_);
v___x_2655_ = v_reuseFailAlloc_2659_;
goto v_reusejp_2654_;
}
v_reusejp_2654_:
{
lean_object* v___x_2657_; 
if (v_isShared_2645_ == 0)
{
lean_ctor_set(v___x_2644_, 1, v___x_2655_);
lean_ctor_set(v___x_2644_, 0, v___x_2653_);
v___x_2657_ = v___x_2644_;
goto v_reusejp_2656_;
}
else
{
lean_object* v_reuseFailAlloc_2658_; 
v_reuseFailAlloc_2658_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2658_, 0, v___x_2653_);
lean_ctor_set(v_reuseFailAlloc_2658_, 1, v___x_2655_);
v___x_2657_ = v_reuseFailAlloc_2658_;
goto v_reusejp_2656_;
}
v_reusejp_2656_:
{
v_a_2618_ = v___x_2657_;
goto v___jp_2617_;
}
}
}
}
}
else
{
lean_object* v___x_2664_; 
lean_dec(v___x_2636_);
if (v_isShared_2633_ == 0)
{
v___x_2664_ = v___x_2632_;
goto v_reusejp_2663_;
}
else
{
lean_object* v_reuseFailAlloc_2668_; 
v_reuseFailAlloc_2668_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2668_, 0, v_fst_2629_);
lean_ctor_set(v_reuseFailAlloc_2668_, 1, v_snd_2630_);
v___x_2664_ = v_reuseFailAlloc_2668_;
goto v_reusejp_2663_;
}
v_reusejp_2663_:
{
lean_object* v___x_2666_; 
if (v_isShared_2628_ == 0)
{
lean_ctor_set(v___x_2627_, 1, v___x_2664_);
v___x_2666_ = v___x_2627_;
goto v_reusejp_2665_;
}
else
{
lean_object* v_reuseFailAlloc_2667_; 
v_reuseFailAlloc_2667_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2667_, 0, v_fst_2625_);
lean_ctor_set(v_reuseFailAlloc_2667_, 1, v___x_2664_);
v___x_2666_ = v_reuseFailAlloc_2667_;
goto v_reusejp_2665_;
}
v_reusejp_2665_:
{
v_a_2618_ = v___x_2666_;
goto v___jp_2617_;
}
}
}
}
}
}
v___jp_2617_:
{
size_t v___x_2619_; size_t v___x_2620_; 
v___x_2619_ = ((size_t)1ULL);
v___x_2620_ = lean_usize_add(v_i_2614_, v___x_2619_);
v_i_2614_ = v___x_2620_;
v_b_2615_ = v_a_2618_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__14___boxed(lean_object* v_a_2671_, lean_object* v_as_2672_, lean_object* v_sz_2673_, lean_object* v_i_2674_, lean_object* v_b_2675_, lean_object* v___y_2676_){
_start:
{
size_t v_sz_boxed_2677_; size_t v_i_boxed_2678_; lean_object* v_res_2679_; 
v_sz_boxed_2677_ = lean_unbox_usize(v_sz_2673_);
lean_dec(v_sz_2673_);
v_i_boxed_2678_ = lean_unbox_usize(v_i_2674_);
lean_dec(v_i_2674_);
v_res_2679_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__14(v_a_2671_, v_as_2672_, v_sz_boxed_2677_, v_i_boxed_2678_, v_b_2675_);
lean_dec_ref(v_as_2672_);
return v_res_2679_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__2(lean_object* v___x_2680_, lean_object* v___x_2681_, lean_object* v___x_2682_, lean_object* v_fst_2683_, lean_object* v___x_2684_, lean_object* v___y_2685_, lean_object* v___y_2686_){
_start:
{
lean_object* v_a_2689_; lean_object* v___x_2693_; lean_object* v___x_2694_; 
v___x_2693_ = lean_st_mk_ref(v___x_2680_);
v___x_2694_ = l_Lean_PrettyPrinter_ppSignature(v_fst_2683_, v___x_2684_, v___x_2693_, v___y_2685_, v___y_2686_);
if (lean_obj_tag(v___x_2694_) == 0)
{
lean_object* v_a_2695_; lean_object* v___x_2696_; 
v_a_2695_ = lean_ctor_get(v___x_2694_, 0);
lean_inc(v_a_2695_);
lean_dec_ref_known(v___x_2694_, 1);
v___x_2696_ = lean_st_ref_get(v___x_2693_);
lean_dec(v___x_2693_);
lean_dec(v___x_2696_);
v_a_2689_ = v_a_2695_;
goto v___jp_2688_;
}
else
{
lean_dec(v___x_2693_);
if (lean_obj_tag(v___x_2694_) == 0)
{
lean_object* v_a_2697_; 
v_a_2697_ = lean_ctor_get(v___x_2694_, 0);
lean_inc(v_a_2697_);
lean_dec_ref_known(v___x_2694_, 1);
v_a_2689_ = v_a_2697_;
goto v___jp_2688_;
}
else
{
lean_object* v_a_2698_; lean_object* v___x_2700_; uint8_t v_isShared_2701_; uint8_t v_isSharedCheck_2705_; 
lean_dec(v___x_2682_);
v_a_2698_ = lean_ctor_get(v___x_2694_, 0);
v_isSharedCheck_2705_ = !lean_is_exclusive(v___x_2694_);
if (v_isSharedCheck_2705_ == 0)
{
v___x_2700_ = v___x_2694_;
v_isShared_2701_ = v_isSharedCheck_2705_;
goto v_resetjp_2699_;
}
else
{
lean_inc(v_a_2698_);
lean_dec(v___x_2694_);
v___x_2700_ = lean_box(0);
v_isShared_2701_ = v_isSharedCheck_2705_;
goto v_resetjp_2699_;
}
v_resetjp_2699_:
{
lean_object* v___x_2703_; 
if (v_isShared_2701_ == 0)
{
v___x_2703_ = v___x_2700_;
goto v_reusejp_2702_;
}
else
{
lean_object* v_reuseFailAlloc_2704_; 
v_reuseFailAlloc_2704_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2704_, 0, v_a_2698_);
v___x_2703_ = v_reuseFailAlloc_2704_;
goto v_reusejp_2702_;
}
v_reusejp_2702_:
{
return v___x_2703_;
}
}
}
}
v___jp_2688_:
{
lean_object* v_fmt_2690_; lean_object* v___x_2691_; lean_object* v___x_2692_; 
v_fmt_2690_ = lean_ctor_get(v_a_2689_, 0);
lean_inc(v_fmt_2690_);
lean_dec_ref(v_a_2689_);
lean_inc(v___x_2682_);
v___x_2691_ = l_Std_Format_pretty(v_fmt_2690_, v___x_2681_, v___x_2682_, v___x_2682_);
v___x_2692_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2692_, 0, v___x_2691_);
return v___x_2692_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__2___boxed(lean_object* v___x_2706_, lean_object* v___x_2707_, lean_object* v___x_2708_, lean_object* v_fst_2709_, lean_object* v___x_2710_, lean_object* v___y_2711_, lean_object* v___y_2712_, lean_object* v___y_2713_){
_start:
{
lean_object* v_res_2714_; 
v_res_2714_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__2(v___x_2706_, v___x_2707_, v___x_2708_, v_fst_2709_, v___x_2710_, v___y_2711_, v___y_2712_);
lean_dec(v___y_2712_);
lean_dec_ref(v___y_2711_);
lean_dec_ref(v___x_2710_);
lean_dec(v___x_2707_);
return v_res_2714_;
}
}
LEAN_EXPORT lean_object* l_List_mapTR_loop___at___00NsExport_main_spec__4(lean_object* v_a_2715_, lean_object* v_a_2716_){
_start:
{
if (lean_obj_tag(v_a_2715_) == 0)
{
lean_object* v___x_2717_; 
v___x_2717_ = l_List_reverse___redArg(v_a_2716_);
return v___x_2717_;
}
else
{
lean_object* v_head_2718_; lean_object* v_tail_2719_; lean_object* v___x_2721_; uint8_t v_isShared_2722_; uint8_t v_isSharedCheck_2738_; 
v_head_2718_ = lean_ctor_get(v_a_2715_, 0);
v_tail_2719_ = lean_ctor_get(v_a_2715_, 1);
v_isSharedCheck_2738_ = !lean_is_exclusive(v_a_2715_);
if (v_isSharedCheck_2738_ == 0)
{
v___x_2721_ = v_a_2715_;
v_isShared_2722_ = v_isSharedCheck_2738_;
goto v_resetjp_2720_;
}
else
{
lean_inc(v_tail_2719_);
lean_inc(v_head_2718_);
lean_dec(v_a_2715_);
v___x_2721_ = lean_box(0);
v_isShared_2722_ = v_isSharedCheck_2738_;
goto v_resetjp_2720_;
}
v_resetjp_2720_:
{
lean_object* v_fst_2723_; lean_object* v_snd_2724_; lean_object* v___x_2726_; uint8_t v_isShared_2727_; uint8_t v_isSharedCheck_2737_; 
v_fst_2723_ = lean_ctor_get(v_head_2718_, 0);
v_snd_2724_ = lean_ctor_get(v_head_2718_, 1);
v_isSharedCheck_2737_ = !lean_is_exclusive(v_head_2718_);
if (v_isSharedCheck_2737_ == 0)
{
v___x_2726_ = v_head_2718_;
v_isShared_2727_ = v_isSharedCheck_2737_;
goto v_resetjp_2725_;
}
else
{
lean_inc(v_snd_2724_);
lean_inc(v_fst_2723_);
lean_dec(v_head_2718_);
v___x_2726_ = lean_box(0);
v_isShared_2727_ = v_isSharedCheck_2737_;
goto v_resetjp_2725_;
}
v_resetjp_2725_:
{
lean_object* v___x_2728_; lean_object* v___x_2729_; lean_object* v___x_2731_; 
v___x_2728_ = l_Lean_JsonNumber_fromNat(v_snd_2724_);
v___x_2729_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_2729_, 0, v___x_2728_);
if (v_isShared_2727_ == 0)
{
lean_ctor_set(v___x_2726_, 1, v___x_2729_);
v___x_2731_ = v___x_2726_;
goto v_reusejp_2730_;
}
else
{
lean_object* v_reuseFailAlloc_2736_; 
v_reuseFailAlloc_2736_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2736_, 0, v_fst_2723_);
lean_ctor_set(v_reuseFailAlloc_2736_, 1, v___x_2729_);
v___x_2731_ = v_reuseFailAlloc_2736_;
goto v_reusejp_2730_;
}
v_reusejp_2730_:
{
lean_object* v___x_2733_; 
if (v_isShared_2722_ == 0)
{
lean_ctor_set(v___x_2721_, 1, v_a_2716_);
lean_ctor_set(v___x_2721_, 0, v___x_2731_);
v___x_2733_ = v___x_2721_;
goto v_reusejp_2732_;
}
else
{
lean_object* v_reuseFailAlloc_2735_; 
v_reuseFailAlloc_2735_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2735_, 0, v___x_2731_);
lean_ctor_set(v_reuseFailAlloc_2735_, 1, v_a_2716_);
v___x_2733_ = v_reuseFailAlloc_2735_;
goto v_reusejp_2732_;
}
v_reusejp_2732_:
{
v_a_2715_ = v_tail_2719_;
v_a_2716_ = v___x_2733_;
goto _start;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_foldrM___at___00NsExport_main_spec__7(lean_object* v_x_2739_, lean_object* v_x_2740_){
_start:
{
if (lean_obj_tag(v_x_2740_) == 0)
{
lean_inc(v_x_2739_);
return v_x_2739_;
}
else
{
lean_object* v_key_2741_; lean_object* v_value_2742_; lean_object* v_tail_2743_; lean_object* v___x_2744_; lean_object* v___x_2745_; lean_object* v___x_2746_; 
v_key_2741_ = lean_ctor_get(v_x_2740_, 0);
v_value_2742_ = lean_ctor_get(v_x_2740_, 1);
v_tail_2743_ = lean_ctor_get(v_x_2740_, 2);
v___x_2744_ = l_Std_DHashMap_Internal_AssocList_foldrM___at___00NsExport_main_spec__7(v_x_2739_, v_tail_2743_);
lean_inc(v_value_2742_);
lean_inc(v_key_2741_);
v___x_2745_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2745_, 0, v_key_2741_);
lean_ctor_set(v___x_2745_, 1, v_value_2742_);
v___x_2746_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_2746_, 0, v___x_2745_);
lean_ctor_set(v___x_2746_, 1, v___x_2744_);
return v___x_2746_;
}
}
}
LEAN_EXPORT lean_object* l_Std_DHashMap_Internal_AssocList_foldrM___at___00NsExport_main_spec__7___boxed(lean_object* v_x_2747_, lean_object* v_x_2748_){
_start:
{
lean_object* v_res_2749_; 
v_res_2749_ = l_Std_DHashMap_Internal_AssocList_foldrM___at___00NsExport_main_spec__7(v_x_2747_, v_x_2748_);
lean_dec(v_x_2748_);
lean_dec(v_x_2747_);
return v_res_2749_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00NsExport_main_spec__8(lean_object* v_as_2750_, size_t v_i_2751_, size_t v_stop_2752_, lean_object* v_b_2753_){
_start:
{
uint8_t v___x_2754_; 
v___x_2754_ = lean_usize_dec_eq(v_i_2751_, v_stop_2752_);
if (v___x_2754_ == 0)
{
size_t v___x_2755_; size_t v___x_2756_; lean_object* v___x_2757_; lean_object* v___x_2758_; 
v___x_2755_ = ((size_t)1ULL);
v___x_2756_ = lean_usize_sub(v_i_2751_, v___x_2755_);
v___x_2757_ = lean_array_uget_borrowed(v_as_2750_, v___x_2756_);
v___x_2758_ = l_Std_DHashMap_Internal_AssocList_foldrM___at___00NsExport_main_spec__7(v_b_2753_, v___x_2757_);
lean_dec(v_b_2753_);
v_i_2751_ = v___x_2756_;
v_b_2753_ = v___x_2758_;
goto _start;
}
else
{
return v_b_2753_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00NsExport_main_spec__8___boxed(lean_object* v_as_2760_, lean_object* v_i_2761_, lean_object* v_stop_2762_, lean_object* v_b_2763_){
_start:
{
size_t v_i_boxed_2764_; size_t v_stop_boxed_2765_; lean_object* v_res_2766_; 
v_i_boxed_2764_ = lean_unbox_usize(v_i_2761_);
lean_dec(v_i_2761_);
v_stop_boxed_2765_ = lean_unbox_usize(v_stop_2762_);
lean_dec(v_stop_2762_);
v_res_2766_ = l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00NsExport_main_spec__8(v_as_2760_, v_i_boxed_2764_, v_stop_boxed_2765_, v_b_2763_);
lean_dec_ref(v_as_2760_);
return v_res_2766_;
}
}
LEAN_EXPORT lean_object* l___private_Std_Data_DHashMap_Internal_AssocList_Basic_0__Std_DHashMap_Internal_AssocList_forInStep_go___at___00NsExport_main_spec__5(lean_object* v_a_2767_, lean_object* v_a_2768_, lean_object* v_a_2769_){
_start:
{
if (lean_obj_tag(v_a_2768_) == 0)
{
lean_object* v___x_2770_; 
v___x_2770_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_2770_, 0, v_a_2769_);
return v___x_2770_;
}
else
{
lean_object* v_key_2771_; lean_object* v_tail_2772_; uint8_t v___x_2773_; lean_object* v___x_2774_; lean_object* v___x_2775_; lean_object* v___x_2776_; lean_object* v___x_2777_; lean_object* v___x_2778_; lean_object* v___x_2779_; lean_object* v___x_2780_; lean_object* v___x_2781_; 
v_key_2771_ = lean_ctor_get(v_a_2768_, 0);
v_tail_2772_ = lean_ctor_get(v_a_2768_, 2);
v___x_2773_ = 1;
v___x_2774_ = lean_unsigned_to_nat(0u);
v___x_2775_ = lean_unsigned_to_nat(1u);
v___x_2776_ = l_NsExport_moduleOf(v_a_2767_, v_key_2771_);
v___x_2777_ = l_Lean_Name_getRoot(v___x_2776_);
lean_dec(v___x_2776_);
v___x_2778_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v___x_2777_, v___x_2773_);
v___x_2779_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Server_Watchdog_handleRename_spec__1___redArg(v_a_2769_, v___x_2778_, v___x_2774_);
v___x_2780_ = lean_nat_add(v___x_2779_, v___x_2775_);
lean_dec(v___x_2779_);
v___x_2781_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00Lean_Server_Test_Cancel_mkTestTask_spec__1___redArg(v_a_2769_, v___x_2778_, v___x_2780_);
v_a_2768_ = v_tail_2772_;
v_a_2769_ = v___x_2781_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Std_Data_DHashMap_Internal_AssocList_Basic_0__Std_DHashMap_Internal_AssocList_forInStep_go___at___00NsExport_main_spec__5___boxed(lean_object* v_a_2783_, lean_object* v_a_2784_, lean_object* v_a_2785_){
_start:
{
lean_object* v_res_2786_; 
v_res_2786_ = l___private_Std_Data_DHashMap_Internal_AssocList_Basic_0__Std_DHashMap_Internal_AssocList_forInStep_go___at___00NsExport_main_spec__5(v_a_2783_, v_a_2784_, v_a_2785_);
lean_dec(v_a_2784_);
lean_dec_ref(v_a_2783_);
return v_res_2786_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__6(lean_object* v_a_2787_, lean_object* v_as_2788_, size_t v_sz_2789_, size_t v_i_2790_, lean_object* v_b_2791_){
_start:
{
uint8_t v___x_2792_; 
v___x_2792_ = lean_usize_dec_lt(v_i_2790_, v_sz_2789_);
if (v___x_2792_ == 0)
{
return v_b_2791_;
}
else
{
lean_object* v_a_2793_; lean_object* v___x_2794_; 
v_a_2793_ = lean_array_uget_borrowed(v_as_2788_, v_i_2790_);
v___x_2794_ = l___private_Std_Data_DHashMap_Internal_AssocList_Basic_0__Std_DHashMap_Internal_AssocList_forInStep_go___at___00NsExport_main_spec__5(v_a_2787_, v_a_2793_, v_b_2791_);
if (lean_obj_tag(v___x_2794_) == 0)
{
lean_object* v_a_2795_; 
v_a_2795_ = lean_ctor_get(v___x_2794_, 0);
lean_inc(v_a_2795_);
lean_dec_ref_known(v___x_2794_, 1);
return v_a_2795_;
}
else
{
lean_object* v_a_2796_; size_t v___x_2797_; size_t v___x_2798_; 
v_a_2796_ = lean_ctor_get(v___x_2794_, 0);
lean_inc(v_a_2796_);
lean_dec_ref_known(v___x_2794_, 1);
v___x_2797_ = ((size_t)1ULL);
v___x_2798_ = lean_usize_add(v_i_2790_, v___x_2797_);
v_i_2790_ = v___x_2798_;
v_b_2791_ = v_a_2796_;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__6___boxed(lean_object* v_a_2800_, lean_object* v_as_2801_, lean_object* v_sz_2802_, lean_object* v_i_2803_, lean_object* v_b_2804_){
_start:
{
size_t v_sz_boxed_2805_; size_t v_i_boxed_2806_; lean_object* v_res_2807_; 
v_sz_boxed_2805_ = lean_unbox_usize(v_sz_2802_);
lean_dec(v_sz_2802_);
v_i_boxed_2806_ = lean_unbox_usize(v_i_2803_);
lean_dec(v_i_2803_);
v_res_2807_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__6(v_a_2800_, v_as_2801_, v_sz_boxed_2805_, v_i_boxed_2806_, v_b_2804_);
lean_dec_ref(v_as_2801_);
lean_dec_ref(v_a_2800_);
return v_res_2807_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___closed__0(void){
_start:
{
lean_object* v___x_2808_; lean_object* v___x_2809_; lean_object* v___x_2810_; 
v___x_2808_ = lean_box(0);
v___x_2809_ = lean_unsigned_to_nat(16u);
v___x_2810_ = lean_mk_array(v___x_2809_, v___x_2808_);
return v___x_2810_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0(lean_object* v___x_2811_, lean_object* v_a_2812_, lean_object* v_xs_2813_){
_start:
{
lean_object* v___y_2815_; lean_object* v_buckets_2819_; lean_object* v___x_2821_; uint8_t v_isShared_2822_; uint8_t v_isSharedCheck_2836_; 
v_buckets_2819_ = lean_ctor_get(v_xs_2813_, 1);
v_isSharedCheck_2836_ = !lean_is_exclusive(v_xs_2813_);
if (v_isSharedCheck_2836_ == 0)
{
lean_object* v_unused_2837_; 
v_unused_2837_ = lean_ctor_get(v_xs_2813_, 0);
lean_dec(v_unused_2837_);
v___x_2821_ = v_xs_2813_;
v_isShared_2822_ = v_isSharedCheck_2836_;
goto v_resetjp_2820_;
}
else
{
lean_inc(v_buckets_2819_);
lean_dec(v_xs_2813_);
v___x_2821_ = lean_box(0);
v_isShared_2822_ = v_isSharedCheck_2836_;
goto v_resetjp_2820_;
}
v___jp_2814_:
{
lean_object* v___x_2816_; lean_object* v___x_2817_; lean_object* v___x_2818_; 
v___x_2816_ = lean_box(0);
v___x_2817_ = l_List_mapTR_loop___at___00NsExport_main_spec__4(v___y_2815_, v___x_2816_);
v___x_2818_ = l_Lean_Json_mkObj(v___x_2817_);
lean_dec(v___x_2817_);
return v___x_2818_;
}
v_resetjp_2820_:
{
lean_object* v___x_2823_; lean_object* v___x_2825_; 
v___x_2823_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___closed__0);
lean_inc(v___x_2811_);
if (v_isShared_2822_ == 0)
{
lean_ctor_set(v___x_2821_, 1, v___x_2823_);
lean_ctor_set(v___x_2821_, 0, v___x_2811_);
v___x_2825_ = v___x_2821_;
goto v_reusejp_2824_;
}
else
{
lean_object* v_reuseFailAlloc_2835_; 
v_reuseFailAlloc_2835_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2835_, 0, v___x_2811_);
lean_ctor_set(v_reuseFailAlloc_2835_, 1, v___x_2823_);
v___x_2825_ = v_reuseFailAlloc_2835_;
goto v_reusejp_2824_;
}
v_reusejp_2824_:
{
size_t v_sz_2826_; size_t v___x_2827_; lean_object* v___x_2828_; lean_object* v_buckets_2829_; lean_object* v___x_2830_; lean_object* v___x_2831_; uint8_t v___x_2832_; 
v_sz_2826_ = lean_array_size(v_buckets_2819_);
v___x_2827_ = ((size_t)0ULL);
v___x_2828_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__6(v_a_2812_, v_buckets_2819_, v_sz_2826_, v___x_2827_, v___x_2825_);
lean_dec_ref(v_buckets_2819_);
v_buckets_2829_ = lean_ctor_get(v___x_2828_, 1);
lean_inc_ref(v_buckets_2829_);
lean_dec_ref(v___x_2828_);
v___x_2830_ = lean_box(0);
v___x_2831_ = lean_array_get_size(v_buckets_2829_);
v___x_2832_ = lean_nat_dec_lt(v___x_2811_, v___x_2831_);
lean_dec(v___x_2811_);
if (v___x_2832_ == 0)
{
lean_dec_ref(v_buckets_2829_);
v___y_2815_ = v___x_2830_;
goto v___jp_2814_;
}
else
{
size_t v___x_2833_; lean_object* v___x_2834_; 
v___x_2833_ = lean_usize_of_nat(v___x_2831_);
v___x_2834_ = l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00NsExport_main_spec__8(v_buckets_2829_, v___x_2833_, v___x_2827_, v___x_2830_);
lean_dec_ref(v_buckets_2829_);
v___y_2815_ = v___x_2834_;
goto v___jp_2814_;
}
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0___boxed(lean_object* v___x_2838_, lean_object* v_a_2839_, lean_object* v_xs_2840_){
_start:
{
lean_object* v_res_2841_; 
v_res_2841_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0(v___x_2838_, v_a_2839_, v_xs_2840_);
lean_dec_ref(v_a_2839_);
return v_res_2841_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__3(lean_object* v___x_2842_, lean_object* v___x_2843_, lean_object* v___x_2844_, lean_object* v___y_2845_, lean_object* v___y_2846_){
_start:
{
lean_object* v___x_2848_; lean_object* v___x_2849_; 
v___x_2848_ = lean_st_mk_ref(v___x_2842_);
v___x_2849_ = l_Lean_Meta_isProp(v___x_2843_, v___x_2844_, v___x_2848_, v___y_2845_, v___y_2846_);
if (lean_obj_tag(v___x_2849_) == 0)
{
lean_object* v_a_2850_; lean_object* v___x_2852_; uint8_t v_isShared_2853_; uint8_t v_isSharedCheck_2858_; 
v_a_2850_ = lean_ctor_get(v___x_2849_, 0);
v_isSharedCheck_2858_ = !lean_is_exclusive(v___x_2849_);
if (v_isSharedCheck_2858_ == 0)
{
v___x_2852_ = v___x_2849_;
v_isShared_2853_ = v_isSharedCheck_2858_;
goto v_resetjp_2851_;
}
else
{
lean_inc(v_a_2850_);
lean_dec(v___x_2849_);
v___x_2852_ = lean_box(0);
v_isShared_2853_ = v_isSharedCheck_2858_;
goto v_resetjp_2851_;
}
v_resetjp_2851_:
{
lean_object* v___x_2854_; lean_object* v___x_2856_; 
v___x_2854_ = lean_st_ref_get(v___x_2848_);
lean_dec(v___x_2848_);
lean_dec(v___x_2854_);
if (v_isShared_2853_ == 0)
{
v___x_2856_ = v___x_2852_;
goto v_reusejp_2855_;
}
else
{
lean_object* v_reuseFailAlloc_2857_; 
v_reuseFailAlloc_2857_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2857_, 0, v_a_2850_);
v___x_2856_ = v_reuseFailAlloc_2857_;
goto v_reusejp_2855_;
}
v_reusejp_2855_:
{
return v___x_2856_;
}
}
}
else
{
lean_dec(v___x_2848_);
return v___x_2849_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__3___boxed(lean_object* v___x_2859_, lean_object* v___x_2860_, lean_object* v___x_2861_, lean_object* v___y_2862_, lean_object* v___y_2863_, lean_object* v___y_2864_){
_start:
{
lean_object* v_res_2865_; 
v_res_2865_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__3(v___x_2859_, v___x_2860_, v___x_2861_, v___y_2862_, v___y_2863_);
lean_dec(v___y_2863_);
lean_dec_ref(v___y_2862_);
lean_dec_ref(v___x_2861_);
return v_res_2865_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(lean_object* v___x_2866_, lean_object* v___x_2867_, lean_object* v___x_2868_, uint8_t v___x_2869_, lean_object* v_a_2870_, lean_object* v___x_2871_, lean_object* v___x_2872_, lean_object* v___x_2873_, lean_object* v___x_2874_, lean_object* v___x_2875_, lean_object* v___x_2876_, lean_object* v___x_2877_, uint8_t v___x_2878_, lean_object* v_00_u03b1_2879_, lean_object* v_x_2880_){
_start:
{
lean_object* v___x_2885_; lean_object* v___x_2886_; lean_object* v___x_2887_; size_t v___x_2888_; lean_object* v___x_2889_; lean_object* v___x_2890_; lean_object* v___x_2891_; lean_object* v___x_2892_; lean_object* v___x_2893_; lean_object* v___x_2894_; lean_object* v___x_2895_; lean_object* v___x_2896_; lean_object* v___x_2897_; lean_object* v___x_2898_; lean_object* v___x_2899_; uint64_t v___x_2900_; lean_object* v___x_2901_; lean_object* v___x_2902_; lean_object* v___x_2903_; lean_object* v___x_2904_; lean_object* v___x_2905_; lean_object* v___x_2906_; lean_object* v___x_2907_; lean_object* v___x_2908_; lean_object* v_env_2909_; lean_object* v___x_2910_; uint8_t v___x_2911_; lean_object* v_fileName_2913_; lean_object* v_fileMap_2914_; lean_object* v_currRecDepth_2915_; lean_object* v_ref_2916_; lean_object* v_currNamespace_2917_; lean_object* v_openDecls_2918_; lean_object* v_initHeartbeats_2919_; lean_object* v_maxHeartbeats_2920_; lean_object* v_quotContext_2921_; lean_object* v_currMacroScope_2922_; lean_object* v_cancelTk_x3f_2923_; uint8_t v_suppressElabErrors_2924_; lean_object* v_inheritedTraceOptions_2925_; lean_object* v___y_2926_; uint8_t v___y_2947_; uint8_t v___x_2967_; 
v___x_2885_ = lean_unsigned_to_nat(32u);
v___x_2886_ = lean_mk_empty_array_with_capacity(v___x_2885_);
v___x_2887_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0);
v___x_2888_ = ((size_t)5ULL);
lean_inc_n(v___x_2866_, 2);
v___x_2889_ = lean_alloc_ctor(0, 4, sizeof(size_t)*1);
lean_ctor_set(v___x_2889_, 0, v___x_2887_);
lean_ctor_set(v___x_2889_, 1, v___x_2886_);
lean_ctor_set(v___x_2889_, 2, v___x_2866_);
lean_ctor_set(v___x_2889_, 3, v___x_2866_);
lean_ctor_set_usize(v___x_2889_, 4, v___x_2888_);
v___x_2890_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2);
v___x_2891_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3);
v___x_2892_ = lean_box(1);
lean_inc_ref_n(v___x_2889_, 3);
v___x_2893_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_2893_, 0, v___x_2889_);
lean_ctor_set(v___x_2893_, 1, v___x_2889_);
lean_ctor_set(v___x_2893_, 2, v___x_2892_);
v___x_2894_ = lean_io_get_num_heartbeats();
v___x_2895_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__5));
lean_inc_n(v___x_2867_, 2);
v___x_2896_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2896_, 0, v___x_2895_);
lean_ctor_set(v___x_2896_, 1, v___x_2867_);
v___x_2897_ = lean_unsigned_to_nat(2u);
v___x_2898_ = lean_box(0);
lean_inc(v___x_2868_);
v___x_2899_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_2899_, 0, v___x_2868_);
lean_ctor_set(v___x_2899_, 1, v___x_2867_);
lean_ctor_set(v___x_2899_, 2, v___x_2898_);
v___x_2900_ = 0ULL;
v___x_2901_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_2901_, 0, v___x_2889_);
lean_ctor_set_uint64(v___x_2901_, sizeof(void*)*1, v___x_2900_);
v___x_2902_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_2902_, 0, v___x_2890_);
lean_ctor_set(v___x_2902_, 1, v___x_2890_);
lean_ctor_set(v___x_2902_, 2, v___x_2889_);
lean_ctor_set_uint8(v___x_2902_, sizeof(void*)*3, v___x_2869_);
v___x_2903_ = lean_mk_empty_array_with_capacity(v___x_2866_);
v___x_2904_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_2904_, 0, v_a_2870_);
lean_ctor_set(v___x_2904_, 1, v___x_2897_);
lean_ctor_set(v___x_2904_, 2, v___x_2896_);
lean_ctor_set(v___x_2904_, 3, v___x_2899_);
lean_ctor_set(v___x_2904_, 4, v___x_2901_);
lean_ctor_set(v___x_2904_, 5, v___x_2891_);
lean_ctor_set(v___x_2904_, 6, v___x_2893_);
lean_ctor_set(v___x_2904_, 7, v___x_2902_);
lean_ctor_set(v___x_2904_, 8, v___x_2903_);
v___x_2905_ = lean_st_mk_ref(v___x_2904_);
v___x_2906_ = l_Lean_inheritedTraceOptions;
v___x_2907_ = lean_st_ref_get(v___x_2906_);
v___x_2908_ = lean_st_ref_get(v___x_2905_);
v_env_2909_ = lean_ctor_get(v___x_2908_, 0);
lean_inc_ref(v_env_2909_);
lean_dec(v___x_2908_);
v___x_2910_ = l_Lean_diagnostics;
v___x_2911_ = l_Lean_Option_get___at___00Lean_Elab_addMacroStack___at___00Lean_throwError___at___00Lean_throwErrorAt___at___00Lean_throwUnknownIdentifierAt___at___00Lean_throwUnknownConstantAt___at___00Lean_throwUnknownConstant___at___00Lean_getConstVal___at___00Lean_mkConstWithLevelParams___at___00Lean_Elab_addConstInfo___at___00Lean_Elab_PostprocessTraces_elabStoreTraceAs_spec__3_spec__5_spec__6_spec__9_spec__12_spec__14_spec__16_spec__18_spec__20_spec__21(v___x_2871_, v___x_2910_);
v___x_2967_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_2909_);
lean_dec_ref(v_env_2909_);
if (v___x_2967_ == 0)
{
if (v___x_2911_ == 0)
{
lean_inc(v___x_2905_);
lean_inc(v___x_2868_);
v_fileName_2913_ = v___x_2872_;
v_fileMap_2914_ = v___x_2873_;
v_currRecDepth_2915_ = v___x_2866_;
v_ref_2916_ = v___x_2874_;
v_currNamespace_2917_ = v___x_2868_;
v_openDecls_2918_ = v___x_2875_;
v_initHeartbeats_2919_ = v___x_2894_;
v_maxHeartbeats_2920_ = v___x_2876_;
v_quotContext_2921_ = v___x_2868_;
v_currMacroScope_2922_ = v___x_2867_;
v_cancelTk_x3f_2923_ = v___x_2877_;
v_suppressElabErrors_2924_ = v___x_2878_;
v_inheritedTraceOptions_2925_ = v___x_2907_;
v___y_2926_ = v___x_2905_;
goto v___jp_2912_;
}
else
{
v___y_2947_ = v___x_2967_;
goto v___jp_2946_;
}
}
else
{
v___y_2947_ = v___x_2911_;
goto v___jp_2946_;
}
v___jp_2882_:
{
lean_object* v___x_2883_; lean_object* v___x_2884_; 
v___x_2883_ = lean_box(0);
v___x_2884_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2884_, 0, v___x_2883_);
return v___x_2884_;
}
v___jp_2912_:
{
lean_object* v___x_2927_; lean_object* v___x_2928_; lean_object* v___x_2929_; lean_object* v___x_2930_; 
v___x_2927_ = l_Lean_maxRecDepth;
v___x_2928_ = l_Lean_Option_get___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0(v___x_2871_, v___x_2927_);
v___x_2929_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_2929_, 0, v_fileName_2913_);
lean_ctor_set(v___x_2929_, 1, v_fileMap_2914_);
lean_ctor_set(v___x_2929_, 2, v___x_2871_);
lean_ctor_set(v___x_2929_, 3, v_currRecDepth_2915_);
lean_ctor_set(v___x_2929_, 4, v___x_2928_);
lean_ctor_set(v___x_2929_, 5, v_ref_2916_);
lean_ctor_set(v___x_2929_, 6, v_currNamespace_2917_);
lean_ctor_set(v___x_2929_, 7, v_openDecls_2918_);
lean_ctor_set(v___x_2929_, 8, v_initHeartbeats_2919_);
lean_ctor_set(v___x_2929_, 9, v_maxHeartbeats_2920_);
lean_ctor_set(v___x_2929_, 10, v_quotContext_2921_);
lean_ctor_set(v___x_2929_, 11, v_currMacroScope_2922_);
lean_ctor_set(v___x_2929_, 12, v_cancelTk_x3f_2923_);
lean_ctor_set(v___x_2929_, 13, v_inheritedTraceOptions_2925_);
lean_ctor_set_uint8(v___x_2929_, sizeof(void*)*14, v___x_2911_);
lean_ctor_set_uint8(v___x_2929_, sizeof(void*)*14 + 1, v_suppressElabErrors_2924_);
v___x_2930_ = lean_apply_3(v_x_2880_, v___x_2929_, v___y_2926_, lean_box(0));
if (lean_obj_tag(v___x_2930_) == 0)
{
lean_object* v_a_2931_; lean_object* v___x_2933_; uint8_t v_isShared_2934_; uint8_t v_isSharedCheck_2940_; 
v_a_2931_ = lean_ctor_get(v___x_2930_, 0);
v_isSharedCheck_2940_ = !lean_is_exclusive(v___x_2930_);
if (v_isSharedCheck_2940_ == 0)
{
v___x_2933_ = v___x_2930_;
v_isShared_2934_ = v_isSharedCheck_2940_;
goto v_resetjp_2932_;
}
else
{
lean_inc(v_a_2931_);
lean_dec(v___x_2930_);
v___x_2933_ = lean_box(0);
v_isShared_2934_ = v_isSharedCheck_2940_;
goto v_resetjp_2932_;
}
v_resetjp_2932_:
{
lean_object* v___x_2935_; lean_object* v___x_2936_; lean_object* v___x_2938_; 
v___x_2935_ = lean_st_ref_get(v___x_2905_);
lean_dec(v___x_2905_);
lean_dec(v___x_2935_);
v___x_2936_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_2936_, 0, v_a_2931_);
if (v_isShared_2934_ == 0)
{
lean_ctor_set(v___x_2933_, 0, v___x_2936_);
v___x_2938_ = v___x_2933_;
goto v_reusejp_2937_;
}
else
{
lean_object* v_reuseFailAlloc_2939_; 
v_reuseFailAlloc_2939_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2939_, 0, v___x_2936_);
v___x_2938_ = v_reuseFailAlloc_2939_;
goto v_reusejp_2937_;
}
v_reusejp_2937_:
{
return v___x_2938_;
}
}
}
else
{
lean_object* v_a_2941_; 
lean_dec(v___x_2905_);
v_a_2941_ = lean_ctor_get(v___x_2930_, 0);
lean_inc(v_a_2941_);
lean_dec_ref_known(v___x_2930_, 1);
if (lean_obj_tag(v_a_2941_) == 0)
{
lean_object* v_msg_2942_; lean_object* v___x_2943_; 
v_msg_2942_ = lean_ctor_get(v_a_2941_, 1);
lean_inc_ref(v_msg_2942_);
lean_dec_ref_known(v_a_2941_, 2);
v___x_2943_ = l_Lean_MessageData_toString(v_msg_2942_);
lean_dec_ref(v___x_2943_);
goto v___jp_2882_;
}
else
{
lean_object* v_id_2944_; lean_object* v___x_2945_; 
v_id_2944_ = lean_ctor_get(v_a_2941_, 0);
lean_inc(v_id_2944_);
lean_dec_ref_known(v_a_2941_, 2);
v___x_2945_ = l_Lean_InternalExceptionId_getName(v_id_2944_);
lean_dec(v_id_2944_);
lean_dec_ref(v___x_2945_);
goto v___jp_2882_;
}
}
}
v___jp_2946_:
{
if (v___y_2947_ == 0)
{
lean_object* v___x_2948_; lean_object* v_env_2949_; lean_object* v_nextMacroScope_2950_; lean_object* v_ngen_2951_; lean_object* v_auxDeclNGen_2952_; lean_object* v_traceState_2953_; lean_object* v_messages_2954_; lean_object* v_infoState_2955_; lean_object* v_snapshotTasks_2956_; lean_object* v___x_2958_; uint8_t v_isShared_2959_; uint8_t v_isSharedCheck_2965_; 
v___x_2948_ = lean_st_ref_take(v___x_2905_);
v_env_2949_ = lean_ctor_get(v___x_2948_, 0);
v_nextMacroScope_2950_ = lean_ctor_get(v___x_2948_, 1);
v_ngen_2951_ = lean_ctor_get(v___x_2948_, 2);
v_auxDeclNGen_2952_ = lean_ctor_get(v___x_2948_, 3);
v_traceState_2953_ = lean_ctor_get(v___x_2948_, 4);
v_messages_2954_ = lean_ctor_get(v___x_2948_, 6);
v_infoState_2955_ = lean_ctor_get(v___x_2948_, 7);
v_snapshotTasks_2956_ = lean_ctor_get(v___x_2948_, 8);
v_isSharedCheck_2965_ = !lean_is_exclusive(v___x_2948_);
if (v_isSharedCheck_2965_ == 0)
{
lean_object* v_unused_2966_; 
v_unused_2966_ = lean_ctor_get(v___x_2948_, 5);
lean_dec(v_unused_2966_);
v___x_2958_ = v___x_2948_;
v_isShared_2959_ = v_isSharedCheck_2965_;
goto v_resetjp_2957_;
}
else
{
lean_inc(v_snapshotTasks_2956_);
lean_inc(v_infoState_2955_);
lean_inc(v_messages_2954_);
lean_inc(v_traceState_2953_);
lean_inc(v_auxDeclNGen_2952_);
lean_inc(v_ngen_2951_);
lean_inc(v_nextMacroScope_2950_);
lean_inc(v_env_2949_);
lean_dec(v___x_2948_);
v___x_2958_ = lean_box(0);
v_isShared_2959_ = v_isSharedCheck_2965_;
goto v_resetjp_2957_;
}
v_resetjp_2957_:
{
lean_object* v___x_2960_; lean_object* v___x_2962_; 
v___x_2960_ = l_Lean_Kernel_enableDiag(v_env_2949_, v___x_2911_);
if (v_isShared_2959_ == 0)
{
lean_ctor_set(v___x_2958_, 5, v___x_2891_);
lean_ctor_set(v___x_2958_, 0, v___x_2960_);
v___x_2962_ = v___x_2958_;
goto v_reusejp_2961_;
}
else
{
lean_object* v_reuseFailAlloc_2964_; 
v_reuseFailAlloc_2964_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_2964_, 0, v___x_2960_);
lean_ctor_set(v_reuseFailAlloc_2964_, 1, v_nextMacroScope_2950_);
lean_ctor_set(v_reuseFailAlloc_2964_, 2, v_ngen_2951_);
lean_ctor_set(v_reuseFailAlloc_2964_, 3, v_auxDeclNGen_2952_);
lean_ctor_set(v_reuseFailAlloc_2964_, 4, v_traceState_2953_);
lean_ctor_set(v_reuseFailAlloc_2964_, 5, v___x_2891_);
lean_ctor_set(v_reuseFailAlloc_2964_, 6, v_messages_2954_);
lean_ctor_set(v_reuseFailAlloc_2964_, 7, v_infoState_2955_);
lean_ctor_set(v_reuseFailAlloc_2964_, 8, v_snapshotTasks_2956_);
v___x_2962_ = v_reuseFailAlloc_2964_;
goto v_reusejp_2961_;
}
v_reusejp_2961_:
{
lean_object* v___x_2963_; 
v___x_2963_ = lean_st_ref_set(v___x_2905_, v___x_2962_);
lean_inc(v___x_2905_);
lean_inc(v___x_2868_);
v_fileName_2913_ = v___x_2872_;
v_fileMap_2914_ = v___x_2873_;
v_currRecDepth_2915_ = v___x_2866_;
v_ref_2916_ = v___x_2874_;
v_currNamespace_2917_ = v___x_2868_;
v_openDecls_2918_ = v___x_2875_;
v_initHeartbeats_2919_ = v___x_2894_;
v_maxHeartbeats_2920_ = v___x_2876_;
v_quotContext_2921_ = v___x_2868_;
v_currMacroScope_2922_ = v___x_2867_;
v_cancelTk_x3f_2923_ = v___x_2877_;
v_suppressElabErrors_2924_ = v___x_2878_;
v_inheritedTraceOptions_2925_ = v___x_2907_;
v___y_2926_ = v___x_2905_;
goto v___jp_2912_;
}
}
}
else
{
lean_inc(v___x_2905_);
lean_inc(v___x_2868_);
v_fileName_2913_ = v___x_2872_;
v_fileMap_2914_ = v___x_2873_;
v_currRecDepth_2915_ = v___x_2866_;
v_ref_2916_ = v___x_2874_;
v_currNamespace_2917_ = v___x_2868_;
v_openDecls_2918_ = v___x_2875_;
v_initHeartbeats_2919_ = v___x_2894_;
v_maxHeartbeats_2920_ = v___x_2876_;
v_quotContext_2921_ = v___x_2868_;
v_currMacroScope_2922_ = v___x_2867_;
v_cancelTk_x3f_2923_ = v___x_2877_;
v_suppressElabErrors_2924_ = v___x_2878_;
v_inheritedTraceOptions_2925_ = v___x_2907_;
v___y_2926_ = v___x_2905_;
goto v___jp_2912_;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1___boxed(lean_object* v___x_2968_, lean_object* v___x_2969_, lean_object* v___x_2970_, lean_object* v___x_2971_, lean_object* v_a_2972_, lean_object* v___x_2973_, lean_object* v___x_2974_, lean_object* v___x_2975_, lean_object* v___x_2976_, lean_object* v___x_2977_, lean_object* v___x_2978_, lean_object* v___x_2979_, lean_object* v___x_2980_, lean_object* v_00_u03b1_2981_, lean_object* v_x_2982_, lean_object* v___y_2983_){
_start:
{
uint8_t v___x_75501__boxed_2984_; uint8_t v___x_75510__boxed_2985_; lean_object* v_res_2986_; 
v___x_75501__boxed_2984_ = lean_unbox(v___x_2971_);
v___x_75510__boxed_2985_ = lean_unbox(v___x_2980_);
v_res_2986_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_2968_, v___x_2969_, v___x_2970_, v___x_75501__boxed_2984_, v_a_2972_, v___x_2973_, v___x_2974_, v___x_2975_, v___x_2976_, v___x_2977_, v___x_2978_, v___x_2979_, v___x_75510__boxed_2985_, v_00_u03b1_2981_, v_x_2982_);
return v_res_2986_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__28(void){
_start:
{
lean_object* v___x_3023_; lean_object* v___x_3024_; 
v___x_3023_ = lean_unsigned_to_nat(0u);
v___x_3024_ = l_Lean_JsonNumber_fromNat(v___x_3023_);
return v___x_3024_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29(void){
_start:
{
lean_object* v___x_3025_; lean_object* v___x_3026_; 
v___x_3025_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__28, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__28_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__28);
v___x_3026_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3026_, 0, v___x_3025_);
return v___x_3026_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23(lean_object* v_a_3043_, lean_object* v_nshards_3044_, lean_object* v_shard_3045_, lean_object* v___x_3046_, lean_object* v_a_3047_, lean_object* v___x_3048_, lean_object* v___x_3049_, lean_object* v_a_3050_, lean_object* v___x_3051_, lean_object* v_a_3052_, lean_object* v_as_3053_, size_t v_sz_3054_, size_t v_i_3055_, lean_object* v_b_3056_){
_start:
{
lean_object* v_a_3059_; uint8_t v___x_3063_; 
v___x_3063_ = lean_usize_dec_lt(v_i_3055_, v_sz_3054_);
if (v___x_3063_ == 0)
{
lean_object* v___x_3064_; 
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v___x_3064_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_3064_, 0, v_b_3056_);
return v___x_3064_;
}
else
{
lean_object* v_a_3065_; lean_object* v_snd_3066_; lean_object* v_fst_3067_; lean_object* v_snd_3068_; lean_object* v___x_3070_; uint8_t v_isShared_3071_; uint8_t v_isSharedCheck_3725_; 
v_a_3065_ = lean_array_uget(v_as_3053_, v_i_3055_);
v_snd_3066_ = lean_ctor_get(v_b_3056_, 1);
lean_inc(v_snd_3066_);
v_fst_3067_ = lean_ctor_get(v_a_3065_, 0);
v_snd_3068_ = lean_ctor_get(v_a_3065_, 1);
v_isSharedCheck_3725_ = !lean_is_exclusive(v_a_3065_);
if (v_isSharedCheck_3725_ == 0)
{
v___x_3070_ = v_a_3065_;
v_isShared_3071_ = v_isSharedCheck_3725_;
goto v_resetjp_3069_;
}
else
{
lean_inc(v_snd_3068_);
lean_inc(v_fst_3067_);
lean_dec(v_a_3065_);
v___x_3070_ = lean_box(0);
v_isShared_3071_ = v_isSharedCheck_3725_;
goto v_resetjp_3069_;
}
v_resetjp_3069_:
{
lean_object* v_fst_3072_; lean_object* v___x_3074_; uint8_t v_isShared_3075_; uint8_t v_isSharedCheck_3723_; 
v_fst_3072_ = lean_ctor_get(v_b_3056_, 0);
v_isSharedCheck_3723_ = !lean_is_exclusive(v_b_3056_);
if (v_isSharedCheck_3723_ == 0)
{
lean_object* v_unused_3724_; 
v_unused_3724_ = lean_ctor_get(v_b_3056_, 1);
lean_dec(v_unused_3724_);
v___x_3074_ = v_b_3056_;
v_isShared_3075_ = v_isSharedCheck_3723_;
goto v_resetjp_3073_;
}
else
{
lean_inc(v_fst_3072_);
lean_dec(v_b_3056_);
v___x_3074_ = lean_box(0);
v_isShared_3075_ = v_isSharedCheck_3723_;
goto v_resetjp_3073_;
}
v_resetjp_3073_:
{
lean_object* v_fst_3076_; lean_object* v_snd_3077_; lean_object* v___x_3079_; uint8_t v_isShared_3080_; uint8_t v_isSharedCheck_3722_; 
v_fst_3076_ = lean_ctor_get(v_snd_3066_, 0);
v_snd_3077_ = lean_ctor_get(v_snd_3066_, 1);
v_isSharedCheck_3722_ = !lean_is_exclusive(v_snd_3066_);
if (v_isSharedCheck_3722_ == 0)
{
v___x_3079_ = v_snd_3066_;
v_isShared_3080_ = v_isSharedCheck_3722_;
goto v_resetjp_3078_;
}
else
{
lean_inc(v_snd_3077_);
lean_inc(v_fst_3076_);
lean_dec(v_snd_3066_);
v___x_3079_ = lean_box(0);
v_isShared_3080_ = v_isSharedCheck_3722_;
goto v_resetjp_3078_;
}
v_resetjp_3078_:
{
lean_object* v___x_3081_; lean_object* v___x_3082_; uint8_t v___x_3083_; 
v___x_3081_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_a_3043_, v_fst_3067_);
v___x_3082_ = lean_box(0);
v___x_3083_ = l_NsExport_instBEqCls_beq(v___x_3081_, v___x_3082_);
lean_dec(v___x_3081_);
if (v___x_3083_ == 0)
{
lean_object* v___x_3085_; 
lean_del_object(v___x_3070_);
lean_dec(v_snd_3068_);
lean_dec(v_fst_3067_);
if (v_isShared_3080_ == 0)
{
v___x_3085_ = v___x_3079_;
goto v_reusejp_3084_;
}
else
{
lean_object* v_reuseFailAlloc_3089_; 
v_reuseFailAlloc_3089_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3089_, 0, v_fst_3076_);
lean_ctor_set(v_reuseFailAlloc_3089_, 1, v_snd_3077_);
v___x_3085_ = v_reuseFailAlloc_3089_;
goto v_reusejp_3084_;
}
v_reusejp_3084_:
{
lean_object* v___x_3087_; 
if (v_isShared_3075_ == 0)
{
lean_ctor_set(v___x_3074_, 1, v___x_3085_);
v___x_3087_ = v___x_3074_;
goto v_reusejp_3086_;
}
else
{
lean_object* v_reuseFailAlloc_3088_; 
v_reuseFailAlloc_3088_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3088_, 0, v_fst_3072_);
lean_ctor_set(v_reuseFailAlloc_3088_, 1, v___x_3085_);
v___x_3087_ = v_reuseFailAlloc_3088_;
goto v_reusejp_3086_;
}
v_reusejp_3086_:
{
v_a_3059_ = v___x_3087_;
goto v___jp_3058_;
}
}
}
else
{
lean_object* v___x_3090_; lean_object* v___x_3091_; lean_object* v___x_3092_; uint8_t v___x_3093_; 
v___x_3090_ = lean_unsigned_to_nat(1u);
v___x_3091_ = lean_nat_add(v_fst_3072_, v___x_3090_);
lean_dec(v_fst_3072_);
v___x_3092_ = lean_nat_mod(v___x_3091_, v_nshards_3044_);
v___x_3093_ = lean_nat_dec_eq(v___x_3092_, v_shard_3045_);
if (v___x_3093_ == 0)
{
lean_object* v___x_3095_; 
lean_dec(v___x_3092_);
lean_del_object(v___x_3070_);
lean_dec(v_snd_3068_);
lean_dec(v_fst_3067_);
if (v_isShared_3080_ == 0)
{
v___x_3095_ = v___x_3079_;
goto v_reusejp_3094_;
}
else
{
lean_object* v_reuseFailAlloc_3099_; 
v_reuseFailAlloc_3099_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3099_, 0, v_fst_3076_);
lean_ctor_set(v_reuseFailAlloc_3099_, 1, v_snd_3077_);
v___x_3095_ = v_reuseFailAlloc_3099_;
goto v_reusejp_3094_;
}
v_reusejp_3094_:
{
lean_object* v___x_3097_; 
if (v_isShared_3075_ == 0)
{
lean_ctor_set(v___x_3074_, 1, v___x_3095_);
lean_ctor_set(v___x_3074_, 0, v___x_3091_);
v___x_3097_ = v___x_3074_;
goto v_reusejp_3096_;
}
else
{
lean_object* v_reuseFailAlloc_3098_; 
v_reuseFailAlloc_3098_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3098_, 0, v___x_3091_);
lean_ctor_set(v_reuseFailAlloc_3098_, 1, v___x_3095_);
v___x_3097_ = v_reuseFailAlloc_3098_;
goto v_reusejp_3096_;
}
v_reusejp_3096_:
{
v_a_3059_ = v___x_3097_;
goto v___jp_3058_;
}
}
}
else
{
lean_object* v___x_3100_; lean_object* v___x_3101_; lean_object* v___x_3102_; lean_object* v_snd_3103_; lean_object* v_fst_3104_; lean_object* v___x_3106_; uint8_t v_isShared_3107_; uint8_t v_isSharedCheck_3721_; 
v___x_3100_ = l_Lean_ConstantInfo_levelParams(v_snd_3068_);
v___x_3101_ = l_Lean_ConstantInfo_type(v_snd_3068_);
lean_inc_ref(v___x_3101_);
v___x_3102_ = l_NsExport_sizes(v___x_3100_, v___x_3101_);
v_snd_3103_ = lean_ctor_get(v___x_3102_, 1);
v_fst_3104_ = lean_ctor_get(v___x_3102_, 0);
v_isSharedCheck_3721_ = !lean_is_exclusive(v___x_3102_);
if (v_isSharedCheck_3721_ == 0)
{
v___x_3106_ = v___x_3102_;
v_isShared_3107_ = v_isSharedCheck_3721_;
goto v_resetjp_3105_;
}
else
{
lean_inc(v_snd_3103_);
lean_inc(v_fst_3104_);
lean_dec(v___x_3102_);
v___x_3106_ = lean_box(0);
v_isShared_3107_ = v_isSharedCheck_3721_;
goto v_resetjp_3105_;
}
v_resetjp_3105_:
{
lean_object* v_fst_3108_; lean_object* v_snd_3109_; lean_object* v___x_3111_; uint8_t v_isShared_3112_; uint8_t v_isSharedCheck_3720_; 
v_fst_3108_ = lean_ctor_get(v_snd_3103_, 0);
v_snd_3109_ = lean_ctor_get(v_snd_3103_, 1);
v_isSharedCheck_3720_ = !lean_is_exclusive(v_snd_3103_);
if (v_isSharedCheck_3720_ == 0)
{
v___x_3111_ = v_snd_3103_;
v_isShared_3112_ = v_isSharedCheck_3720_;
goto v_resetjp_3110_;
}
else
{
lean_inc(v_snd_3109_);
lean_inc(v_fst_3108_);
lean_dec(v_snd_3103_);
v___x_3111_ = lean_box(0);
v_isShared_3112_ = v_isSharedCheck_3720_;
goto v_resetjp_3110_;
}
v_resetjp_3110_:
{
lean_object* v___x_3113_; lean_object* v___y_3115_; lean_object* v___y_3116_; lean_object* v_fields_3117_; lean_object* v___x_3165_; lean_object* v___x_3166_; lean_object* v___x_3167_; lean_object* v___x_3169_; 
v___x_3113_ = lean_unsigned_to_nat(0u);
lean_inc_ref(v___x_3101_);
v___x_3165_ = l_Lean_Expr_getUsedConstants(v___x_3101_);
v___x_3166_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___closed__0));
v___x_3167_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(v___x_3046_, v_fst_3067_, v___x_3166_);
if (v_isShared_3080_ == 0)
{
lean_ctor_set(v___x_3079_, 1, v_fst_3108_);
lean_ctor_set(v___x_3079_, 0, v_fst_3104_);
v___x_3169_ = v___x_3079_;
goto v_reusejp_3168_;
}
else
{
lean_object* v_reuseFailAlloc_3719_; 
v_reuseFailAlloc_3719_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3719_, 0, v_fst_3104_);
lean_ctor_set(v_reuseFailAlloc_3719_, 1, v_fst_3108_);
v___x_3169_ = v_reuseFailAlloc_3719_;
goto v_reusejp_3168_;
}
v___jp_3114_:
{
lean_object* v___x_3118_; lean_object* v___x_3119_; lean_object* v___x_3120_; 
v___x_3118_ = l_Lean_Json_mkObj(v_fields_3117_);
lean_dec(v_fields_3117_);
v___x_3119_ = l_Lean_Json_compress(v___x_3118_);
v___x_3120_ = l_IO_FS_Handle_putStrLn(v_a_3050_, v___x_3119_);
if (lean_obj_tag(v___x_3120_) == 0)
{
lean_object* v___x_3121_; lean_object* v___x_3122_; uint8_t v___x_3123_; 
lean_dec_ref_known(v___x_3120_, 1);
v___x_3121_ = lean_nat_add(v_snd_3077_, v___x_3090_);
lean_dec(v_snd_3077_);
v___x_3122_ = lean_nat_mod(v___x_3121_, v___y_3115_);
lean_dec(v___y_3115_);
v___x_3123_ = lean_nat_dec_eq(v___x_3122_, v___x_3113_);
lean_dec(v___x_3122_);
if (v___x_3123_ == 0)
{
lean_object* v___x_3125_; 
if (v_isShared_3112_ == 0)
{
lean_ctor_set(v___x_3111_, 1, v___x_3121_);
lean_ctor_set(v___x_3111_, 0, v___y_3116_);
v___x_3125_ = v___x_3111_;
goto v_reusejp_3124_;
}
else
{
lean_object* v_reuseFailAlloc_3129_; 
v_reuseFailAlloc_3129_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3129_, 0, v___y_3116_);
lean_ctor_set(v_reuseFailAlloc_3129_, 1, v___x_3121_);
v___x_3125_ = v_reuseFailAlloc_3129_;
goto v_reusejp_3124_;
}
v_reusejp_3124_:
{
lean_object* v___x_3127_; 
if (v_isShared_3107_ == 0)
{
lean_ctor_set(v___x_3106_, 1, v___x_3125_);
lean_ctor_set(v___x_3106_, 0, v___x_3091_);
v___x_3127_ = v___x_3106_;
goto v_reusejp_3126_;
}
else
{
lean_object* v_reuseFailAlloc_3128_; 
v_reuseFailAlloc_3128_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3128_, 0, v___x_3091_);
lean_ctor_set(v_reuseFailAlloc_3128_, 1, v___x_3125_);
v___x_3127_ = v_reuseFailAlloc_3128_;
goto v_reusejp_3126_;
}
v_reusejp_3126_:
{
v_a_3059_ = v___x_3127_;
goto v___jp_3058_;
}
}
}
else
{
lean_object* v___x_3130_; lean_object* v___x_3131_; lean_object* v___x_3132_; lean_object* v___x_3133_; lean_object* v___x_3134_; lean_object* v___x_3135_; lean_object* v___x_3136_; lean_object* v___x_3137_; lean_object* v___x_3138_; lean_object* v___x_3139_; lean_object* v___x_3140_; lean_object* v___x_3141_; lean_object* v___x_3142_; 
v___x_3130_ = lean_io_mono_ms_now();
v___x_3131_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__0));
lean_inc_ref(v___x_3051_);
v___x_3132_ = lean_string_append(v___x_3051_, v___x_3131_);
lean_inc(v___x_3121_);
v___x_3133_ = l_Nat_reprFast(v___x_3121_);
v___x_3134_ = lean_string_append(v___x_3132_, v___x_3133_);
lean_dec_ref(v___x_3133_);
v___x_3135_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__1));
v___x_3136_ = lean_string_append(v___x_3134_, v___x_3135_);
v___x_3137_ = lean_nat_sub(v___x_3130_, v_a_3052_);
lean_dec(v___x_3130_);
v___x_3138_ = l_Nat_reprFast(v___x_3137_);
v___x_3139_ = lean_string_append(v___x_3136_, v___x_3138_);
lean_dec_ref(v___x_3138_);
v___x_3140_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__2));
v___x_3141_ = lean_string_append(v___x_3139_, v___x_3140_);
v___x_3142_ = l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(v___x_3141_);
if (lean_obj_tag(v___x_3142_) == 0)
{
lean_object* v___x_3144_; 
lean_dec_ref_known(v___x_3142_, 1);
if (v_isShared_3112_ == 0)
{
lean_ctor_set(v___x_3111_, 1, v___x_3121_);
lean_ctor_set(v___x_3111_, 0, v___y_3116_);
v___x_3144_ = v___x_3111_;
goto v_reusejp_3143_;
}
else
{
lean_object* v_reuseFailAlloc_3148_; 
v_reuseFailAlloc_3148_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3148_, 0, v___y_3116_);
lean_ctor_set(v_reuseFailAlloc_3148_, 1, v___x_3121_);
v___x_3144_ = v_reuseFailAlloc_3148_;
goto v_reusejp_3143_;
}
v_reusejp_3143_:
{
lean_object* v___x_3146_; 
if (v_isShared_3107_ == 0)
{
lean_ctor_set(v___x_3106_, 1, v___x_3144_);
lean_ctor_set(v___x_3106_, 0, v___x_3091_);
v___x_3146_ = v___x_3106_;
goto v_reusejp_3145_;
}
else
{
lean_object* v_reuseFailAlloc_3147_; 
v_reuseFailAlloc_3147_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3147_, 0, v___x_3091_);
lean_ctor_set(v_reuseFailAlloc_3147_, 1, v___x_3144_);
v___x_3146_ = v_reuseFailAlloc_3147_;
goto v_reusejp_3145_;
}
v_reusejp_3145_:
{
v_a_3059_ = v___x_3146_;
goto v___jp_3058_;
}
}
}
else
{
lean_object* v_a_3149_; lean_object* v___x_3151_; uint8_t v_isShared_3152_; uint8_t v_isSharedCheck_3156_; 
lean_dec(v___x_3121_);
lean_dec(v___y_3116_);
lean_del_object(v___x_3111_);
lean_del_object(v___x_3106_);
lean_dec(v___x_3091_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3149_ = lean_ctor_get(v___x_3142_, 0);
v_isSharedCheck_3156_ = !lean_is_exclusive(v___x_3142_);
if (v_isSharedCheck_3156_ == 0)
{
v___x_3151_ = v___x_3142_;
v_isShared_3152_ = v_isSharedCheck_3156_;
goto v_resetjp_3150_;
}
else
{
lean_inc(v_a_3149_);
lean_dec(v___x_3142_);
v___x_3151_ = lean_box(0);
v_isShared_3152_ = v_isSharedCheck_3156_;
goto v_resetjp_3150_;
}
v_resetjp_3150_:
{
lean_object* v___x_3154_; 
if (v_isShared_3152_ == 0)
{
v___x_3154_ = v___x_3151_;
goto v_reusejp_3153_;
}
else
{
lean_object* v_reuseFailAlloc_3155_; 
v_reuseFailAlloc_3155_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3155_, 0, v_a_3149_);
v___x_3154_ = v_reuseFailAlloc_3155_;
goto v_reusejp_3153_;
}
v_reusejp_3153_:
{
return v___x_3154_;
}
}
}
}
}
else
{
lean_object* v_a_3157_; lean_object* v___x_3159_; uint8_t v_isShared_3160_; uint8_t v_isSharedCheck_3164_; 
lean_dec(v___y_3116_);
lean_dec(v___y_3115_);
lean_del_object(v___x_3111_);
lean_del_object(v___x_3106_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3157_ = lean_ctor_get(v___x_3120_, 0);
v_isSharedCheck_3164_ = !lean_is_exclusive(v___x_3120_);
if (v_isSharedCheck_3164_ == 0)
{
v___x_3159_ = v___x_3120_;
v_isShared_3160_ = v_isSharedCheck_3164_;
goto v_resetjp_3158_;
}
else
{
lean_inc(v_a_3157_);
lean_dec(v___x_3120_);
v___x_3159_ = lean_box(0);
v_isShared_3160_ = v_isSharedCheck_3164_;
goto v_resetjp_3158_;
}
v_resetjp_3158_:
{
lean_object* v___x_3162_; 
if (v_isShared_3160_ == 0)
{
v___x_3162_ = v___x_3159_;
goto v_reusejp_3161_;
}
else
{
lean_object* v_reuseFailAlloc_3163_; 
v_reuseFailAlloc_3163_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3163_, 0, v_a_3157_);
v___x_3162_ = v_reuseFailAlloc_3163_;
goto v_reusejp_3161_;
}
v_reusejp_3161_:
{
return v___x_3162_;
}
}
}
}
v_reusejp_3168_:
{
lean_object* v___x_3171_; 
if (v_isShared_3075_ == 0)
{
lean_ctor_set(v___x_3074_, 1, v___x_3169_);
lean_ctor_set(v___x_3074_, 0, v___x_3165_);
v___x_3171_ = v___x_3074_;
goto v_reusejp_3170_;
}
else
{
lean_object* v_reuseFailAlloc_3718_; 
v_reuseFailAlloc_3718_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3718_, 0, v___x_3165_);
lean_ctor_set(v_reuseFailAlloc_3718_, 1, v___x_3169_);
v___x_3171_ = v_reuseFailAlloc_3718_;
goto v_reusejp_3170_;
}
v_reusejp_3170_:
{
size_t v_sz_3172_; size_t v___x_3173_; lean_object* v___x_3174_; 
v_sz_3172_ = lean_array_size(v___x_3167_);
v___x_3173_ = ((size_t)0ULL);
lean_inc_ref(v_a_3047_);
v___x_3174_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__14(v_a_3047_, v___x_3167_, v_sz_3172_, v___x_3173_, v___x_3171_);
if (lean_obj_tag(v___x_3174_) == 0)
{
lean_object* v_a_3175_; lean_object* v_snd_3176_; lean_object* v_fst_3177_; lean_object* v___x_3179_; uint8_t v_isShared_3180_; uint8_t v_isSharedCheck_3709_; 
v_a_3175_ = lean_ctor_get(v___x_3174_, 0);
lean_inc(v_a_3175_);
lean_dec_ref_known(v___x_3174_, 1);
v_snd_3176_ = lean_ctor_get(v_a_3175_, 1);
v_fst_3177_ = lean_ctor_get(v_a_3175_, 0);
v_isSharedCheck_3709_ = !lean_is_exclusive(v_a_3175_);
if (v_isSharedCheck_3709_ == 0)
{
v___x_3179_ = v_a_3175_;
v_isShared_3180_ = v_isSharedCheck_3709_;
goto v_resetjp_3178_;
}
else
{
lean_inc(v_snd_3176_);
lean_inc(v_fst_3177_);
lean_dec(v_a_3175_);
v___x_3179_ = lean_box(0);
v_isShared_3180_ = v_isSharedCheck_3709_;
goto v_resetjp_3178_;
}
v_resetjp_3178_:
{
lean_object* v_fst_3181_; lean_object* v_snd_3182_; lean_object* v___x_3184_; uint8_t v_isShared_3185_; uint8_t v_isSharedCheck_3708_; 
v_fst_3181_ = lean_ctor_get(v_snd_3176_, 0);
v_snd_3182_ = lean_ctor_get(v_snd_3176_, 1);
v_isSharedCheck_3708_ = !lean_is_exclusive(v_snd_3176_);
if (v_isSharedCheck_3708_ == 0)
{
v___x_3184_ = v_snd_3176_;
v_isShared_3185_ = v_isSharedCheck_3708_;
goto v_resetjp_3183_;
}
else
{
lean_inc(v_snd_3182_);
lean_inc(v_fst_3181_);
lean_dec(v_snd_3176_);
v___x_3184_ = lean_box(0);
v_isShared_3185_ = v_isSharedCheck_3708_;
goto v_resetjp_3183_;
}
v_resetjp_3183_:
{
lean_object* v___y_3187_; lean_object* v___y_3188_; lean_object* v___y_3189_; lean_object* v___y_3190_; lean_object* v___y_3191_; lean_object* v___y_3192_; lean_object* v___y_3193_; uint8_t v___y_3194_; lean_object* v___y_3195_; lean_object* v___y_3196_; lean_object* v___y_3197_; lean_object* v___y_3198_; lean_object* v___y_3199_; lean_object* v___y_3200_; lean_object* v___y_3201_; lean_object* v___y_3202_; lean_object* v___y_3203_; lean_object* v___y_3204_; lean_object* v___y_3205_; lean_object* v___y_3206_; lean_object* v___y_3207_; lean_object* v___y_3208_; lean_object* v___y_3209_; lean_object* v___y_3210_; lean_object* v___y_3211_; lean_object* v___y_3212_; lean_object* v___y_3213_; lean_object* v___y_3334_; lean_object* v___y_3335_; lean_object* v___y_3336_; uint8_t v___y_3337_; lean_object* v___y_3338_; lean_object* v___y_3339_; lean_object* v___y_3340_; lean_object* v___y_3341_; lean_object* v___y_3342_; lean_object* v___y_3343_; lean_object* v___y_3344_; lean_object* v___y_3345_; lean_object* v___y_3346_; lean_object* v___y_3347_; lean_object* v___y_3348_; lean_object* v___y_3349_; lean_object* v___y_3350_; lean_object* v___y_3351_; lean_object* v___y_3352_; lean_object* v___y_3353_; lean_object* v___y_3354_; lean_object* v___y_3355_; uint8_t v___y_3356_; lean_object* v___y_3357_; uint8_t v___y_3358_; uint8_t v___x_3393_; lean_object* v___y_3395_; lean_object* v___y_3396_; lean_object* v___y_3397_; lean_object* v___y_3398_; lean_object* v___y_3399_; lean_object* v___y_3400_; lean_object* v___y_3401_; lean_object* v___y_3402_; lean_object* v___y_3403_; uint8_t v___y_3404_; lean_object* v___y_3405_; lean_object* v___y_3406_; lean_object* v___y_3407_; lean_object* v___y_3408_; lean_object* v___y_3409_; uint8_t v___y_3410_; lean_object* v___y_3411_; lean_object* v_a_3412_; lean_object* v___y_3444_; lean_object* v___y_3445_; lean_object* v___y_3446_; lean_object* v___y_3447_; lean_object* v___y_3448_; lean_object* v___y_3449_; lean_object* v___y_3450_; lean_object* v___y_3451_; lean_object* v___y_3452_; uint8_t v___y_3453_; lean_object* v___y_3454_; lean_object* v___y_3455_; lean_object* v___y_3456_; lean_object* v___y_3457_; lean_object* v___y_3458_; uint8_t v___y_3459_; lean_object* v___y_3460_; lean_object* v___x_3462_; lean_object* v___x_3463_; lean_object* v___x_3464_; lean_object* v___x_3465_; lean_object* v___x_3466_; lean_object* v___x_3467_; lean_object* v___x_3468_; lean_object* v___x_3469_; lean_object* v___x_3470_; lean_object* v___x_3471_; lean_object* v___y_3473_; lean_object* v___y_3474_; lean_object* v___y_3475_; lean_object* v___y_3476_; lean_object* v___y_3477_; lean_object* v___y_3478_; lean_object* v___y_3479_; lean_object* v___y_3480_; uint8_t v___y_3481_; lean_object* v___y_3482_; lean_object* v___y_3483_; lean_object* v___y_3484_; lean_object* v___y_3485_; uint8_t v___y_3486_; lean_object* v___y_3487_; lean_object* v_stmt_3488_; lean_object* v___y_3521_; lean_object* v___y_3522_; uint8_t v___y_3523_; lean_object* v___y_3524_; lean_object* v___y_3525_; lean_object* v___y_3526_; lean_object* v___y_3527_; lean_object* v___y_3528_; lean_object* v___y_3529_; lean_object* v___y_3530_; lean_object* v___y_3531_; lean_object* v___y_3532_; lean_object* v_ppFail_3533_; lean_object* v___y_3543_; uint8_t v___y_3544_; lean_object* v___y_3545_; lean_object* v___y_3546_; lean_object* v___y_3547_; lean_object* v___y_3548_; lean_object* v___y_3549_; lean_object* v___y_3550_; lean_object* v___y_3551_; lean_object* v___y_3552_; lean_object* v___y_3553_; uint8_t v___y_3554_; lean_object* v___y_3573_; lean_object* v___y_3574_; lean_object* v___y_3575_; lean_object* v___y_3576_; lean_object* v___y_3577_; lean_object* v___y_3578_; lean_object* v___y_3579_; lean_object* v___y_3580_; lean_object* v___y_3581_; lean_object* v___y_3582_; lean_object* v_stmt_3583_; uint8_t v_ppOk_3584_; lean_object* v___y_3598_; lean_object* v___y_3599_; lean_object* v___y_3600_; lean_object* v___y_3601_; lean_object* v___y_3602_; lean_object* v___y_3603_; lean_object* v___y_3604_; lean_object* v___y_3605_; lean_object* v___y_3606_; lean_object* v___y_3644_; lean_object* v___y_3645_; lean_object* v___y_3646_; lean_object* v___y_3647_; lean_object* v___y_3648_; lean_object* v___y_3649_; lean_object* v___y_3650_; lean_object* v___y_3651_; lean_object* v_valConsts_3654_; lean_object* v_proofSize_3655_; lean_object* v_proofTree_3656_; lean_object* v___x_3701_; 
v___x_3393_ = 0;
v___x_3462_ = lean_box(0);
v___x_3463_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_3464_ = l_Lean_instInhabitedFileMap_default;
v___x_3465_ = l_Lean_Options_empty;
v___x_3466_ = lean_unsigned_to_nat(100u);
v___x_3467_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_3468_ = lean_box(0);
v___x_3469_ = lean_box(0);
v___x_3470_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_3471_ = lean_box(0);
lean_inc(v_snd_3068_);
v___x_3701_ = l_NsExport_valueOf_x3f(v_snd_3068_);
if (lean_obj_tag(v___x_3701_) == 1)
{
lean_object* v_val_3702_; lean_object* v___x_3703_; lean_object* v_snd_3704_; lean_object* v_fst_3705_; lean_object* v_fst_3706_; lean_object* v___x_3707_; 
v_val_3702_ = lean_ctor_get(v___x_3701_, 0);
lean_inc_n(v_val_3702_, 2);
lean_dec_ref_known(v___x_3701_, 1);
v___x_3703_ = l_NsExport_sizes(v___x_3100_, v_val_3702_);
lean_dec(v___x_3100_);
v_snd_3704_ = lean_ctor_get(v___x_3703_, 1);
lean_inc(v_snd_3704_);
v_fst_3705_ = lean_ctor_get(v___x_3703_, 0);
lean_inc(v_fst_3705_);
lean_dec_ref(v___x_3703_);
v_fst_3706_ = lean_ctor_get(v_snd_3704_, 0);
lean_inc(v_fst_3706_);
lean_dec(v_snd_3704_);
v___x_3707_ = l_Lean_Expr_getUsedConstants(v_val_3702_);
v_valConsts_3654_ = v___x_3707_;
v_proofSize_3655_ = v_fst_3706_;
v_proofTree_3656_ = v_fst_3705_;
goto v___jp_3653_;
}
else
{
lean_dec(v___x_3701_);
lean_dec(v___x_3100_);
v_valConsts_3654_ = v___x_3166_;
v_proofSize_3655_ = v___x_3113_;
v_proofTree_3656_ = v___x_3113_;
goto v___jp_3653_;
}
v___jp_3186_:
{
lean_object* v_size_3214_; lean_object* v_size_3215_; lean_object* v___x_3217_; 
v_size_3214_ = lean_ctor_get(v___y_3201_, 0);
v_size_3215_ = lean_ctor_get(v___y_3190_, 0);
lean_inc_ref(v___y_3195_);
if (v_isShared_3185_ == 0)
{
lean_ctor_set(v___x_3184_, 1, v___y_3213_);
lean_ctor_set(v___x_3184_, 0, v___y_3195_);
v___x_3217_ = v___x_3184_;
goto v_reusejp_3216_;
}
else
{
lean_object* v_reuseFailAlloc_3332_; 
v_reuseFailAlloc_3332_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3332_, 0, v___y_3195_);
lean_ctor_set(v_reuseFailAlloc_3332_, 1, v___y_3213_);
v___x_3217_ = v_reuseFailAlloc_3332_;
goto v_reusejp_3216_;
}
v_reusejp_3216_:
{
lean_object* v___x_3218_; lean_object* v___x_3219_; lean_object* v___x_3220_; lean_object* v___x_3222_; 
v___x_3218_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__3));
v___x_3219_ = l_Lean_JsonNumber_fromNat(v___y_3205_);
v___x_3220_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3220_, 0, v___x_3219_);
if (v_isShared_3180_ == 0)
{
lean_ctor_set(v___x_3179_, 1, v___x_3220_);
lean_ctor_set(v___x_3179_, 0, v___x_3218_);
v___x_3222_ = v___x_3179_;
goto v_reusejp_3221_;
}
else
{
lean_object* v_reuseFailAlloc_3331_; 
v_reuseFailAlloc_3331_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3331_, 0, v___x_3218_);
lean_ctor_set(v_reuseFailAlloc_3331_, 1, v___x_3220_);
v___x_3222_ = v_reuseFailAlloc_3331_;
goto v_reusejp_3221_;
}
v_reusejp_3221_:
{
lean_object* v___x_3223_; lean_object* v___x_3224_; lean_object* v___x_3225_; lean_object* v___x_3226_; lean_object* v___x_3228_; 
v___x_3223_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__4));
v___x_3224_ = lean_array_get_size(v___y_3210_);
lean_dec_ref(v___y_3210_);
v___x_3225_ = l_Lean_JsonNumber_fromNat(v___x_3224_);
v___x_3226_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3226_, 0, v___x_3225_);
if (v_isShared_3071_ == 0)
{
lean_ctor_set(v___x_3070_, 1, v___x_3226_);
lean_ctor_set(v___x_3070_, 0, v___x_3223_);
v___x_3228_ = v___x_3070_;
goto v_reusejp_3227_;
}
else
{
lean_object* v_reuseFailAlloc_3330_; 
v_reuseFailAlloc_3330_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3330_, 0, v___x_3223_);
lean_ctor_set(v_reuseFailAlloc_3330_, 1, v___x_3226_);
v___x_3228_ = v_reuseFailAlloc_3330_;
goto v_reusejp_3227_;
}
v_reusejp_3227_:
{
lean_object* v___x_3229_; lean_object* v___x_3230_; lean_object* v___x_3231_; lean_object* v___x_3232_; lean_object* v___x_3233_; lean_object* v___x_3234_; lean_object* v___x_3235_; lean_object* v___x_3236_; lean_object* v___x_3237_; lean_object* v___x_3238_; lean_object* v___x_3239_; lean_object* v___x_3240_; lean_object* v___x_3241_; lean_object* v___x_3242_; lean_object* v___x_3243_; lean_object* v___x_3244_; lean_object* v___x_3245_; lean_object* v___x_3246_; lean_object* v___x_3247_; lean_object* v___x_3248_; lean_object* v___x_3249_; lean_object* v___x_3250_; lean_object* v___x_3251_; lean_object* v___x_3252_; lean_object* v___x_3253_; lean_object* v___x_3254_; lean_object* v___x_3255_; lean_object* v___x_3256_; lean_object* v___x_3257_; lean_object* v___x_3258_; lean_object* v___x_3259_; uint64_t v___x_3260_; lean_object* v___x_3261_; lean_object* v___x_3262_; lean_object* v___x_3263_; lean_object* v___x_3264_; lean_object* v___x_3265_; lean_object* v___x_3266_; lean_object* v___x_3267_; lean_object* v___x_3268_; lean_object* v___x_3269_; lean_object* v___x_3270_; lean_object* v___x_3271_; lean_object* v___x_3272_; lean_object* v___x_3273_; lean_object* v___x_3274_; lean_object* v___x_3275_; lean_object* v___x_3276_; lean_object* v___x_3277_; lean_object* v___x_3278_; lean_object* v___x_3279_; lean_object* v___x_3280_; lean_object* v___x_3281_; lean_object* v___x_3282_; lean_object* v___x_3283_; lean_object* v___x_3284_; lean_object* v___x_3285_; lean_object* v___x_3286_; lean_object* v___x_3287_; lean_object* v___x_3288_; lean_object* v___x_3289_; lean_object* v___x_3290_; lean_object* v___x_3291_; 
v___x_3229_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__5));
v___x_3230_ = lean_array_get_size(v___x_3167_);
lean_dec(v___x_3167_);
v___x_3231_ = l_Lean_JsonNumber_fromNat(v___x_3230_);
v___x_3232_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3232_, 0, v___x_3231_);
v___x_3233_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3233_, 0, v___x_3229_);
lean_ctor_set(v___x_3233_, 1, v___x_3232_);
v___x_3234_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__6));
v___x_3235_ = l_NsExport_sortedNames(v___y_3188_);
lean_dec_ref(v___y_3188_);
v___x_3236_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_3235_);
v___x_3237_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3237_, 0, v___x_3234_);
lean_ctor_set(v___x_3237_, 1, v___x_3236_);
v___x_3238_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__7));
v___x_3239_ = l_NsExport_sortedNames(v___y_3208_);
lean_dec_ref(v___y_3208_);
v___x_3240_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_3239_);
v___x_3241_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3241_, 0, v___x_3238_);
lean_ctor_set(v___x_3241_, 1, v___x_3240_);
v___x_3242_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__8));
lean_inc(v_size_3214_);
v___x_3243_ = l_Lean_JsonNumber_fromNat(v_size_3214_);
v___x_3244_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3244_, 0, v___x_3243_);
v___x_3245_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3245_, 0, v___x_3242_);
lean_ctor_set(v___x_3245_, 1, v___x_3244_);
v___x_3246_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__9));
lean_inc(v_size_3215_);
v___x_3247_ = l_Lean_JsonNumber_fromNat(v_size_3215_);
v___x_3248_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3248_, 0, v___x_3247_);
v___x_3249_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3249_, 0, v___x_3246_);
lean_ctor_set(v___x_3249_, 1, v___x_3248_);
v___x_3250_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__10));
v___x_3251_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0(v___x_3113_, v_a_3047_, v___y_3201_);
v___x_3252_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3252_, 0, v___x_3250_);
lean_ctor_set(v___x_3252_, 1, v___x_3251_);
v___x_3253_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__11));
v___x_3254_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0(v___x_3113_, v_a_3047_, v___y_3190_);
v___x_3255_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3255_, 0, v___x_3253_);
lean_ctor_set(v___x_3255_, 1, v___x_3254_);
v___x_3256_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__12));
v___x_3257_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_3257_, 0, v___y_3194_);
v___x_3258_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3258_, 0, v___x_3256_);
lean_ctor_set(v___x_3258_, 1, v___x_3257_);
v___x_3259_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__13));
v___x_3260_ = lean_unbox_uint64(v_snd_3109_);
lean_dec(v_snd_3109_);
v___x_3261_ = l_NsExport_hexOf(v___x_3260_);
v___x_3262_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_3262_, 0, v___x_3261_);
v___x_3263_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3263_, 0, v___x_3259_);
lean_ctor_set(v___x_3263_, 1, v___x_3262_);
v___x_3264_ = lean_box(0);
v___x_3265_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3265_, 0, v___x_3263_);
lean_ctor_set(v___x_3265_, 1, v___x_3264_);
v___x_3266_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3266_, 0, v___x_3258_);
lean_ctor_set(v___x_3266_, 1, v___x_3265_);
v___x_3267_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3267_, 0, v___x_3255_);
lean_ctor_set(v___x_3267_, 1, v___x_3266_);
v___x_3268_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3268_, 0, v___x_3252_);
lean_ctor_set(v___x_3268_, 1, v___x_3267_);
v___x_3269_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3269_, 0, v___x_3249_);
lean_ctor_set(v___x_3269_, 1, v___x_3268_);
v___x_3270_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3270_, 0, v___x_3245_);
lean_ctor_set(v___x_3270_, 1, v___x_3269_);
v___x_3271_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3271_, 0, v___x_3241_);
lean_ctor_set(v___x_3271_, 1, v___x_3270_);
v___x_3272_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3272_, 0, v___x_3237_);
lean_ctor_set(v___x_3272_, 1, v___x_3271_);
v___x_3273_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3273_, 0, v___x_3233_);
lean_ctor_set(v___x_3273_, 1, v___x_3272_);
v___x_3274_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3274_, 0, v___x_3228_);
lean_ctor_set(v___x_3274_, 1, v___x_3273_);
v___x_3275_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3275_, 0, v___x_3222_);
lean_ctor_set(v___x_3275_, 1, v___x_3274_);
v___x_3276_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3276_, 0, v___x_3217_);
lean_ctor_set(v___x_3276_, 1, v___x_3275_);
v___x_3277_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3277_, 0, v___y_3211_);
lean_ctor_set(v___x_3277_, 1, v___x_3276_);
v___x_3278_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3278_, 0, v___y_3202_);
lean_ctor_set(v___x_3278_, 1, v___x_3277_);
v___x_3279_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3279_, 0, v___y_3187_);
lean_ctor_set(v___x_3279_, 1, v___x_3278_);
v___x_3280_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3280_, 0, v___y_3189_);
lean_ctor_set(v___x_3280_, 1, v___x_3279_);
v___x_3281_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3281_, 0, v___y_3204_);
lean_ctor_set(v___x_3281_, 1, v___x_3280_);
v___x_3282_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3282_, 0, v___y_3191_);
lean_ctor_set(v___x_3282_, 1, v___x_3281_);
v___x_3283_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3283_, 0, v___y_3200_);
lean_ctor_set(v___x_3283_, 1, v___x_3282_);
v___x_3284_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3284_, 0, v___y_3193_);
lean_ctor_set(v___x_3284_, 1, v___x_3283_);
v___x_3285_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3285_, 0, v___y_3206_);
lean_ctor_set(v___x_3285_, 1, v___x_3284_);
v___x_3286_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3286_, 0, v___y_3209_);
lean_ctor_set(v___x_3286_, 1, v___x_3285_);
v___x_3287_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3287_, 0, v___y_3207_);
lean_ctor_set(v___x_3287_, 1, v___x_3286_);
v___x_3288_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3288_, 0, v___y_3212_);
lean_ctor_set(v___x_3288_, 1, v___x_3287_);
v___x_3289_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3289_, 0, v___y_3196_);
lean_ctor_set(v___x_3289_, 1, v___x_3288_);
v___x_3290_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3290_, 0, v___y_3197_);
lean_ctor_set(v___x_3290_, 1, v___x_3289_);
v___x_3291_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3291_, 0, v___y_3198_);
lean_ctor_set(v___x_3291_, 1, v___x_3290_);
if (lean_obj_tag(v___y_3203_) == 0)
{
lean_object* v___x_3292_; lean_object* v___x_3293_; 
v___x_3292_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__19));
v___x_3293_ = l_List_appendTR___redArg(v___x_3291_, v___x_3292_);
v___y_3115_ = v___y_3192_;
v___y_3116_ = v___y_3199_;
v_fields_3117_ = v___x_3293_;
goto v___jp_3114_;
}
else
{
lean_object* v_val_3294_; lean_object* v___x_3296_; uint8_t v_isShared_3297_; uint8_t v_isSharedCheck_3329_; 
v_val_3294_ = lean_ctor_get(v___y_3203_, 0);
v_isSharedCheck_3329_ = !lean_is_exclusive(v___y_3203_);
if (v_isSharedCheck_3329_ == 0)
{
v___x_3296_ = v___y_3203_;
v_isShared_3297_ = v_isSharedCheck_3329_;
goto v_resetjp_3295_;
}
else
{
lean_inc(v_val_3294_);
lean_dec(v___y_3203_);
v___x_3296_ = lean_box(0);
v_isShared_3297_ = v_isSharedCheck_3329_;
goto v_resetjp_3295_;
}
v_resetjp_3295_:
{
lean_object* v_pos_3298_; lean_object* v_endPos_3299_; lean_object* v_line_3300_; lean_object* v___x_3302_; uint8_t v_isShared_3303_; uint8_t v_isSharedCheck_3327_; 
v_pos_3298_ = lean_ctor_get(v_val_3294_, 0);
lean_inc_ref(v_pos_3298_);
v_endPos_3299_ = lean_ctor_get(v_val_3294_, 2);
lean_inc_ref(v_endPos_3299_);
lean_dec(v_val_3294_);
v_line_3300_ = lean_ctor_get(v_pos_3298_, 0);
v_isSharedCheck_3327_ = !lean_is_exclusive(v_pos_3298_);
if (v_isSharedCheck_3327_ == 0)
{
lean_object* v_unused_3328_; 
v_unused_3328_ = lean_ctor_get(v_pos_3298_, 1);
lean_dec(v_unused_3328_);
v___x_3302_ = v_pos_3298_;
v_isShared_3303_ = v_isSharedCheck_3327_;
goto v_resetjp_3301_;
}
else
{
lean_inc(v_line_3300_);
lean_dec(v_pos_3298_);
v___x_3302_ = lean_box(0);
v_isShared_3303_ = v_isSharedCheck_3327_;
goto v_resetjp_3301_;
}
v_resetjp_3301_:
{
lean_object* v_line_3304_; lean_object* v___x_3306_; uint8_t v_isShared_3307_; uint8_t v_isSharedCheck_3325_; 
v_line_3304_ = lean_ctor_get(v_endPos_3299_, 0);
v_isSharedCheck_3325_ = !lean_is_exclusive(v_endPos_3299_);
if (v_isSharedCheck_3325_ == 0)
{
lean_object* v_unused_3326_; 
v_unused_3326_ = lean_ctor_get(v_endPos_3299_, 1);
lean_dec(v_unused_3326_);
v___x_3306_ = v_endPos_3299_;
v_isShared_3307_ = v_isSharedCheck_3325_;
goto v_resetjp_3305_;
}
else
{
lean_inc(v_line_3304_);
lean_dec(v_endPos_3299_);
v___x_3306_ = lean_box(0);
v_isShared_3307_ = v_isSharedCheck_3325_;
goto v_resetjp_3305_;
}
v_resetjp_3305_:
{
lean_object* v___x_3308_; lean_object* v___x_3309_; lean_object* v___x_3311_; 
v___x_3308_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__14));
v___x_3309_ = l_Lean_JsonNumber_fromNat(v_line_3300_);
if (v_isShared_3297_ == 0)
{
lean_ctor_set_tag(v___x_3296_, 2);
lean_ctor_set(v___x_3296_, 0, v___x_3309_);
v___x_3311_ = v___x_3296_;
goto v_reusejp_3310_;
}
else
{
lean_object* v_reuseFailAlloc_3324_; 
v_reuseFailAlloc_3324_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3324_, 0, v___x_3309_);
v___x_3311_ = v_reuseFailAlloc_3324_;
goto v_reusejp_3310_;
}
v_reusejp_3310_:
{
lean_object* v___x_3313_; 
if (v_isShared_3307_ == 0)
{
lean_ctor_set(v___x_3306_, 1, v___x_3311_);
lean_ctor_set(v___x_3306_, 0, v___x_3308_);
v___x_3313_ = v___x_3306_;
goto v_reusejp_3312_;
}
else
{
lean_object* v_reuseFailAlloc_3323_; 
v_reuseFailAlloc_3323_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3323_, 0, v___x_3308_);
lean_ctor_set(v_reuseFailAlloc_3323_, 1, v___x_3311_);
v___x_3313_ = v_reuseFailAlloc_3323_;
goto v_reusejp_3312_;
}
v_reusejp_3312_:
{
lean_object* v___x_3314_; lean_object* v___x_3315_; lean_object* v___x_3316_; lean_object* v___x_3318_; 
v___x_3314_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__16));
v___x_3315_ = l_Lean_JsonNumber_fromNat(v_line_3304_);
v___x_3316_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3316_, 0, v___x_3315_);
if (v_isShared_3303_ == 0)
{
lean_ctor_set(v___x_3302_, 1, v___x_3316_);
lean_ctor_set(v___x_3302_, 0, v___x_3314_);
v___x_3318_ = v___x_3302_;
goto v_reusejp_3317_;
}
else
{
lean_object* v_reuseFailAlloc_3322_; 
v_reuseFailAlloc_3322_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3322_, 0, v___x_3314_);
lean_ctor_set(v_reuseFailAlloc_3322_, 1, v___x_3316_);
v___x_3318_ = v_reuseFailAlloc_3322_;
goto v_reusejp_3317_;
}
v_reusejp_3317_:
{
lean_object* v___x_3319_; lean_object* v___x_3320_; lean_object* v___x_3321_; 
v___x_3319_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3319_, 0, v___x_3318_);
lean_ctor_set(v___x_3319_, 1, v___x_3264_);
v___x_3320_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3320_, 0, v___x_3313_);
lean_ctor_set(v___x_3320_, 1, v___x_3319_);
v___x_3321_ = l_List_appendTR___redArg(v___x_3291_, v___x_3320_);
v___y_3115_ = v___y_3192_;
v___y_3116_ = v___y_3199_;
v_fields_3117_ = v___x_3321_;
goto v___jp_3114_;
}
}
}
}
}
}
}
}
}
}
}
v___jp_3333_:
{
lean_object* v___x_3359_; lean_object* v___x_3360_; lean_object* v___x_3361_; lean_object* v___x_3362_; lean_object* v___x_3363_; lean_object* v___x_3364_; lean_object* v___x_3365_; lean_object* v___x_3366_; lean_object* v___x_3367_; lean_object* v___x_3368_; lean_object* v___x_3369_; lean_object* v___x_3370_; lean_object* v___x_3371_; lean_object* v___x_3372_; uint8_t v___x_3373_; lean_object* v___x_3374_; lean_object* v___x_3375_; lean_object* v___x_3376_; lean_object* v___x_3377_; lean_object* v___x_3378_; lean_object* v___x_3379_; lean_object* v___x_3380_; lean_object* v___x_3381_; lean_object* v___x_3382_; lean_object* v___x_3383_; lean_object* v___x_3384_; lean_object* v___x_3385_; lean_object* v___x_3386_; lean_object* v___x_3387_; uint8_t v___x_3388_; 
v___x_3359_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_3359_, 0, v___y_3358_);
lean_inc_ref(v___y_3338_);
v___x_3360_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3360_, 0, v___y_3338_);
lean_ctor_set(v___x_3360_, 1, v___x_3359_);
v___x_3361_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__20));
v___x_3362_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_3362_, 0, v___y_3350_);
v___x_3363_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3363_, 0, v___x_3361_);
lean_ctor_set(v___x_3363_, 1, v___x_3362_);
v___x_3364_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__21));
v___x_3365_ = l_Lean_JsonNumber_fromNat(v___y_3355_);
v___x_3366_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3366_, 0, v___x_3365_);
v___x_3367_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3367_, 0, v___x_3364_);
lean_ctor_set(v___x_3367_, 1, v___x_3366_);
v___x_3368_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__22));
v___x_3369_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_3369_, 0, v___y_3356_);
v___x_3370_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3370_, 0, v___x_3368_);
lean_ctor_set(v___x_3370_, 1, v___x_3369_);
v___x_3371_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__23));
v___x_3372_ = lean_alloc_ctor(1, 0, 1);
v___x_3373_ = lean_unbox(v___y_3353_);
lean_dec(v___y_3353_);
lean_ctor_set_uint8(v___x_3372_, 0, v___x_3373_);
v___x_3374_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3374_, 0, v___x_3371_);
lean_ctor_set(v___x_3374_, 1, v___x_3372_);
v___x_3375_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__24));
v___x_3376_ = l_Lean_JsonNumber_fromNat(v_fst_3181_);
v___x_3377_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3377_, 0, v___x_3376_);
v___x_3378_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3378_, 0, v___x_3375_);
lean_ctor_set(v___x_3378_, 1, v___x_3377_);
v___x_3379_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__25));
v___x_3380_ = l_Lean_JsonNumber_fromNat(v_snd_3182_);
v___x_3381_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3381_, 0, v___x_3380_);
v___x_3382_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3382_, 0, v___x_3379_);
lean_ctor_set(v___x_3382_, 1, v___x_3381_);
v___x_3383_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__26));
v___x_3384_ = l_Lean_JsonNumber_fromNat(v___y_3357_);
v___x_3385_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3385_, 0, v___x_3384_);
v___x_3386_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3386_, 0, v___x_3383_);
lean_ctor_set(v___x_3386_, 1, v___x_3385_);
v___x_3387_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__27));
v___x_3388_ = lean_nat_dec_eq(v___y_3348_, v___x_3113_);
if (v___x_3388_ == 0)
{
lean_object* v___x_3389_; lean_object* v___x_3390_; lean_object* v___x_3391_; 
v___x_3389_ = lean_nat_log2(v___y_3348_);
lean_dec(v___y_3348_);
v___x_3390_ = l_Lean_JsonNumber_fromNat(v___x_3389_);
v___x_3391_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3391_, 0, v___x_3390_);
v___y_3187_ = v___x_3378_;
v___y_3188_ = v___y_3334_;
v___y_3189_ = v___x_3374_;
v___y_3190_ = v___y_3335_;
v___y_3191_ = v___x_3367_;
v___y_3192_ = v___y_3336_;
v___y_3193_ = v___x_3360_;
v___y_3194_ = v___y_3337_;
v___y_3195_ = v___x_3387_;
v___y_3196_ = v___y_3339_;
v___y_3197_ = v___y_3340_;
v___y_3198_ = v___y_3341_;
v___y_3199_ = v___y_3342_;
v___y_3200_ = v___x_3363_;
v___y_3201_ = v___y_3343_;
v___y_3202_ = v___x_3382_;
v___y_3203_ = v___y_3344_;
v___y_3204_ = v___x_3370_;
v___y_3205_ = v___y_3345_;
v___y_3206_ = v___y_3346_;
v___y_3207_ = v___y_3347_;
v___y_3208_ = v___y_3349_;
v___y_3209_ = v___y_3351_;
v___y_3210_ = v___y_3352_;
v___y_3211_ = v___x_3386_;
v___y_3212_ = v___y_3354_;
v___y_3213_ = v___x_3391_;
goto v___jp_3186_;
}
else
{
lean_object* v___x_3392_; 
lean_dec(v___y_3348_);
v___x_3392_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29);
v___y_3187_ = v___x_3378_;
v___y_3188_ = v___y_3334_;
v___y_3189_ = v___x_3374_;
v___y_3190_ = v___y_3335_;
v___y_3191_ = v___x_3367_;
v___y_3192_ = v___y_3336_;
v___y_3193_ = v___x_3360_;
v___y_3194_ = v___y_3337_;
v___y_3195_ = v___x_3387_;
v___y_3196_ = v___y_3339_;
v___y_3197_ = v___y_3340_;
v___y_3198_ = v___y_3341_;
v___y_3199_ = v___y_3342_;
v___y_3200_ = v___x_3363_;
v___y_3201_ = v___y_3343_;
v___y_3202_ = v___x_3382_;
v___y_3203_ = v___y_3344_;
v___y_3204_ = v___x_3370_;
v___y_3205_ = v___y_3345_;
v___y_3206_ = v___y_3346_;
v___y_3207_ = v___y_3347_;
v___y_3208_ = v___y_3349_;
v___y_3209_ = v___y_3351_;
v___y_3210_ = v___y_3352_;
v___y_3211_ = v___x_3386_;
v___y_3212_ = v___y_3354_;
v___y_3213_ = v___x_3392_;
goto v___jp_3186_;
}
}
v___jp_3394_:
{
lean_object* v___x_3413_; lean_object* v___x_3414_; lean_object* v___x_3415_; lean_object* v___x_3416_; lean_object* v___x_3417_; lean_object* v___x_3418_; lean_object* v___x_3419_; lean_object* v___x_3420_; lean_object* v___x_3421_; lean_object* v___x_3422_; lean_object* v___x_3423_; lean_object* v___x_3424_; lean_object* v___x_3425_; lean_object* v___x_3426_; lean_object* v___x_3427_; lean_object* v___x_3428_; lean_object* v___x_3429_; lean_object* v___x_3430_; uint8_t v___x_3431_; lean_object* v___x_3432_; lean_object* v___x_3433_; lean_object* v___x_3434_; uint8_t v___x_3435_; lean_object* v___x_3436_; lean_object* v___x_3437_; lean_object* v___x_3438_; uint8_t v___x_3439_; lean_object* v___x_3440_; lean_object* v___x_3441_; lean_object* v___x_3442_; 
v___x_3413_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__30));
lean_inc_n(v_fst_3067_, 2);
v___x_3414_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_3067_, v___x_3393_);
v___x_3415_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_3415_, 0, v___x_3414_);
v___x_3416_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3416_, 0, v___x_3413_);
lean_ctor_set(v___x_3416_, 1, v___x_3415_);
v___x_3417_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__31));
v___x_3418_ = l_Lean_privateToUserName(v_fst_3067_);
v___x_3419_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v___x_3418_, v___x_3393_);
v___x_3420_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_3420_, 0, v___x_3419_);
v___x_3421_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3421_, 0, v___x_3417_);
lean_ctor_set(v___x_3421_, 1, v___x_3420_);
v___x_3422_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__32));
v___x_3423_ = l_NsExport_moduleOf(v_a_3047_, v_fst_3067_);
v___x_3424_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v___x_3423_, v___x_3093_);
v___x_3425_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_3425_, 0, v___x_3424_);
v___x_3426_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3426_, 0, v___x_3422_);
lean_ctor_set(v___x_3426_, 1, v___x_3425_);
v___x_3427_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__33));
lean_inc_ref(v___y_3399_);
v___x_3428_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_3428_, 0, v___y_3399_);
v___x_3429_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3429_, 0, v___x_3427_);
lean_ctor_set(v___x_3429_, 1, v___x_3428_);
v___x_3430_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__34));
lean_inc_ref_n(v_a_3047_, 2);
v___x_3431_ = l_Lean_isClass(v_a_3047_, v_fst_3067_);
v___x_3432_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_3432_, 0, v___x_3431_);
v___x_3433_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3433_, 0, v___x_3430_);
lean_ctor_set(v___x_3433_, 1, v___x_3432_);
v___x_3434_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__35));
v___x_3435_ = l_Lean_Meta_isInstanceCore(v_a_3047_, v_fst_3067_);
v___x_3436_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_3436_, 0, v___x_3435_);
v___x_3437_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3437_, 0, v___x_3434_);
lean_ctor_set(v___x_3437_, 1, v___x_3436_);
v___x_3438_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__36));
v___x_3439_ = l_Lean_isPrivateName(v_fst_3067_);
lean_dec(v_fst_3067_);
v___x_3440_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_3440_, 0, v___x_3439_);
v___x_3441_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3441_, 0, v___x_3438_);
lean_ctor_set(v___x_3441_, 1, v___x_3440_);
v___x_3442_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__37));
if (lean_obj_tag(v___y_3398_) == 0)
{
v___y_3334_ = v___y_3395_;
v___y_3335_ = v___y_3401_;
v___y_3336_ = v___y_3402_;
v___y_3337_ = v___y_3404_;
v___y_3338_ = v___x_3442_;
v___y_3339_ = v___x_3426_;
v___y_3340_ = v___x_3421_;
v___y_3341_ = v___x_3416_;
v___y_3342_ = v___y_3396_;
v___y_3343_ = v___y_3397_;
v___y_3344_ = v_a_3412_;
v___y_3345_ = v___y_3400_;
v___y_3346_ = v___x_3441_;
v___y_3347_ = v___x_3433_;
v___y_3348_ = v___y_3403_;
v___y_3349_ = v___y_3405_;
v___y_3350_ = v___y_3406_;
v___y_3351_ = v___x_3437_;
v___y_3352_ = v___y_3407_;
v___y_3353_ = v___y_3408_;
v___y_3354_ = v___x_3429_;
v___y_3355_ = v___y_3409_;
v___y_3356_ = v___y_3410_;
v___y_3357_ = v___y_3411_;
v___y_3358_ = v___x_3393_;
goto v___jp_3333_;
}
else
{
lean_dec_ref_known(v___y_3398_, 1);
v___y_3334_ = v___y_3395_;
v___y_3335_ = v___y_3401_;
v___y_3336_ = v___y_3402_;
v___y_3337_ = v___y_3404_;
v___y_3338_ = v___x_3442_;
v___y_3339_ = v___x_3426_;
v___y_3340_ = v___x_3421_;
v___y_3341_ = v___x_3416_;
v___y_3342_ = v___y_3396_;
v___y_3343_ = v___y_3397_;
v___y_3344_ = v_a_3412_;
v___y_3345_ = v___y_3400_;
v___y_3346_ = v___x_3441_;
v___y_3347_ = v___x_3433_;
v___y_3348_ = v___y_3403_;
v___y_3349_ = v___y_3405_;
v___y_3350_ = v___y_3406_;
v___y_3351_ = v___x_3437_;
v___y_3352_ = v___y_3407_;
v___y_3353_ = v___y_3408_;
v___y_3354_ = v___x_3429_;
v___y_3355_ = v___y_3409_;
v___y_3356_ = v___y_3410_;
v___y_3357_ = v___y_3411_;
v___y_3358_ = v___x_3093_;
goto v___jp_3333_;
}
}
v___jp_3443_:
{
lean_object* v___x_3461_; 
v___x_3461_ = lean_box(0);
v___y_3395_ = v___y_3444_;
v___y_3396_ = v___y_3445_;
v___y_3397_ = v___y_3446_;
v___y_3398_ = v___y_3447_;
v___y_3399_ = v___y_3448_;
v___y_3400_ = v___y_3449_;
v___y_3401_ = v___y_3450_;
v___y_3402_ = v___y_3451_;
v___y_3403_ = v___y_3452_;
v___y_3404_ = v___y_3453_;
v___y_3405_ = v___y_3454_;
v___y_3406_ = v___y_3455_;
v___y_3407_ = v___y_3456_;
v___y_3408_ = v___y_3457_;
v___y_3409_ = v___y_3458_;
v___y_3410_ = v___y_3459_;
v___y_3411_ = v___y_3460_;
v_a_3412_ = v___x_3461_;
goto v___jp_3394_;
}
v___jp_3472_:
{
lean_object* v___x_3489_; 
lean_inc(v_fst_3067_);
lean_inc_ref(v_a_3047_);
v___x_3489_ = l_Lean_findDocString_x3f(v_a_3047_, v_fst_3067_, v___x_3093_, v___x_3465_, v___x_3462_, v___x_3469_);
if (lean_obj_tag(v___x_3489_) == 0)
{
lean_object* v_a_3490_; lean_object* v___x_3491_; lean_object* v___x_3492_; 
v_a_3490_ = lean_ctor_get(v___x_3489_, 0);
lean_inc(v_a_3490_);
lean_dec_ref_known(v___x_3489_, 1);
lean_inc(v_fst_3067_);
v___x_3491_ = lean_alloc_closure((void*)(l_Lean_findDeclarationRanges_x3f___at___00Lean_Linter_EnvLinter_sortResults_spec__0___boxed), 4, 1);
lean_closure_set(v___x_3491_, 0, v_fst_3067_);
lean_inc_ref(v_a_3047_);
v___x_3492_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3113_, v___x_3090_, v___x_3462_, v___x_3093_, v_a_3047_, v___x_3467_, v___x_3463_, v___x_3464_, v___x_3468_, v___x_3469_, v___x_3470_, v___x_3471_, v___x_3393_, lean_box(0), v___x_3491_);
if (lean_obj_tag(v___x_3492_) == 0)
{
lean_object* v_a_3493_; 
v_a_3493_ = lean_ctor_get(v___x_3492_, 0);
lean_inc(v_a_3493_);
lean_dec_ref_known(v___x_3492_, 1);
if (lean_obj_tag(v_a_3493_) == 0)
{
v___y_3444_ = v___y_3473_;
v___y_3445_ = v___y_3474_;
v___y_3446_ = v___y_3475_;
v___y_3447_ = v_a_3490_;
v___y_3448_ = v___y_3476_;
v___y_3449_ = v___y_3477_;
v___y_3450_ = v___y_3478_;
v___y_3451_ = v___y_3479_;
v___y_3452_ = v___y_3480_;
v___y_3453_ = v___y_3481_;
v___y_3454_ = v___y_3482_;
v___y_3455_ = v_stmt_3488_;
v___y_3456_ = v___y_3483_;
v___y_3457_ = v___y_3484_;
v___y_3458_ = v___y_3485_;
v___y_3459_ = v___y_3486_;
v___y_3460_ = v___y_3487_;
goto v___jp_3443_;
}
else
{
lean_object* v_val_3494_; 
v_val_3494_ = lean_ctor_get(v_a_3493_, 0);
lean_inc(v_val_3494_);
lean_dec_ref_known(v_a_3493_, 1);
if (lean_obj_tag(v_val_3494_) == 0)
{
v___y_3444_ = v___y_3473_;
v___y_3445_ = v___y_3474_;
v___y_3446_ = v___y_3475_;
v___y_3447_ = v_a_3490_;
v___y_3448_ = v___y_3476_;
v___y_3449_ = v___y_3477_;
v___y_3450_ = v___y_3478_;
v___y_3451_ = v___y_3479_;
v___y_3452_ = v___y_3480_;
v___y_3453_ = v___y_3481_;
v___y_3454_ = v___y_3482_;
v___y_3455_ = v_stmt_3488_;
v___y_3456_ = v___y_3483_;
v___y_3457_ = v___y_3484_;
v___y_3458_ = v___y_3485_;
v___y_3459_ = v___y_3486_;
v___y_3460_ = v___y_3487_;
goto v___jp_3443_;
}
else
{
lean_object* v_val_3495_; lean_object* v___x_3497_; uint8_t v_isShared_3498_; uint8_t v_isSharedCheck_3503_; 
v_val_3495_ = lean_ctor_get(v_val_3494_, 0);
v_isSharedCheck_3503_ = !lean_is_exclusive(v_val_3494_);
if (v_isSharedCheck_3503_ == 0)
{
v___x_3497_ = v_val_3494_;
v_isShared_3498_ = v_isSharedCheck_3503_;
goto v_resetjp_3496_;
}
else
{
lean_inc(v_val_3495_);
lean_dec(v_val_3494_);
v___x_3497_ = lean_box(0);
v_isShared_3498_ = v_isSharedCheck_3503_;
goto v_resetjp_3496_;
}
v_resetjp_3496_:
{
lean_object* v_range_3499_; lean_object* v___x_3501_; 
v_range_3499_ = lean_ctor_get(v_val_3495_, 0);
lean_inc_ref(v_range_3499_);
lean_dec(v_val_3495_);
if (v_isShared_3498_ == 0)
{
lean_ctor_set(v___x_3497_, 0, v_range_3499_);
v___x_3501_ = v___x_3497_;
goto v_reusejp_3500_;
}
else
{
lean_object* v_reuseFailAlloc_3502_; 
v_reuseFailAlloc_3502_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3502_, 0, v_range_3499_);
v___x_3501_ = v_reuseFailAlloc_3502_;
goto v_reusejp_3500_;
}
v_reusejp_3500_:
{
v___y_3395_ = v___y_3473_;
v___y_3396_ = v___y_3474_;
v___y_3397_ = v___y_3475_;
v___y_3398_ = v_a_3490_;
v___y_3399_ = v___y_3476_;
v___y_3400_ = v___y_3477_;
v___y_3401_ = v___y_3478_;
v___y_3402_ = v___y_3479_;
v___y_3403_ = v___y_3480_;
v___y_3404_ = v___y_3481_;
v___y_3405_ = v___y_3482_;
v___y_3406_ = v_stmt_3488_;
v___y_3407_ = v___y_3483_;
v___y_3408_ = v___y_3484_;
v___y_3409_ = v___y_3485_;
v___y_3410_ = v___y_3486_;
v___y_3411_ = v___y_3487_;
v_a_3412_ = v___x_3501_;
goto v___jp_3394_;
}
}
}
}
}
else
{
lean_object* v_a_3504_; lean_object* v___x_3506_; uint8_t v_isShared_3507_; uint8_t v_isSharedCheck_3511_; 
lean_dec(v_a_3490_);
lean_dec_ref(v_stmt_3488_);
lean_dec(v___y_3487_);
lean_dec(v___y_3485_);
lean_dec(v___y_3484_);
lean_dec_ref(v___y_3483_);
lean_dec_ref(v___y_3482_);
lean_dec(v___y_3480_);
lean_dec(v___y_3479_);
lean_dec_ref(v___y_3478_);
lean_dec(v___y_3477_);
lean_dec_ref(v___y_3475_);
lean_dec(v___y_3474_);
lean_dec_ref(v___y_3473_);
lean_del_object(v___x_3184_);
lean_dec(v_snd_3182_);
lean_dec(v_fst_3181_);
lean_del_object(v___x_3179_);
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_del_object(v___x_3070_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3504_ = lean_ctor_get(v___x_3492_, 0);
v_isSharedCheck_3511_ = !lean_is_exclusive(v___x_3492_);
if (v_isSharedCheck_3511_ == 0)
{
v___x_3506_ = v___x_3492_;
v_isShared_3507_ = v_isSharedCheck_3511_;
goto v_resetjp_3505_;
}
else
{
lean_inc(v_a_3504_);
lean_dec(v___x_3492_);
v___x_3506_ = lean_box(0);
v_isShared_3507_ = v_isSharedCheck_3511_;
goto v_resetjp_3505_;
}
v_resetjp_3505_:
{
lean_object* v___x_3509_; 
if (v_isShared_3507_ == 0)
{
v___x_3509_ = v___x_3506_;
goto v_reusejp_3508_;
}
else
{
lean_object* v_reuseFailAlloc_3510_; 
v_reuseFailAlloc_3510_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3510_, 0, v_a_3504_);
v___x_3509_ = v_reuseFailAlloc_3510_;
goto v_reusejp_3508_;
}
v_reusejp_3508_:
{
return v___x_3509_;
}
}
}
}
else
{
lean_object* v_a_3512_; lean_object* v___x_3514_; uint8_t v_isShared_3515_; uint8_t v_isSharedCheck_3519_; 
lean_dec_ref(v_stmt_3488_);
lean_dec(v___y_3487_);
lean_dec(v___y_3485_);
lean_dec(v___y_3484_);
lean_dec_ref(v___y_3483_);
lean_dec_ref(v___y_3482_);
lean_dec(v___y_3480_);
lean_dec(v___y_3479_);
lean_dec_ref(v___y_3478_);
lean_dec(v___y_3477_);
lean_dec_ref(v___y_3475_);
lean_dec(v___y_3474_);
lean_dec_ref(v___y_3473_);
lean_del_object(v___x_3184_);
lean_dec(v_snd_3182_);
lean_dec(v_fst_3181_);
lean_del_object(v___x_3179_);
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_del_object(v___x_3070_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3512_ = lean_ctor_get(v___x_3489_, 0);
v_isSharedCheck_3519_ = !lean_is_exclusive(v___x_3489_);
if (v_isSharedCheck_3519_ == 0)
{
v___x_3514_ = v___x_3489_;
v_isShared_3515_ = v_isSharedCheck_3519_;
goto v_resetjp_3513_;
}
else
{
lean_inc(v_a_3512_);
lean_dec(v___x_3489_);
v___x_3514_ = lean_box(0);
v_isShared_3515_ = v_isSharedCheck_3519_;
goto v_resetjp_3513_;
}
v_resetjp_3513_:
{
lean_object* v___x_3517_; 
if (v_isShared_3515_ == 0)
{
v___x_3517_ = v___x_3514_;
goto v_reusejp_3516_;
}
else
{
lean_object* v_reuseFailAlloc_3518_; 
v_reuseFailAlloc_3518_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3518_, 0, v_a_3512_);
v___x_3517_ = v_reuseFailAlloc_3518_;
goto v_reusejp_3516_;
}
v_reusejp_3516_:
{
return v___x_3517_;
}
}
}
}
v___jp_3520_:
{
lean_object* v___x_3534_; lean_object* v___x_3535_; uint8_t v___x_3536_; 
v___x_3534_ = lean_string_length(v___y_3530_);
v___x_3535_ = lean_unsigned_to_nat(2000u);
v___x_3536_ = lean_nat_dec_lt(v___x_3535_, v___x_3534_);
if (v___x_3536_ == 0)
{
v___y_3473_ = v___y_3524_;
v___y_3474_ = v_ppFail_3533_;
v___y_3475_ = v___y_3527_;
v___y_3476_ = v___y_3529_;
v___y_3477_ = v___y_3531_;
v___y_3478_ = v___y_3532_;
v___y_3479_ = v___x_3535_;
v___y_3480_ = v___y_3521_;
v___y_3481_ = v___y_3523_;
v___y_3482_ = v___y_3522_;
v___y_3483_ = v___y_3525_;
v___y_3484_ = v___y_3526_;
v___y_3485_ = v___x_3534_;
v___y_3486_ = v___x_3536_;
v___y_3487_ = v___y_3528_;
v_stmt_3488_ = v___y_3530_;
goto v___jp_3472_;
}
else
{
lean_object* v___x_3537_; lean_object* v___x_3538_; lean_object* v___x_3539_; lean_object* v___x_3540_; lean_object* v___x_3541_; 
v___x_3537_ = lean_string_utf8_byte_size(v___y_3530_);
lean_inc(v___y_3530_);
v___x_3538_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_3538_, 0, v___y_3530_);
lean_ctor_set(v___x_3538_, 1, v___x_3113_);
lean_ctor_set(v___x_3538_, 2, v___x_3537_);
v___x_3539_ = l_String_Slice_Pos_nextn(v___x_3538_, v___x_3113_, v___x_3535_);
lean_dec_ref_known(v___x_3538_, 3);
v___x_3540_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_3540_, 0, v___y_3530_);
lean_ctor_set(v___x_3540_, 1, v___x_3113_);
lean_ctor_set(v___x_3540_, 2, v___x_3539_);
v___x_3541_ = l_String_Slice_toString(v___x_3540_);
lean_dec_ref_known(v___x_3540_, 3);
v___y_3473_ = v___y_3524_;
v___y_3474_ = v_ppFail_3533_;
v___y_3475_ = v___y_3527_;
v___y_3476_ = v___y_3529_;
v___y_3477_ = v___y_3531_;
v___y_3478_ = v___y_3532_;
v___y_3479_ = v___x_3535_;
v___y_3480_ = v___y_3521_;
v___y_3481_ = v___y_3523_;
v___y_3482_ = v___y_3522_;
v___y_3483_ = v___y_3525_;
v___y_3484_ = v___y_3526_;
v___y_3485_ = v___x_3534_;
v___y_3486_ = v___x_3536_;
v___y_3487_ = v___y_3528_;
v_stmt_3488_ = v___x_3541_;
goto v___jp_3472_;
}
}
v___jp_3542_:
{
lean_object* v___x_3555_; lean_object* v___x_3556_; lean_object* v___x_3557_; 
v___x_3555_ = lean_box(v___y_3544_);
v___x_3556_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3556_, 0, v___y_3553_);
lean_ctor_set(v___x_3556_, 1, v___x_3555_);
lean_inc_ref(v_a_3047_);
v___x_3557_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16(v_a_3047_, v___x_3092_, v_shard_3045_, v___x_3167_, v_sz_3172_, v___x_3173_, v___x_3556_);
lean_dec(v___x_3092_);
if (lean_obj_tag(v___x_3557_) == 0)
{
lean_object* v_a_3558_; lean_object* v_snd_3559_; uint8_t v___x_3560_; 
v_a_3558_ = lean_ctor_get(v___x_3557_, 0);
lean_inc(v_a_3558_);
lean_dec_ref_known(v___x_3557_, 1);
v_snd_3559_ = lean_ctor_get(v_a_3558_, 1);
lean_inc(v_snd_3559_);
v___x_3560_ = lean_unbox(v_snd_3559_);
if (v___x_3560_ == 0)
{
lean_object* v_fst_3561_; lean_object* v___x_3562_; 
v_fst_3561_ = lean_ctor_get(v_a_3558_, 0);
lean_inc(v_fst_3561_);
lean_dec(v_a_3558_);
v___x_3562_ = lean_nat_add(v_fst_3076_, v___x_3090_);
lean_dec(v_fst_3076_);
v___y_3521_ = v___y_3543_;
v___y_3522_ = v___y_3545_;
v___y_3523_ = v___y_3554_;
v___y_3524_ = v___y_3546_;
v___y_3525_ = v___y_3547_;
v___y_3526_ = v_snd_3559_;
v___y_3527_ = v___y_3548_;
v___y_3528_ = v___y_3550_;
v___y_3529_ = v___y_3549_;
v___y_3530_ = v_fst_3561_;
v___y_3531_ = v___y_3551_;
v___y_3532_ = v___y_3552_;
v_ppFail_3533_ = v___x_3562_;
goto v___jp_3520_;
}
else
{
lean_object* v_fst_3563_; 
v_fst_3563_ = lean_ctor_get(v_a_3558_, 0);
lean_inc(v_fst_3563_);
lean_dec(v_a_3558_);
v___y_3521_ = v___y_3543_;
v___y_3522_ = v___y_3545_;
v___y_3523_ = v___y_3554_;
v___y_3524_ = v___y_3546_;
v___y_3525_ = v___y_3547_;
v___y_3526_ = v_snd_3559_;
v___y_3527_ = v___y_3548_;
v___y_3528_ = v___y_3550_;
v___y_3529_ = v___y_3549_;
v___y_3530_ = v_fst_3563_;
v___y_3531_ = v___y_3551_;
v___y_3532_ = v___y_3552_;
v_ppFail_3533_ = v_fst_3076_;
goto v___jp_3520_;
}
}
else
{
lean_object* v_a_3564_; lean_object* v___x_3566_; uint8_t v_isShared_3567_; uint8_t v_isSharedCheck_3571_; 
lean_dec_ref(v___y_3552_);
lean_dec(v___y_3551_);
lean_dec(v___y_3550_);
lean_dec_ref(v___y_3548_);
lean_dec_ref(v___y_3547_);
lean_dec_ref(v___y_3546_);
lean_dec_ref(v___y_3545_);
lean_dec(v___y_3543_);
lean_del_object(v___x_3184_);
lean_dec(v_snd_3182_);
lean_dec(v_fst_3181_);
lean_del_object(v___x_3179_);
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_dec(v_fst_3076_);
lean_del_object(v___x_3070_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3564_ = lean_ctor_get(v___x_3557_, 0);
v_isSharedCheck_3571_ = !lean_is_exclusive(v___x_3557_);
if (v_isSharedCheck_3571_ == 0)
{
v___x_3566_ = v___x_3557_;
v_isShared_3567_ = v_isSharedCheck_3571_;
goto v_resetjp_3565_;
}
else
{
lean_inc(v_a_3564_);
lean_dec(v___x_3557_);
v___x_3566_ = lean_box(0);
v_isShared_3567_ = v_isSharedCheck_3571_;
goto v_resetjp_3565_;
}
v_resetjp_3565_:
{
lean_object* v___x_3569_; 
if (v_isShared_3567_ == 0)
{
v___x_3569_ = v___x_3566_;
goto v_reusejp_3568_;
}
else
{
lean_object* v_reuseFailAlloc_3570_; 
v_reuseFailAlloc_3570_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3570_, 0, v_a_3564_);
v___x_3569_ = v_reuseFailAlloc_3570_;
goto v_reusejp_3568_;
}
v_reusejp_3568_:
{
return v___x_3569_;
}
}
}
}
v___jp_3572_:
{
lean_object* v___x_3585_; 
lean_inc_ref(v_a_3047_);
v___x_3585_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3113_, v___x_3090_, v___x_3462_, v___x_3093_, v_a_3047_, v___x_3467_, v___x_3463_, v___x_3464_, v___x_3468_, v___x_3469_, v___x_3470_, v___x_3471_, v___x_3393_, lean_box(0), v___y_3573_);
if (lean_obj_tag(v___x_3585_) == 0)
{
lean_object* v_a_3586_; 
v_a_3586_ = lean_ctor_get(v___x_3585_, 0);
lean_inc(v_a_3586_);
lean_dec_ref_known(v___x_3585_, 1);
if (lean_obj_tag(v_a_3586_) == 0)
{
v___y_3543_ = v___y_3574_;
v___y_3544_ = v_ppOk_3584_;
v___y_3545_ = v___y_3575_;
v___y_3546_ = v___y_3576_;
v___y_3547_ = v___y_3577_;
v___y_3548_ = v___y_3578_;
v___y_3549_ = v___y_3580_;
v___y_3550_ = v___y_3579_;
v___y_3551_ = v___y_3581_;
v___y_3552_ = v___y_3582_;
v___y_3553_ = v_stmt_3583_;
v___y_3554_ = v___x_3393_;
goto v___jp_3542_;
}
else
{
lean_object* v_val_3587_; uint8_t v___x_3588_; 
v_val_3587_ = lean_ctor_get(v_a_3586_, 0);
lean_inc(v_val_3587_);
lean_dec_ref_known(v_a_3586_, 1);
v___x_3588_ = lean_unbox(v_val_3587_);
lean_dec(v_val_3587_);
v___y_3543_ = v___y_3574_;
v___y_3544_ = v_ppOk_3584_;
v___y_3545_ = v___y_3575_;
v___y_3546_ = v___y_3576_;
v___y_3547_ = v___y_3577_;
v___y_3548_ = v___y_3578_;
v___y_3549_ = v___y_3580_;
v___y_3550_ = v___y_3579_;
v___y_3551_ = v___y_3581_;
v___y_3552_ = v___y_3582_;
v___y_3553_ = v_stmt_3583_;
v___y_3554_ = v___x_3588_;
goto v___jp_3542_;
}
}
else
{
lean_object* v_a_3589_; lean_object* v___x_3591_; uint8_t v_isShared_3592_; uint8_t v_isSharedCheck_3596_; 
lean_dec_ref(v_stmt_3583_);
lean_dec_ref(v___y_3582_);
lean_dec(v___y_3581_);
lean_dec(v___y_3579_);
lean_dec_ref(v___y_3578_);
lean_dec_ref(v___y_3577_);
lean_dec_ref(v___y_3576_);
lean_dec_ref(v___y_3575_);
lean_dec(v___y_3574_);
lean_del_object(v___x_3184_);
lean_dec(v_snd_3182_);
lean_dec(v_fst_3181_);
lean_del_object(v___x_3179_);
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec(v___x_3092_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_dec(v_fst_3076_);
lean_del_object(v___x_3070_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3589_ = lean_ctor_get(v___x_3585_, 0);
v_isSharedCheck_3596_ = !lean_is_exclusive(v___x_3585_);
if (v_isSharedCheck_3596_ == 0)
{
v___x_3591_ = v___x_3585_;
v_isShared_3592_ = v_isSharedCheck_3596_;
goto v_resetjp_3590_;
}
else
{
lean_inc(v_a_3589_);
lean_dec(v___x_3585_);
v___x_3591_ = lean_box(0);
v_isShared_3592_ = v_isSharedCheck_3596_;
goto v_resetjp_3590_;
}
v_resetjp_3590_:
{
lean_object* v___x_3594_; 
if (v_isShared_3592_ == 0)
{
v___x_3594_ = v___x_3591_;
goto v_reusejp_3593_;
}
else
{
lean_object* v_reuseFailAlloc_3595_; 
v_reuseFailAlloc_3595_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3595_, 0, v_a_3589_);
v___x_3594_ = v_reuseFailAlloc_3595_;
goto v_reusejp_3593_;
}
v_reusejp_3593_:
{
return v___x_3594_;
}
}
}
}
v___jp_3597_:
{
uint8_t v___x_3607_; uint8_t v___x_3608_; uint8_t v___x_3609_; lean_object* v___x_3610_; uint64_t v___x_3611_; lean_object* v___x_3612_; lean_object* v___x_3613_; lean_object* v___x_3614_; lean_object* v___x_3615_; lean_object* v___x_3616_; lean_object* v___f_3617_; lean_object* v___x_3618_; 
v___x_3607_ = 1;
v___x_3608_ = 0;
v___x_3609_ = 2;
v___x_3610_ = lean_alloc_ctor(0, 0, 20);
lean_ctor_set_uint8(v___x_3610_, 0, v___x_3393_);
lean_ctor_set_uint8(v___x_3610_, 1, v___x_3393_);
lean_ctor_set_uint8(v___x_3610_, 2, v___x_3393_);
lean_ctor_set_uint8(v___x_3610_, 3, v___x_3393_);
lean_ctor_set_uint8(v___x_3610_, 4, v___x_3393_);
lean_ctor_set_uint8(v___x_3610_, 5, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 6, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 7, v___x_3393_);
lean_ctor_set_uint8(v___x_3610_, 8, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 9, v___x_3607_);
lean_ctor_set_uint8(v___x_3610_, 10, v___x_3608_);
lean_ctor_set_uint8(v___x_3610_, 11, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 12, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 13, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 14, v___x_3609_);
lean_ctor_set_uint8(v___x_3610_, 15, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 16, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 17, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 18, v___x_3093_);
lean_ctor_set_uint8(v___x_3610_, 19, v___x_3393_);
v___x_3611_ = l___private_Lean_Meta_Basic_0__Lean_Meta_Config_toKey(v___x_3610_);
v___x_3612_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_3612_, 0, v___x_3610_);
lean_ctor_set_uint64(v___x_3612_, sizeof(void*)*1, v___x_3611_);
v___x_3613_ = lean_box(1);
v___x_3614_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4);
v___x_3615_ = lean_alloc_ctor(0, 7, 4);
lean_ctor_set(v___x_3615_, 0, v___x_3612_);
lean_ctor_set(v___x_3615_, 1, v___x_3613_);
lean_ctor_set(v___x_3615_, 2, v___x_3614_);
lean_ctor_set(v___x_3615_, 3, v___x_3166_);
lean_ctor_set(v___x_3615_, 4, v___x_3471_);
lean_ctor_set(v___x_3615_, 5, v___x_3113_);
lean_ctor_set(v___x_3615_, 6, v___x_3471_);
lean_ctor_set_uint8(v___x_3615_, sizeof(void*)*7, v___x_3393_);
lean_ctor_set_uint8(v___x_3615_, sizeof(void*)*7 + 1, v___x_3393_);
lean_ctor_set_uint8(v___x_3615_, sizeof(void*)*7 + 2, v___x_3393_);
lean_ctor_set_uint8(v___x_3615_, sizeof(void*)*7 + 3, v___x_3093_);
v___x_3616_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16);
lean_inc_ref(v___x_3615_);
lean_inc(v_fst_3067_);
v___f_3617_ = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__2___boxed), 8, 5);
lean_closure_set(v___f_3617_, 0, v___x_3616_);
lean_closure_set(v___f_3617_, 1, v___x_3466_);
lean_closure_set(v___f_3617_, 2, v___x_3113_);
lean_closure_set(v___f_3617_, 3, v_fst_3067_);
lean_closure_set(v___f_3617_, 4, v___x_3615_);
lean_inc_ref(v_a_3047_);
v___x_3618_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3113_, v___x_3090_, v___x_3462_, v___x_3093_, v_a_3047_, v___x_3467_, v___x_3463_, v___x_3464_, v___x_3468_, v___x_3469_, v___x_3470_, v___x_3471_, v___x_3393_, lean_box(0), v___f_3617_);
if (lean_obj_tag(v___x_3618_) == 0)
{
lean_object* v_a_3619_; lean_object* v___f_3620_; 
v_a_3619_ = lean_ctor_get(v___x_3618_, 0);
lean_inc(v_a_3619_);
lean_dec_ref_known(v___x_3618_, 1);
lean_inc_ref(v___x_3615_);
lean_inc_ref(v___x_3101_);
v___f_3620_ = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__3___boxed), 6, 3);
lean_closure_set(v___f_3620_, 0, v___x_3616_);
lean_closure_set(v___f_3620_, 1, v___x_3101_);
lean_closure_set(v___f_3620_, 2, v___x_3615_);
if (lean_obj_tag(v_a_3619_) == 0)
{
lean_object* v___f_3621_; lean_object* v___x_3622_; 
v___f_3621_ = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__4___boxed), 8, 5);
lean_closure_set(v___f_3621_, 0, v___x_3616_);
lean_closure_set(v___f_3621_, 1, v___x_3466_);
lean_closure_set(v___f_3621_, 2, v___x_3113_);
lean_closure_set(v___f_3621_, 3, v___x_3101_);
lean_closure_set(v___f_3621_, 4, v___x_3615_);
lean_inc_ref(v_a_3047_);
v___x_3622_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3113_, v___x_3090_, v___x_3462_, v___x_3093_, v_a_3047_, v___x_3467_, v___x_3463_, v___x_3464_, v___x_3468_, v___x_3469_, v___x_3470_, v___x_3471_, v___x_3393_, lean_box(0), v___f_3621_);
if (lean_obj_tag(v___x_3622_) == 0)
{
lean_object* v_a_3623_; 
v_a_3623_ = lean_ctor_get(v___x_3622_, 0);
lean_inc(v_a_3623_);
lean_dec_ref_known(v___x_3622_, 1);
if (lean_obj_tag(v_a_3623_) == 0)
{
lean_object* v___x_3624_; 
v___x_3624_ = ((lean_object*)(l_NsExport_hexOf___closed__0));
v___y_3573_ = v___f_3620_;
v___y_3574_ = v___y_3598_;
v___y_3575_ = v___y_3599_;
v___y_3576_ = v___y_3600_;
v___y_3577_ = v___y_3601_;
v___y_3578_ = v___y_3602_;
v___y_3579_ = v___y_3603_;
v___y_3580_ = v___y_3606_;
v___y_3581_ = v___y_3604_;
v___y_3582_ = v___y_3605_;
v_stmt_3583_ = v___x_3624_;
v_ppOk_3584_ = v___x_3393_;
goto v___jp_3572_;
}
else
{
lean_object* v_val_3625_; 
v_val_3625_ = lean_ctor_get(v_a_3623_, 0);
lean_inc(v_val_3625_);
lean_dec_ref_known(v_a_3623_, 1);
v___y_3573_ = v___f_3620_;
v___y_3574_ = v___y_3598_;
v___y_3575_ = v___y_3599_;
v___y_3576_ = v___y_3600_;
v___y_3577_ = v___y_3601_;
v___y_3578_ = v___y_3602_;
v___y_3579_ = v___y_3603_;
v___y_3580_ = v___y_3606_;
v___y_3581_ = v___y_3604_;
v___y_3582_ = v___y_3605_;
v_stmt_3583_ = v_val_3625_;
v_ppOk_3584_ = v___x_3093_;
goto v___jp_3572_;
}
}
else
{
lean_object* v_a_3626_; lean_object* v___x_3628_; uint8_t v_isShared_3629_; uint8_t v_isSharedCheck_3633_; 
lean_dec_ref(v___f_3620_);
lean_dec_ref(v___y_3605_);
lean_dec(v___y_3604_);
lean_dec(v___y_3603_);
lean_dec_ref(v___y_3602_);
lean_dec_ref(v___y_3601_);
lean_dec_ref(v___y_3600_);
lean_dec_ref(v___y_3599_);
lean_dec(v___y_3598_);
lean_del_object(v___x_3184_);
lean_dec(v_snd_3182_);
lean_dec(v_fst_3181_);
lean_del_object(v___x_3179_);
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec(v___x_3092_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_dec(v_fst_3076_);
lean_del_object(v___x_3070_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3626_ = lean_ctor_get(v___x_3622_, 0);
v_isSharedCheck_3633_ = !lean_is_exclusive(v___x_3622_);
if (v_isSharedCheck_3633_ == 0)
{
v___x_3628_ = v___x_3622_;
v_isShared_3629_ = v_isSharedCheck_3633_;
goto v_resetjp_3627_;
}
else
{
lean_inc(v_a_3626_);
lean_dec(v___x_3622_);
v___x_3628_ = lean_box(0);
v_isShared_3629_ = v_isSharedCheck_3633_;
goto v_resetjp_3627_;
}
v_resetjp_3627_:
{
lean_object* v___x_3631_; 
if (v_isShared_3629_ == 0)
{
v___x_3631_ = v___x_3628_;
goto v_reusejp_3630_;
}
else
{
lean_object* v_reuseFailAlloc_3632_; 
v_reuseFailAlloc_3632_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3632_, 0, v_a_3626_);
v___x_3631_ = v_reuseFailAlloc_3632_;
goto v_reusejp_3630_;
}
v_reusejp_3630_:
{
return v___x_3631_;
}
}
}
}
else
{
lean_object* v_val_3634_; 
lean_dec_ref_known(v___x_3615_, 7);
lean_dec_ref(v___x_3101_);
v_val_3634_ = lean_ctor_get(v_a_3619_, 0);
lean_inc(v_val_3634_);
lean_dec_ref_known(v_a_3619_, 1);
v___y_3573_ = v___f_3620_;
v___y_3574_ = v___y_3598_;
v___y_3575_ = v___y_3599_;
v___y_3576_ = v___y_3600_;
v___y_3577_ = v___y_3601_;
v___y_3578_ = v___y_3602_;
v___y_3579_ = v___y_3603_;
v___y_3580_ = v___y_3606_;
v___y_3581_ = v___y_3604_;
v___y_3582_ = v___y_3605_;
v_stmt_3583_ = v_val_3634_;
v_ppOk_3584_ = v___x_3093_;
goto v___jp_3572_;
}
}
else
{
lean_object* v_a_3635_; lean_object* v___x_3637_; uint8_t v_isShared_3638_; uint8_t v_isSharedCheck_3642_; 
lean_dec_ref_known(v___x_3615_, 7);
lean_dec_ref(v___y_3605_);
lean_dec(v___y_3604_);
lean_dec(v___y_3603_);
lean_dec_ref(v___y_3602_);
lean_dec_ref(v___y_3601_);
lean_dec_ref(v___y_3600_);
lean_dec_ref(v___y_3599_);
lean_dec(v___y_3598_);
lean_del_object(v___x_3184_);
lean_dec(v_snd_3182_);
lean_dec(v_fst_3181_);
lean_del_object(v___x_3179_);
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec_ref(v___x_3101_);
lean_dec(v___x_3092_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_dec(v_fst_3076_);
lean_del_object(v___x_3070_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3635_ = lean_ctor_get(v___x_3618_, 0);
v_isSharedCheck_3642_ = !lean_is_exclusive(v___x_3618_);
if (v_isSharedCheck_3642_ == 0)
{
v___x_3637_ = v___x_3618_;
v_isShared_3638_ = v_isSharedCheck_3642_;
goto v_resetjp_3636_;
}
else
{
lean_inc(v_a_3635_);
lean_dec(v___x_3618_);
v___x_3637_ = lean_box(0);
v_isShared_3638_ = v_isSharedCheck_3642_;
goto v_resetjp_3636_;
}
v_resetjp_3636_:
{
lean_object* v___x_3640_; 
if (v_isShared_3638_ == 0)
{
v___x_3640_ = v___x_3637_;
goto v_reusejp_3639_;
}
else
{
lean_object* v_reuseFailAlloc_3641_; 
v_reuseFailAlloc_3641_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3641_, 0, v_a_3635_);
v___x_3640_ = v_reuseFailAlloc_3641_;
goto v_reusejp_3639_;
}
v_reusejp_3639_:
{
return v___x_3640_;
}
}
}
}
v___jp_3643_:
{
lean_object* v___x_3652_; 
v___x_3652_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__38));
v___y_3598_ = v___y_3644_;
v___y_3599_ = v___y_3645_;
v___y_3600_ = v___y_3646_;
v___y_3601_ = v___y_3647_;
v___y_3602_ = v___y_3648_;
v___y_3603_ = v___y_3649_;
v___y_3604_ = v___y_3650_;
v___y_3605_ = v___y_3651_;
v___y_3606_ = v___x_3652_;
goto v___jp_3597_;
}
v___jp_3653_:
{
lean_object* v___x_3657_; lean_object* v___x_3658_; size_t v_sz_3659_; lean_object* v___x_3660_; 
v___x_3657_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(v___x_3048_, v_fst_3067_, v___x_3166_);
v___x_3658_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3658_, 0, v_valConsts_3654_);
lean_ctor_set(v___x_3658_, 1, v___x_3113_);
v_sz_3659_ = lean_array_size(v___x_3657_);
lean_inc_ref(v_a_3047_);
v___x_3660_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__15(v_a_3047_, v___x_3657_, v_sz_3659_, v___x_3173_, v___x_3658_);
if (lean_obj_tag(v___x_3660_) == 0)
{
lean_object* v_a_3661_; lean_object* v___x_3662_; lean_object* v_fst_3663_; lean_object* v_snd_3664_; lean_object* v_fst_3665_; lean_object* v_snd_3666_; lean_object* v___x_3667_; 
v_a_3661_ = lean_ctor_get(v___x_3660_, 0);
lean_inc(v_a_3661_);
lean_dec_ref_known(v___x_3660_, 1);
lean_inc_n(v_fst_3067_, 2);
lean_inc_ref_n(v___x_3049_, 2);
v___x_3662_ = l_NsExport_resolveDeps(v___x_3049_, v_fst_3067_, v_fst_3177_);
v_fst_3663_ = lean_ctor_get(v___x_3662_, 0);
lean_inc(v_fst_3663_);
v_snd_3664_ = lean_ctor_get(v___x_3662_, 1);
lean_inc(v_snd_3664_);
lean_dec_ref(v___x_3662_);
v_fst_3665_ = lean_ctor_get(v_a_3661_, 0);
lean_inc(v_fst_3665_);
v_snd_3666_ = lean_ctor_get(v_a_3661_, 1);
lean_inc(v_snd_3666_);
lean_dec(v_a_3661_);
v___x_3667_ = l_NsExport_resolveDeps(v___x_3049_, v_fst_3067_, v_fst_3665_);
switch(lean_obj_tag(v_snd_3068_))
{
case 0:
{
lean_object* v_fst_3668_; lean_object* v_snd_3669_; lean_object* v___x_3670_; 
lean_dec_ref_known(v_snd_3068_, 1);
v_fst_3668_ = lean_ctor_get(v___x_3667_, 0);
lean_inc(v_fst_3668_);
v_snd_3669_ = lean_ctor_get(v___x_3667_, 1);
lean_inc(v_snd_3669_);
lean_dec_ref(v___x_3667_);
v___x_3670_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__39));
v___y_3598_ = v_proofTree_3656_;
v___y_3599_ = v_fst_3668_;
v___y_3600_ = v_fst_3663_;
v___y_3601_ = v___x_3657_;
v___y_3602_ = v_snd_3664_;
v___y_3603_ = v_proofSize_3655_;
v___y_3604_ = v_snd_3666_;
v___y_3605_ = v_snd_3669_;
v___y_3606_ = v___x_3670_;
goto v___jp_3597_;
}
case 2:
{
lean_object* v_fst_3671_; lean_object* v_snd_3672_; lean_object* v___x_3673_; 
lean_dec_ref_known(v_snd_3068_, 1);
v_fst_3671_ = lean_ctor_get(v___x_3667_, 0);
lean_inc(v_fst_3671_);
v_snd_3672_ = lean_ctor_get(v___x_3667_, 1);
lean_inc(v_snd_3672_);
lean_dec_ref(v___x_3667_);
v___x_3673_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__40));
v___y_3598_ = v_proofTree_3656_;
v___y_3599_ = v_fst_3671_;
v___y_3600_ = v_fst_3663_;
v___y_3601_ = v___x_3657_;
v___y_3602_ = v_snd_3664_;
v___y_3603_ = v_proofSize_3655_;
v___y_3604_ = v_snd_3666_;
v___y_3605_ = v_snd_3672_;
v___y_3606_ = v___x_3673_;
goto v___jp_3597_;
}
case 3:
{
lean_object* v_fst_3674_; lean_object* v_snd_3675_; lean_object* v___x_3676_; 
lean_dec_ref_known(v_snd_3068_, 1);
v_fst_3674_ = lean_ctor_get(v___x_3667_, 0);
lean_inc(v_fst_3674_);
v_snd_3675_ = lean_ctor_get(v___x_3667_, 1);
lean_inc(v_snd_3675_);
lean_dec_ref(v___x_3667_);
v___x_3676_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__41));
v___y_3598_ = v_proofTree_3656_;
v___y_3599_ = v_fst_3674_;
v___y_3600_ = v_fst_3663_;
v___y_3601_ = v___x_3657_;
v___y_3602_ = v_snd_3664_;
v___y_3603_ = v_proofSize_3655_;
v___y_3604_ = v_snd_3666_;
v___y_3605_ = v_snd_3675_;
v___y_3606_ = v___x_3676_;
goto v___jp_3597_;
}
case 1:
{
lean_object* v_fst_3677_; lean_object* v_snd_3678_; uint8_t v___x_3679_; 
lean_dec_ref_known(v_snd_3068_, 1);
v_fst_3677_ = lean_ctor_get(v___x_3667_, 0);
lean_inc(v_fst_3677_);
v_snd_3678_ = lean_ctor_get(v___x_3667_, 1);
lean_inc(v_snd_3678_);
lean_dec_ref(v___x_3667_);
lean_inc_ref(v_a_3047_);
v___x_3679_ = l_Lean_Meta_isInstanceCore(v_a_3047_, v_fst_3067_);
if (v___x_3679_ == 0)
{
lean_object* v___x_3680_; lean_object* v___x_3681_; lean_object* v___x_3682_; uint8_t v___x_3683_; 
v___x_3680_ = l_Lean_Expr_getForallBody(v___x_3101_);
v___x_3681_ = l_Lean_Expr_getAppFn(v___x_3680_);
lean_dec_ref(v___x_3680_);
v___x_3682_ = l_Lean_Expr_constName(v___x_3681_);
lean_dec_ref(v___x_3681_);
lean_inc_ref(v_a_3047_);
v___x_3683_ = l_Lean_isClass(v_a_3047_, v___x_3682_);
lean_dec(v___x_3682_);
if (v___x_3683_ == 0)
{
lean_object* v___x_3684_; 
v___x_3684_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__42));
v___y_3598_ = v_proofTree_3656_;
v___y_3599_ = v_fst_3677_;
v___y_3600_ = v_fst_3663_;
v___y_3601_ = v___x_3657_;
v___y_3602_ = v_snd_3664_;
v___y_3603_ = v_proofSize_3655_;
v___y_3604_ = v_snd_3666_;
v___y_3605_ = v_snd_3678_;
v___y_3606_ = v___x_3684_;
goto v___jp_3597_;
}
else
{
v___y_3644_ = v_proofTree_3656_;
v___y_3645_ = v_fst_3677_;
v___y_3646_ = v_fst_3663_;
v___y_3647_ = v___x_3657_;
v___y_3648_ = v_snd_3664_;
v___y_3649_ = v_proofSize_3655_;
v___y_3650_ = v_snd_3666_;
v___y_3651_ = v_snd_3678_;
goto v___jp_3643_;
}
}
else
{
v___y_3644_ = v_proofTree_3656_;
v___y_3645_ = v_fst_3677_;
v___y_3646_ = v_fst_3663_;
v___y_3647_ = v___x_3657_;
v___y_3648_ = v_snd_3664_;
v___y_3649_ = v_proofSize_3655_;
v___y_3650_ = v_snd_3666_;
v___y_3651_ = v_snd_3678_;
goto v___jp_3643_;
}
}
case 5:
{
lean_object* v_fst_3685_; lean_object* v_snd_3686_; uint8_t v___x_3687_; 
lean_dec_ref_known(v_snd_3068_, 1);
v_fst_3685_ = lean_ctor_get(v___x_3667_, 0);
lean_inc(v_fst_3685_);
v_snd_3686_ = lean_ctor_get(v___x_3667_, 1);
lean_inc(v_snd_3686_);
lean_dec_ref(v___x_3667_);
lean_inc(v_fst_3067_);
lean_inc_ref(v_a_3047_);
v___x_3687_ = l_Lean_isStructure(v_a_3047_, v_fst_3067_);
if (v___x_3687_ == 0)
{
lean_object* v___x_3688_; 
v___x_3688_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__43));
v___y_3598_ = v_proofTree_3656_;
v___y_3599_ = v_fst_3685_;
v___y_3600_ = v_fst_3663_;
v___y_3601_ = v___x_3657_;
v___y_3602_ = v_snd_3664_;
v___y_3603_ = v_proofSize_3655_;
v___y_3604_ = v_snd_3666_;
v___y_3605_ = v_snd_3686_;
v___y_3606_ = v___x_3688_;
goto v___jp_3597_;
}
else
{
lean_object* v___x_3689_; 
v___x_3689_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__44));
v___y_3598_ = v_proofTree_3656_;
v___y_3599_ = v_fst_3685_;
v___y_3600_ = v_fst_3663_;
v___y_3601_ = v___x_3657_;
v___y_3602_ = v_snd_3664_;
v___y_3603_ = v_proofSize_3655_;
v___y_3604_ = v_snd_3666_;
v___y_3605_ = v_snd_3686_;
v___y_3606_ = v___x_3689_;
goto v___jp_3597_;
}
}
default: 
{
lean_object* v_fst_3690_; lean_object* v_snd_3691_; lean_object* v___x_3692_; 
lean_dec(v_snd_3068_);
v_fst_3690_ = lean_ctor_get(v___x_3667_, 0);
lean_inc(v_fst_3690_);
v_snd_3691_ = lean_ctor_get(v___x_3667_, 1);
lean_inc(v_snd_3691_);
lean_dec_ref(v___x_3667_);
v___x_3692_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__45));
v___y_3598_ = v_proofTree_3656_;
v___y_3599_ = v_fst_3690_;
v___y_3600_ = v_fst_3663_;
v___y_3601_ = v___x_3657_;
v___y_3602_ = v_snd_3664_;
v___y_3603_ = v_proofSize_3655_;
v___y_3604_ = v_snd_3666_;
v___y_3605_ = v_snd_3691_;
v___y_3606_ = v___x_3692_;
goto v___jp_3597_;
}
}
}
else
{
lean_object* v_a_3693_; lean_object* v___x_3695_; uint8_t v_isShared_3696_; uint8_t v_isSharedCheck_3700_; 
lean_dec(v___x_3657_);
lean_dec(v_proofTree_3656_);
lean_dec(v_proofSize_3655_);
lean_del_object(v___x_3184_);
lean_dec(v_snd_3182_);
lean_dec(v_fst_3181_);
lean_del_object(v___x_3179_);
lean_dec(v_fst_3177_);
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec_ref(v___x_3101_);
lean_dec(v___x_3092_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_dec(v_fst_3076_);
lean_del_object(v___x_3070_);
lean_dec(v_snd_3068_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3693_ = lean_ctor_get(v___x_3660_, 0);
v_isSharedCheck_3700_ = !lean_is_exclusive(v___x_3660_);
if (v_isSharedCheck_3700_ == 0)
{
v___x_3695_ = v___x_3660_;
v_isShared_3696_ = v_isSharedCheck_3700_;
goto v_resetjp_3694_;
}
else
{
lean_inc(v_a_3693_);
lean_dec(v___x_3660_);
v___x_3695_ = lean_box(0);
v_isShared_3696_ = v_isSharedCheck_3700_;
goto v_resetjp_3694_;
}
v_resetjp_3694_:
{
lean_object* v___x_3698_; 
if (v_isShared_3696_ == 0)
{
v___x_3698_ = v___x_3695_;
goto v_reusejp_3697_;
}
else
{
lean_object* v_reuseFailAlloc_3699_; 
v_reuseFailAlloc_3699_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3699_, 0, v_a_3693_);
v___x_3698_ = v_reuseFailAlloc_3699_;
goto v_reusejp_3697_;
}
v_reusejp_3697_:
{
return v___x_3698_;
}
}
}
}
}
}
}
else
{
lean_object* v_a_3710_; lean_object* v___x_3712_; uint8_t v_isShared_3713_; uint8_t v_isSharedCheck_3717_; 
lean_dec(v___x_3167_);
lean_del_object(v___x_3111_);
lean_dec(v_snd_3109_);
lean_del_object(v___x_3106_);
lean_dec_ref(v___x_3101_);
lean_dec(v___x_3100_);
lean_dec(v___x_3092_);
lean_dec(v___x_3091_);
lean_dec(v_snd_3077_);
lean_dec(v_fst_3076_);
lean_del_object(v___x_3070_);
lean_dec(v_snd_3068_);
lean_dec(v_fst_3067_);
lean_dec_ref(v___x_3051_);
lean_dec_ref(v___x_3049_);
lean_dec_ref(v_a_3047_);
v_a_3710_ = lean_ctor_get(v___x_3174_, 0);
v_isSharedCheck_3717_ = !lean_is_exclusive(v___x_3174_);
if (v_isSharedCheck_3717_ == 0)
{
v___x_3712_ = v___x_3174_;
v_isShared_3713_ = v_isSharedCheck_3717_;
goto v_resetjp_3711_;
}
else
{
lean_inc(v_a_3710_);
lean_dec(v___x_3174_);
v___x_3712_ = lean_box(0);
v_isShared_3713_ = v_isSharedCheck_3717_;
goto v_resetjp_3711_;
}
v_resetjp_3711_:
{
lean_object* v___x_3715_; 
if (v_isShared_3713_ == 0)
{
v___x_3715_ = v___x_3712_;
goto v_reusejp_3714_;
}
else
{
lean_object* v_reuseFailAlloc_3716_; 
v_reuseFailAlloc_3716_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3716_, 0, v_a_3710_);
v___x_3715_ = v_reuseFailAlloc_3716_;
goto v_reusejp_3714_;
}
v_reusejp_3714_:
{
return v___x_3715_;
}
}
}
}
}
}
}
}
}
}
}
}
}
v___jp_3058_:
{
size_t v___x_3060_; size_t v___x_3061_; 
v___x_3060_ = ((size_t)1ULL);
v___x_3061_ = lean_usize_add(v_i_3055_, v___x_3060_);
v_i_3055_ = v___x_3061_;
v_b_3056_ = v_a_3059_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___boxed(lean_object* v_a_3726_, lean_object* v_nshards_3727_, lean_object* v_shard_3728_, lean_object* v___x_3729_, lean_object* v_a_3730_, lean_object* v___x_3731_, lean_object* v___x_3732_, lean_object* v_a_3733_, lean_object* v___x_3734_, lean_object* v_a_3735_, lean_object* v_as_3736_, lean_object* v_sz_3737_, lean_object* v_i_3738_, lean_object* v_b_3739_, lean_object* v___y_3740_){
_start:
{
size_t v_sz_boxed_3741_; size_t v_i_boxed_3742_; lean_object* v_res_3743_; 
v_sz_boxed_3741_ = lean_unbox_usize(v_sz_3737_);
lean_dec(v_sz_3737_);
v_i_boxed_3742_ = lean_unbox_usize(v_i_3738_);
lean_dec(v_i_3738_);
v_res_3743_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23(v_a_3726_, v_nshards_3727_, v_shard_3728_, v___x_3729_, v_a_3730_, v___x_3731_, v___x_3732_, v_a_3733_, v___x_3734_, v_a_3735_, v_as_3736_, v_sz_boxed_3741_, v_i_boxed_3742_, v_b_3739_);
lean_dec_ref(v_as_3736_);
lean_dec(v_a_3735_);
lean_dec(v_a_3733_);
lean_dec_ref(v___x_3731_);
lean_dec_ref(v___x_3729_);
lean_dec(v_shard_3728_);
lean_dec(v_nshards_3727_);
lean_dec_ref(v_a_3726_);
return v_res_3743_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17(lean_object* v_a_3744_, lean_object* v_nshards_3745_, lean_object* v_shard_3746_, lean_object* v_a_3747_, lean_object* v___x_3748_, lean_object* v___x_3749_, lean_object* v___x_3750_, lean_object* v_a_3751_, lean_object* v___x_3752_, lean_object* v_a_3753_, lean_object* v_as_3754_, size_t v_sz_3755_, size_t v_i_3756_, lean_object* v_b_3757_){
_start:
{
lean_object* v_a_3760_; uint8_t v___x_3764_; 
v___x_3764_ = lean_usize_dec_lt(v_i_3756_, v_sz_3755_);
if (v___x_3764_ == 0)
{
lean_object* v___x_3765_; 
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v___x_3765_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_3765_, 0, v_b_3757_);
return v___x_3765_;
}
else
{
lean_object* v_a_3766_; lean_object* v_snd_3767_; lean_object* v_fst_3768_; lean_object* v_snd_3769_; lean_object* v___x_3771_; uint8_t v_isShared_3772_; uint8_t v_isSharedCheck_4428_; 
v_a_3766_ = lean_array_uget(v_as_3754_, v_i_3756_);
v_snd_3767_ = lean_ctor_get(v_b_3757_, 1);
lean_inc(v_snd_3767_);
v_fst_3768_ = lean_ctor_get(v_a_3766_, 0);
v_snd_3769_ = lean_ctor_get(v_a_3766_, 1);
v_isSharedCheck_4428_ = !lean_is_exclusive(v_a_3766_);
if (v_isSharedCheck_4428_ == 0)
{
v___x_3771_ = v_a_3766_;
v_isShared_3772_ = v_isSharedCheck_4428_;
goto v_resetjp_3770_;
}
else
{
lean_inc(v_snd_3769_);
lean_inc(v_fst_3768_);
lean_dec(v_a_3766_);
v___x_3771_ = lean_box(0);
v_isShared_3772_ = v_isSharedCheck_4428_;
goto v_resetjp_3770_;
}
v_resetjp_3770_:
{
lean_object* v_fst_3773_; lean_object* v___x_3775_; uint8_t v_isShared_3776_; uint8_t v_isSharedCheck_4426_; 
v_fst_3773_ = lean_ctor_get(v_b_3757_, 0);
v_isSharedCheck_4426_ = !lean_is_exclusive(v_b_3757_);
if (v_isSharedCheck_4426_ == 0)
{
lean_object* v_unused_4427_; 
v_unused_4427_ = lean_ctor_get(v_b_3757_, 1);
lean_dec(v_unused_4427_);
v___x_3775_ = v_b_3757_;
v_isShared_3776_ = v_isSharedCheck_4426_;
goto v_resetjp_3774_;
}
else
{
lean_inc(v_fst_3773_);
lean_dec(v_b_3757_);
v___x_3775_ = lean_box(0);
v_isShared_3776_ = v_isSharedCheck_4426_;
goto v_resetjp_3774_;
}
v_resetjp_3774_:
{
lean_object* v_fst_3777_; lean_object* v_snd_3778_; lean_object* v___x_3780_; uint8_t v_isShared_3781_; uint8_t v_isSharedCheck_4425_; 
v_fst_3777_ = lean_ctor_get(v_snd_3767_, 0);
v_snd_3778_ = lean_ctor_get(v_snd_3767_, 1);
v_isSharedCheck_4425_ = !lean_is_exclusive(v_snd_3767_);
if (v_isSharedCheck_4425_ == 0)
{
v___x_3780_ = v_snd_3767_;
v_isShared_3781_ = v_isSharedCheck_4425_;
goto v_resetjp_3779_;
}
else
{
lean_inc(v_snd_3778_);
lean_inc(v_fst_3777_);
lean_dec(v_snd_3767_);
v___x_3780_ = lean_box(0);
v_isShared_3781_ = v_isSharedCheck_4425_;
goto v_resetjp_3779_;
}
v_resetjp_3779_:
{
lean_object* v___x_3782_; lean_object* v___x_3783_; uint8_t v___x_3784_; 
v___x_3782_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_a_3744_, v_fst_3768_);
v___x_3783_ = lean_box(0);
v___x_3784_ = l_NsExport_instBEqCls_beq(v___x_3782_, v___x_3783_);
lean_dec(v___x_3782_);
if (v___x_3784_ == 0)
{
lean_object* v___x_3786_; 
lean_del_object(v___x_3771_);
lean_dec(v_snd_3769_);
lean_dec(v_fst_3768_);
if (v_isShared_3781_ == 0)
{
v___x_3786_ = v___x_3780_;
goto v_reusejp_3785_;
}
else
{
lean_object* v_reuseFailAlloc_3790_; 
v_reuseFailAlloc_3790_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3790_, 0, v_fst_3777_);
lean_ctor_set(v_reuseFailAlloc_3790_, 1, v_snd_3778_);
v___x_3786_ = v_reuseFailAlloc_3790_;
goto v_reusejp_3785_;
}
v_reusejp_3785_:
{
lean_object* v___x_3788_; 
if (v_isShared_3776_ == 0)
{
lean_ctor_set(v___x_3775_, 1, v___x_3786_);
v___x_3788_ = v___x_3775_;
goto v_reusejp_3787_;
}
else
{
lean_object* v_reuseFailAlloc_3789_; 
v_reuseFailAlloc_3789_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3789_, 0, v_fst_3773_);
lean_ctor_set(v_reuseFailAlloc_3789_, 1, v___x_3786_);
v___x_3788_ = v_reuseFailAlloc_3789_;
goto v_reusejp_3787_;
}
v_reusejp_3787_:
{
v_a_3760_ = v___x_3788_;
goto v___jp_3759_;
}
}
}
else
{
lean_object* v___x_3791_; lean_object* v___x_3792_; lean_object* v___x_3793_; uint8_t v___x_3794_; 
v___x_3791_ = lean_unsigned_to_nat(1u);
v___x_3792_ = lean_nat_add(v_fst_3773_, v___x_3791_);
lean_dec(v_fst_3773_);
v___x_3793_ = lean_nat_mod(v___x_3792_, v_nshards_3745_);
v___x_3794_ = lean_nat_dec_eq(v___x_3793_, v_shard_3746_);
if (v___x_3794_ == 0)
{
lean_object* v___x_3796_; 
lean_dec(v___x_3793_);
lean_del_object(v___x_3771_);
lean_dec(v_snd_3769_);
lean_dec(v_fst_3768_);
if (v_isShared_3781_ == 0)
{
v___x_3796_ = v___x_3780_;
goto v_reusejp_3795_;
}
else
{
lean_object* v_reuseFailAlloc_3800_; 
v_reuseFailAlloc_3800_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3800_, 0, v_fst_3777_);
lean_ctor_set(v_reuseFailAlloc_3800_, 1, v_snd_3778_);
v___x_3796_ = v_reuseFailAlloc_3800_;
goto v_reusejp_3795_;
}
v_reusejp_3795_:
{
lean_object* v___x_3798_; 
if (v_isShared_3776_ == 0)
{
lean_ctor_set(v___x_3775_, 1, v___x_3796_);
lean_ctor_set(v___x_3775_, 0, v___x_3792_);
v___x_3798_ = v___x_3775_;
goto v_reusejp_3797_;
}
else
{
lean_object* v_reuseFailAlloc_3799_; 
v_reuseFailAlloc_3799_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3799_, 0, v___x_3792_);
lean_ctor_set(v_reuseFailAlloc_3799_, 1, v___x_3796_);
v___x_3798_ = v_reuseFailAlloc_3799_;
goto v_reusejp_3797_;
}
v_reusejp_3797_:
{
v_a_3760_ = v___x_3798_;
goto v___jp_3759_;
}
}
}
else
{
lean_object* v___x_3801_; lean_object* v___x_3802_; lean_object* v___x_3803_; lean_object* v_snd_3804_; lean_object* v_fst_3805_; lean_object* v___x_3807_; uint8_t v_isShared_3808_; uint8_t v_isSharedCheck_4424_; 
v___x_3801_ = l_Lean_ConstantInfo_levelParams(v_snd_3769_);
v___x_3802_ = l_Lean_ConstantInfo_type(v_snd_3769_);
lean_inc_ref(v___x_3802_);
v___x_3803_ = l_NsExport_sizes(v___x_3801_, v___x_3802_);
v_snd_3804_ = lean_ctor_get(v___x_3803_, 1);
v_fst_3805_ = lean_ctor_get(v___x_3803_, 0);
v_isSharedCheck_4424_ = !lean_is_exclusive(v___x_3803_);
if (v_isSharedCheck_4424_ == 0)
{
v___x_3807_ = v___x_3803_;
v_isShared_3808_ = v_isSharedCheck_4424_;
goto v_resetjp_3806_;
}
else
{
lean_inc(v_snd_3804_);
lean_inc(v_fst_3805_);
lean_dec(v___x_3803_);
v___x_3807_ = lean_box(0);
v_isShared_3808_ = v_isSharedCheck_4424_;
goto v_resetjp_3806_;
}
v_resetjp_3806_:
{
lean_object* v_fst_3809_; lean_object* v_snd_3810_; lean_object* v___x_3812_; uint8_t v_isShared_3813_; uint8_t v_isSharedCheck_4423_; 
v_fst_3809_ = lean_ctor_get(v_snd_3804_, 0);
v_snd_3810_ = lean_ctor_get(v_snd_3804_, 1);
v_isSharedCheck_4423_ = !lean_is_exclusive(v_snd_3804_);
if (v_isSharedCheck_4423_ == 0)
{
v___x_3812_ = v_snd_3804_;
v_isShared_3813_ = v_isSharedCheck_4423_;
goto v_resetjp_3811_;
}
else
{
lean_inc(v_snd_3810_);
lean_inc(v_fst_3809_);
lean_dec(v_snd_3804_);
v___x_3812_ = lean_box(0);
v_isShared_3813_ = v_isSharedCheck_4423_;
goto v_resetjp_3811_;
}
v_resetjp_3811_:
{
lean_object* v___x_3814_; lean_object* v___y_3816_; lean_object* v___y_3817_; lean_object* v_fields_3818_; lean_object* v___x_3866_; lean_object* v___x_3867_; lean_object* v___x_3868_; lean_object* v___x_3870_; 
v___x_3814_ = lean_unsigned_to_nat(0u);
lean_inc_ref(v___x_3802_);
v___x_3866_ = l_Lean_Expr_getUsedConstants(v___x_3802_);
v___x_3867_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13___closed__0));
v___x_3868_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(v___x_3748_, v_fst_3768_, v___x_3867_);
if (v_isShared_3781_ == 0)
{
lean_ctor_set(v___x_3780_, 1, v_fst_3809_);
lean_ctor_set(v___x_3780_, 0, v_fst_3805_);
v___x_3870_ = v___x_3780_;
goto v_reusejp_3869_;
}
else
{
lean_object* v_reuseFailAlloc_4422_; 
v_reuseFailAlloc_4422_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_4422_, 0, v_fst_3805_);
lean_ctor_set(v_reuseFailAlloc_4422_, 1, v_fst_3809_);
v___x_3870_ = v_reuseFailAlloc_4422_;
goto v_reusejp_3869_;
}
v___jp_3815_:
{
lean_object* v___x_3819_; lean_object* v___x_3820_; lean_object* v___x_3821_; 
v___x_3819_ = l_Lean_Json_mkObj(v_fields_3818_);
lean_dec(v_fields_3818_);
v___x_3820_ = l_Lean_Json_compress(v___x_3819_);
v___x_3821_ = l_IO_FS_Handle_putStrLn(v_a_3751_, v___x_3820_);
if (lean_obj_tag(v___x_3821_) == 0)
{
lean_object* v___x_3822_; lean_object* v___x_3823_; uint8_t v___x_3824_; 
lean_dec_ref_known(v___x_3821_, 1);
v___x_3822_ = lean_nat_add(v_snd_3778_, v___x_3791_);
lean_dec(v_snd_3778_);
v___x_3823_ = lean_nat_mod(v___x_3822_, v___y_3816_);
lean_dec(v___y_3816_);
v___x_3824_ = lean_nat_dec_eq(v___x_3823_, v___x_3814_);
lean_dec(v___x_3823_);
if (v___x_3824_ == 0)
{
lean_object* v___x_3826_; 
if (v_isShared_3813_ == 0)
{
lean_ctor_set(v___x_3812_, 1, v___x_3822_);
lean_ctor_set(v___x_3812_, 0, v___y_3817_);
v___x_3826_ = v___x_3812_;
goto v_reusejp_3825_;
}
else
{
lean_object* v_reuseFailAlloc_3830_; 
v_reuseFailAlloc_3830_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3830_, 0, v___y_3817_);
lean_ctor_set(v_reuseFailAlloc_3830_, 1, v___x_3822_);
v___x_3826_ = v_reuseFailAlloc_3830_;
goto v_reusejp_3825_;
}
v_reusejp_3825_:
{
lean_object* v___x_3828_; 
if (v_isShared_3808_ == 0)
{
lean_ctor_set(v___x_3807_, 1, v___x_3826_);
lean_ctor_set(v___x_3807_, 0, v___x_3792_);
v___x_3828_ = v___x_3807_;
goto v_reusejp_3827_;
}
else
{
lean_object* v_reuseFailAlloc_3829_; 
v_reuseFailAlloc_3829_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3829_, 0, v___x_3792_);
lean_ctor_set(v_reuseFailAlloc_3829_, 1, v___x_3826_);
v___x_3828_ = v_reuseFailAlloc_3829_;
goto v_reusejp_3827_;
}
v_reusejp_3827_:
{
v_a_3760_ = v___x_3828_;
goto v___jp_3759_;
}
}
}
else
{
lean_object* v___x_3831_; lean_object* v___x_3832_; lean_object* v___x_3833_; lean_object* v___x_3834_; lean_object* v___x_3835_; lean_object* v___x_3836_; lean_object* v___x_3837_; lean_object* v___x_3838_; lean_object* v___x_3839_; lean_object* v___x_3840_; lean_object* v___x_3841_; lean_object* v___x_3842_; lean_object* v___x_3843_; 
v___x_3831_ = lean_io_mono_ms_now();
v___x_3832_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__0));
lean_inc_ref(v___x_3752_);
v___x_3833_ = lean_string_append(v___x_3752_, v___x_3832_);
lean_inc(v___x_3822_);
v___x_3834_ = l_Nat_reprFast(v___x_3822_);
v___x_3835_ = lean_string_append(v___x_3833_, v___x_3834_);
lean_dec_ref(v___x_3834_);
v___x_3836_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__1));
v___x_3837_ = lean_string_append(v___x_3835_, v___x_3836_);
v___x_3838_ = lean_nat_sub(v___x_3831_, v_a_3753_);
lean_dec(v___x_3831_);
v___x_3839_ = l_Nat_reprFast(v___x_3838_);
v___x_3840_ = lean_string_append(v___x_3837_, v___x_3839_);
lean_dec_ref(v___x_3839_);
v___x_3841_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__2));
v___x_3842_ = lean_string_append(v___x_3840_, v___x_3841_);
v___x_3843_ = l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(v___x_3842_);
if (lean_obj_tag(v___x_3843_) == 0)
{
lean_object* v___x_3845_; 
lean_dec_ref_known(v___x_3843_, 1);
if (v_isShared_3813_ == 0)
{
lean_ctor_set(v___x_3812_, 1, v___x_3822_);
lean_ctor_set(v___x_3812_, 0, v___y_3817_);
v___x_3845_ = v___x_3812_;
goto v_reusejp_3844_;
}
else
{
lean_object* v_reuseFailAlloc_3849_; 
v_reuseFailAlloc_3849_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3849_, 0, v___y_3817_);
lean_ctor_set(v_reuseFailAlloc_3849_, 1, v___x_3822_);
v___x_3845_ = v_reuseFailAlloc_3849_;
goto v_reusejp_3844_;
}
v_reusejp_3844_:
{
lean_object* v___x_3847_; 
if (v_isShared_3808_ == 0)
{
lean_ctor_set(v___x_3807_, 1, v___x_3845_);
lean_ctor_set(v___x_3807_, 0, v___x_3792_);
v___x_3847_ = v___x_3807_;
goto v_reusejp_3846_;
}
else
{
lean_object* v_reuseFailAlloc_3848_; 
v_reuseFailAlloc_3848_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_3848_, 0, v___x_3792_);
lean_ctor_set(v_reuseFailAlloc_3848_, 1, v___x_3845_);
v___x_3847_ = v_reuseFailAlloc_3848_;
goto v_reusejp_3846_;
}
v_reusejp_3846_:
{
v_a_3760_ = v___x_3847_;
goto v___jp_3759_;
}
}
}
else
{
lean_object* v_a_3850_; lean_object* v___x_3852_; uint8_t v_isShared_3853_; uint8_t v_isSharedCheck_3857_; 
lean_dec(v___x_3822_);
lean_dec(v___y_3817_);
lean_del_object(v___x_3812_);
lean_del_object(v___x_3807_);
lean_dec(v___x_3792_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_3850_ = lean_ctor_get(v___x_3843_, 0);
v_isSharedCheck_3857_ = !lean_is_exclusive(v___x_3843_);
if (v_isSharedCheck_3857_ == 0)
{
v___x_3852_ = v___x_3843_;
v_isShared_3853_ = v_isSharedCheck_3857_;
goto v_resetjp_3851_;
}
else
{
lean_inc(v_a_3850_);
lean_dec(v___x_3843_);
v___x_3852_ = lean_box(0);
v_isShared_3853_ = v_isSharedCheck_3857_;
goto v_resetjp_3851_;
}
v_resetjp_3851_:
{
lean_object* v___x_3855_; 
if (v_isShared_3853_ == 0)
{
v___x_3855_ = v___x_3852_;
goto v_reusejp_3854_;
}
else
{
lean_object* v_reuseFailAlloc_3856_; 
v_reuseFailAlloc_3856_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3856_, 0, v_a_3850_);
v___x_3855_ = v_reuseFailAlloc_3856_;
goto v_reusejp_3854_;
}
v_reusejp_3854_:
{
return v___x_3855_;
}
}
}
}
}
else
{
lean_object* v_a_3858_; lean_object* v___x_3860_; uint8_t v_isShared_3861_; uint8_t v_isSharedCheck_3865_; 
lean_dec(v___y_3817_);
lean_dec(v___y_3816_);
lean_del_object(v___x_3812_);
lean_del_object(v___x_3807_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_3858_ = lean_ctor_get(v___x_3821_, 0);
v_isSharedCheck_3865_ = !lean_is_exclusive(v___x_3821_);
if (v_isSharedCheck_3865_ == 0)
{
v___x_3860_ = v___x_3821_;
v_isShared_3861_ = v_isSharedCheck_3865_;
goto v_resetjp_3859_;
}
else
{
lean_inc(v_a_3858_);
lean_dec(v___x_3821_);
v___x_3860_ = lean_box(0);
v_isShared_3861_ = v_isSharedCheck_3865_;
goto v_resetjp_3859_;
}
v_resetjp_3859_:
{
lean_object* v___x_3863_; 
if (v_isShared_3861_ == 0)
{
v___x_3863_ = v___x_3860_;
goto v_reusejp_3862_;
}
else
{
lean_object* v_reuseFailAlloc_3864_; 
v_reuseFailAlloc_3864_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_3864_, 0, v_a_3858_);
v___x_3863_ = v_reuseFailAlloc_3864_;
goto v_reusejp_3862_;
}
v_reusejp_3862_:
{
return v___x_3863_;
}
}
}
}
v_reusejp_3869_:
{
lean_object* v___x_3872_; 
if (v_isShared_3776_ == 0)
{
lean_ctor_set(v___x_3775_, 1, v___x_3870_);
lean_ctor_set(v___x_3775_, 0, v___x_3866_);
v___x_3872_ = v___x_3775_;
goto v_reusejp_3871_;
}
else
{
lean_object* v_reuseFailAlloc_4421_; 
v_reuseFailAlloc_4421_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_4421_, 0, v___x_3866_);
lean_ctor_set(v_reuseFailAlloc_4421_, 1, v___x_3870_);
v___x_3872_ = v_reuseFailAlloc_4421_;
goto v_reusejp_3871_;
}
v_reusejp_3871_:
{
size_t v_sz_3873_; size_t v___x_3874_; lean_object* v___x_3875_; 
v_sz_3873_ = lean_array_size(v___x_3868_);
v___x_3874_ = ((size_t)0ULL);
lean_inc_ref(v_a_3747_);
v___x_3875_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__14(v_a_3747_, v___x_3868_, v_sz_3873_, v___x_3874_, v___x_3872_);
if (lean_obj_tag(v___x_3875_) == 0)
{
lean_object* v_a_3876_; lean_object* v_snd_3877_; lean_object* v_fst_3878_; lean_object* v___x_3880_; uint8_t v_isShared_3881_; uint8_t v_isSharedCheck_4412_; 
v_a_3876_ = lean_ctor_get(v___x_3875_, 0);
lean_inc(v_a_3876_);
lean_dec_ref_known(v___x_3875_, 1);
v_snd_3877_ = lean_ctor_get(v_a_3876_, 1);
v_fst_3878_ = lean_ctor_get(v_a_3876_, 0);
v_isSharedCheck_4412_ = !lean_is_exclusive(v_a_3876_);
if (v_isSharedCheck_4412_ == 0)
{
v___x_3880_ = v_a_3876_;
v_isShared_3881_ = v_isSharedCheck_4412_;
goto v_resetjp_3879_;
}
else
{
lean_inc(v_snd_3877_);
lean_inc(v_fst_3878_);
lean_dec(v_a_3876_);
v___x_3880_ = lean_box(0);
v_isShared_3881_ = v_isSharedCheck_4412_;
goto v_resetjp_3879_;
}
v_resetjp_3879_:
{
lean_object* v_fst_3882_; lean_object* v_snd_3883_; lean_object* v___x_3885_; uint8_t v_isShared_3886_; uint8_t v_isSharedCheck_4411_; 
v_fst_3882_ = lean_ctor_get(v_snd_3877_, 0);
v_snd_3883_ = lean_ctor_get(v_snd_3877_, 1);
v_isSharedCheck_4411_ = !lean_is_exclusive(v_snd_3877_);
if (v_isSharedCheck_4411_ == 0)
{
v___x_3885_ = v_snd_3877_;
v_isShared_3886_ = v_isSharedCheck_4411_;
goto v_resetjp_3884_;
}
else
{
lean_inc(v_snd_3883_);
lean_inc(v_fst_3882_);
lean_dec(v_snd_3877_);
v___x_3885_ = lean_box(0);
v_isShared_3886_ = v_isSharedCheck_4411_;
goto v_resetjp_3884_;
}
v_resetjp_3884_:
{
lean_object* v___y_3888_; lean_object* v___y_3889_; lean_object* v___y_3890_; lean_object* v___y_3891_; lean_object* v___y_3892_; lean_object* v___y_3893_; lean_object* v___y_3894_; lean_object* v___y_3895_; lean_object* v___y_3896_; lean_object* v___y_3897_; lean_object* v___y_3898_; lean_object* v___y_3899_; lean_object* v___y_3900_; lean_object* v___y_3901_; lean_object* v___y_3902_; lean_object* v___y_3903_; lean_object* v___y_3904_; lean_object* v___y_3905_; lean_object* v___y_3906_; lean_object* v___y_3907_; lean_object* v___y_3908_; lean_object* v___y_3909_; lean_object* v___y_3910_; uint8_t v___y_3911_; lean_object* v___y_3912_; lean_object* v___y_3913_; lean_object* v___y_3914_; lean_object* v___y_4035_; lean_object* v___y_4036_; lean_object* v___y_4037_; lean_object* v___y_4038_; lean_object* v___y_4039_; lean_object* v___y_4040_; lean_object* v___y_4041_; lean_object* v___y_4042_; lean_object* v___y_4043_; lean_object* v___y_4044_; lean_object* v___y_4045_; lean_object* v___y_4046_; lean_object* v___y_4047_; lean_object* v___y_4048_; lean_object* v___y_4049_; lean_object* v___y_4050_; lean_object* v___y_4051_; lean_object* v___y_4052_; lean_object* v___y_4053_; uint8_t v___y_4054_; lean_object* v___y_4055_; lean_object* v___y_4056_; lean_object* v___y_4057_; uint8_t v___y_4058_; uint8_t v___y_4059_; uint8_t v___x_4094_; lean_object* v___y_4096_; lean_object* v___y_4097_; lean_object* v___y_4098_; lean_object* v___y_4099_; lean_object* v___y_4100_; lean_object* v___y_4101_; lean_object* v___y_4102_; lean_object* v___y_4103_; lean_object* v___y_4104_; uint8_t v___y_4105_; lean_object* v___y_4106_; lean_object* v___y_4107_; lean_object* v___y_4108_; lean_object* v___y_4109_; lean_object* v___y_4110_; uint8_t v___y_4111_; lean_object* v___y_4112_; lean_object* v_a_4113_; lean_object* v___y_4145_; lean_object* v___y_4146_; lean_object* v___y_4147_; lean_object* v___y_4148_; lean_object* v___y_4149_; lean_object* v___y_4150_; lean_object* v___y_4151_; lean_object* v___y_4152_; lean_object* v___y_4153_; uint8_t v___y_4154_; lean_object* v___y_4155_; lean_object* v___y_4156_; lean_object* v___y_4157_; lean_object* v___y_4158_; lean_object* v___y_4159_; uint8_t v___y_4160_; lean_object* v___y_4161_; lean_object* v___x_4163_; lean_object* v___x_4164_; lean_object* v___x_4165_; lean_object* v___x_4166_; lean_object* v___x_4167_; lean_object* v___x_4168_; lean_object* v___x_4169_; lean_object* v___x_4170_; lean_object* v___x_4171_; lean_object* v___x_4172_; lean_object* v___y_4174_; lean_object* v___y_4175_; lean_object* v___y_4176_; lean_object* v___y_4177_; lean_object* v___y_4178_; lean_object* v___y_4179_; lean_object* v___y_4180_; lean_object* v___y_4181_; lean_object* v___y_4182_; uint8_t v___y_4183_; lean_object* v___y_4184_; lean_object* v___y_4185_; lean_object* v___y_4186_; lean_object* v___y_4187_; uint8_t v___y_4188_; lean_object* v_stmt_4189_; lean_object* v___y_4222_; lean_object* v___y_4223_; lean_object* v___y_4224_; lean_object* v___y_4225_; lean_object* v___y_4226_; lean_object* v___y_4227_; lean_object* v___y_4228_; lean_object* v___y_4229_; uint8_t v___y_4230_; lean_object* v___y_4231_; lean_object* v___y_4232_; lean_object* v___y_4233_; lean_object* v_ppFail_4234_; lean_object* v___y_4244_; lean_object* v___y_4245_; lean_object* v___y_4246_; lean_object* v___y_4247_; lean_object* v___y_4248_; lean_object* v___y_4249_; lean_object* v___y_4250_; lean_object* v___y_4251_; uint8_t v___y_4252_; lean_object* v___y_4253_; lean_object* v___y_4254_; uint8_t v___y_4255_; lean_object* v___y_4274_; lean_object* v___y_4275_; lean_object* v___y_4276_; lean_object* v___y_4277_; lean_object* v___y_4278_; lean_object* v___y_4279_; lean_object* v___y_4280_; lean_object* v___y_4281_; lean_object* v___y_4282_; lean_object* v___y_4283_; lean_object* v_stmt_4284_; uint8_t v_ppOk_4285_; lean_object* v___y_4299_; lean_object* v___y_4300_; lean_object* v___y_4301_; lean_object* v___y_4302_; lean_object* v___y_4303_; lean_object* v___y_4304_; lean_object* v___y_4305_; lean_object* v___y_4306_; lean_object* v___y_4307_; lean_object* v___y_4347_; lean_object* v___y_4348_; lean_object* v___y_4349_; lean_object* v___y_4350_; lean_object* v___y_4351_; lean_object* v___y_4352_; lean_object* v___y_4353_; lean_object* v___y_4354_; lean_object* v_valConsts_4357_; lean_object* v_proofSize_4358_; lean_object* v_proofTree_4359_; lean_object* v___x_4404_; 
v___x_4094_ = 0;
v___x_4163_ = lean_unsigned_to_nat(100u);
v___x_4164_ = lean_box(0);
v___x_4165_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_4166_ = l_Lean_instInhabitedFileMap_default;
v___x_4167_ = l_Lean_Options_empty;
v___x_4168_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_4169_ = lean_box(0);
v___x_4170_ = lean_box(0);
v___x_4171_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_4172_ = lean_box(0);
lean_inc(v_snd_3769_);
v___x_4404_ = l_NsExport_valueOf_x3f(v_snd_3769_);
if (lean_obj_tag(v___x_4404_) == 1)
{
lean_object* v_val_4405_; lean_object* v___x_4406_; lean_object* v_snd_4407_; lean_object* v_fst_4408_; lean_object* v_fst_4409_; lean_object* v___x_4410_; 
v_val_4405_ = lean_ctor_get(v___x_4404_, 0);
lean_inc_n(v_val_4405_, 2);
lean_dec_ref_known(v___x_4404_, 1);
v___x_4406_ = l_NsExport_sizes(v___x_3801_, v_val_4405_);
lean_dec(v___x_3801_);
v_snd_4407_ = lean_ctor_get(v___x_4406_, 1);
lean_inc(v_snd_4407_);
v_fst_4408_ = lean_ctor_get(v___x_4406_, 0);
lean_inc(v_fst_4408_);
lean_dec_ref(v___x_4406_);
v_fst_4409_ = lean_ctor_get(v_snd_4407_, 0);
lean_inc(v_fst_4409_);
lean_dec(v_snd_4407_);
v___x_4410_ = l_Lean_Expr_getUsedConstants(v_val_4405_);
v_valConsts_4357_ = v___x_4410_;
v_proofSize_4358_ = v_fst_4409_;
v_proofTree_4359_ = v_fst_4408_;
goto v___jp_4356_;
}
else
{
lean_dec(v___x_4404_);
lean_dec(v___x_3801_);
v_valConsts_4357_ = v___x_3867_;
v_proofSize_4358_ = v___x_3814_;
v_proofTree_4359_ = v___x_3814_;
goto v___jp_4356_;
}
v___jp_3887_:
{
lean_object* v_size_3915_; lean_object* v_size_3916_; lean_object* v___x_3918_; 
v_size_3915_ = lean_ctor_get(v___y_3888_, 0);
v_size_3916_ = lean_ctor_get(v___y_3901_, 0);
lean_inc_ref(v___y_3903_);
if (v_isShared_3886_ == 0)
{
lean_ctor_set(v___x_3885_, 1, v___y_3914_);
lean_ctor_set(v___x_3885_, 0, v___y_3903_);
v___x_3918_ = v___x_3885_;
goto v_reusejp_3917_;
}
else
{
lean_object* v_reuseFailAlloc_4033_; 
v_reuseFailAlloc_4033_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_4033_, 0, v___y_3903_);
lean_ctor_set(v_reuseFailAlloc_4033_, 1, v___y_3914_);
v___x_3918_ = v_reuseFailAlloc_4033_;
goto v_reusejp_3917_;
}
v_reusejp_3917_:
{
lean_object* v___x_3919_; lean_object* v___x_3920_; lean_object* v___x_3921_; lean_object* v___x_3923_; 
v___x_3919_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__3));
v___x_3920_ = l_Lean_JsonNumber_fromNat(v___y_3897_);
v___x_3921_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3921_, 0, v___x_3920_);
if (v_isShared_3881_ == 0)
{
lean_ctor_set(v___x_3880_, 1, v___x_3921_);
lean_ctor_set(v___x_3880_, 0, v___x_3919_);
v___x_3923_ = v___x_3880_;
goto v_reusejp_3922_;
}
else
{
lean_object* v_reuseFailAlloc_4032_; 
v_reuseFailAlloc_4032_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_4032_, 0, v___x_3919_);
lean_ctor_set(v_reuseFailAlloc_4032_, 1, v___x_3921_);
v___x_3923_ = v_reuseFailAlloc_4032_;
goto v_reusejp_3922_;
}
v_reusejp_3922_:
{
lean_object* v___x_3924_; lean_object* v___x_3925_; lean_object* v___x_3926_; lean_object* v___x_3927_; lean_object* v___x_3929_; 
v___x_3924_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__4));
v___x_3925_ = lean_array_get_size(v___y_3909_);
lean_dec_ref(v___y_3909_);
v___x_3926_ = l_Lean_JsonNumber_fromNat(v___x_3925_);
v___x_3927_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3927_, 0, v___x_3926_);
if (v_isShared_3772_ == 0)
{
lean_ctor_set(v___x_3771_, 1, v___x_3927_);
lean_ctor_set(v___x_3771_, 0, v___x_3924_);
v___x_3929_ = v___x_3771_;
goto v_reusejp_3928_;
}
else
{
lean_object* v_reuseFailAlloc_4031_; 
v_reuseFailAlloc_4031_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_4031_, 0, v___x_3924_);
lean_ctor_set(v_reuseFailAlloc_4031_, 1, v___x_3927_);
v___x_3929_ = v_reuseFailAlloc_4031_;
goto v_reusejp_3928_;
}
v_reusejp_3928_:
{
lean_object* v___x_3930_; lean_object* v___x_3931_; lean_object* v___x_3932_; lean_object* v___x_3933_; lean_object* v___x_3934_; lean_object* v___x_3935_; lean_object* v___x_3936_; lean_object* v___x_3937_; lean_object* v___x_3938_; lean_object* v___x_3939_; lean_object* v___x_3940_; lean_object* v___x_3941_; lean_object* v___x_3942_; lean_object* v___x_3943_; lean_object* v___x_3944_; lean_object* v___x_3945_; lean_object* v___x_3946_; lean_object* v___x_3947_; lean_object* v___x_3948_; lean_object* v___x_3949_; lean_object* v___x_3950_; lean_object* v___x_3951_; lean_object* v___x_3952_; lean_object* v___x_3953_; lean_object* v___x_3954_; lean_object* v___x_3955_; lean_object* v___x_3956_; lean_object* v___x_3957_; lean_object* v___x_3958_; lean_object* v___x_3959_; lean_object* v___x_3960_; uint64_t v___x_3961_; lean_object* v___x_3962_; lean_object* v___x_3963_; lean_object* v___x_3964_; lean_object* v___x_3965_; lean_object* v___x_3966_; lean_object* v___x_3967_; lean_object* v___x_3968_; lean_object* v___x_3969_; lean_object* v___x_3970_; lean_object* v___x_3971_; lean_object* v___x_3972_; lean_object* v___x_3973_; lean_object* v___x_3974_; lean_object* v___x_3975_; lean_object* v___x_3976_; lean_object* v___x_3977_; lean_object* v___x_3978_; lean_object* v___x_3979_; lean_object* v___x_3980_; lean_object* v___x_3981_; lean_object* v___x_3982_; lean_object* v___x_3983_; lean_object* v___x_3984_; lean_object* v___x_3985_; lean_object* v___x_3986_; lean_object* v___x_3987_; lean_object* v___x_3988_; lean_object* v___x_3989_; lean_object* v___x_3990_; lean_object* v___x_3991_; lean_object* v___x_3992_; 
v___x_3930_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__5));
v___x_3931_ = lean_array_get_size(v___x_3868_);
lean_dec(v___x_3868_);
v___x_3932_ = l_Lean_JsonNumber_fromNat(v___x_3931_);
v___x_3933_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3933_, 0, v___x_3932_);
v___x_3934_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3934_, 0, v___x_3930_);
lean_ctor_set(v___x_3934_, 1, v___x_3933_);
v___x_3935_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__6));
v___x_3936_ = l_NsExport_sortedNames(v___y_3894_);
lean_dec_ref(v___y_3894_);
v___x_3937_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_3936_);
v___x_3938_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3938_, 0, v___x_3935_);
lean_ctor_set(v___x_3938_, 1, v___x_3937_);
v___x_3939_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__7));
v___x_3940_ = l_NsExport_sortedNames(v___y_3904_);
lean_dec_ref(v___y_3904_);
v___x_3941_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_3940_);
v___x_3942_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3942_, 0, v___x_3939_);
lean_ctor_set(v___x_3942_, 1, v___x_3941_);
v___x_3943_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__8));
lean_inc(v_size_3915_);
v___x_3944_ = l_Lean_JsonNumber_fromNat(v_size_3915_);
v___x_3945_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3945_, 0, v___x_3944_);
v___x_3946_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3946_, 0, v___x_3943_);
lean_ctor_set(v___x_3946_, 1, v___x_3945_);
v___x_3947_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__9));
lean_inc(v_size_3916_);
v___x_3948_ = l_Lean_JsonNumber_fromNat(v_size_3916_);
v___x_3949_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_3949_, 0, v___x_3948_);
v___x_3950_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3950_, 0, v___x_3947_);
lean_ctor_set(v___x_3950_, 1, v___x_3949_);
v___x_3951_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__10));
v___x_3952_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0(v___x_3814_, v_a_3747_, v___y_3888_);
v___x_3953_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3953_, 0, v___x_3951_);
lean_ctor_set(v___x_3953_, 1, v___x_3952_);
v___x_3954_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__11));
v___x_3955_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__0(v___x_3814_, v_a_3747_, v___y_3901_);
v___x_3956_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3956_, 0, v___x_3954_);
lean_ctor_set(v___x_3956_, 1, v___x_3955_);
v___x_3957_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__12));
v___x_3958_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_3958_, 0, v___y_3911_);
v___x_3959_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3959_, 0, v___x_3957_);
lean_ctor_set(v___x_3959_, 1, v___x_3958_);
v___x_3960_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__13));
v___x_3961_ = lean_unbox_uint64(v_snd_3810_);
lean_dec(v_snd_3810_);
v___x_3962_ = l_NsExport_hexOf(v___x_3961_);
v___x_3963_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_3963_, 0, v___x_3962_);
v___x_3964_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_3964_, 0, v___x_3960_);
lean_ctor_set(v___x_3964_, 1, v___x_3963_);
v___x_3965_ = lean_box(0);
v___x_3966_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3966_, 0, v___x_3964_);
lean_ctor_set(v___x_3966_, 1, v___x_3965_);
v___x_3967_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3967_, 0, v___x_3959_);
lean_ctor_set(v___x_3967_, 1, v___x_3966_);
v___x_3968_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3968_, 0, v___x_3956_);
lean_ctor_set(v___x_3968_, 1, v___x_3967_);
v___x_3969_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3969_, 0, v___x_3953_);
lean_ctor_set(v___x_3969_, 1, v___x_3968_);
v___x_3970_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3970_, 0, v___x_3950_);
lean_ctor_set(v___x_3970_, 1, v___x_3969_);
v___x_3971_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3971_, 0, v___x_3946_);
lean_ctor_set(v___x_3971_, 1, v___x_3970_);
v___x_3972_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3972_, 0, v___x_3942_);
lean_ctor_set(v___x_3972_, 1, v___x_3971_);
v___x_3973_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3973_, 0, v___x_3938_);
lean_ctor_set(v___x_3973_, 1, v___x_3972_);
v___x_3974_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3974_, 0, v___x_3934_);
lean_ctor_set(v___x_3974_, 1, v___x_3973_);
v___x_3975_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3975_, 0, v___x_3929_);
lean_ctor_set(v___x_3975_, 1, v___x_3974_);
v___x_3976_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3976_, 0, v___x_3923_);
lean_ctor_set(v___x_3976_, 1, v___x_3975_);
v___x_3977_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3977_, 0, v___x_3918_);
lean_ctor_set(v___x_3977_, 1, v___x_3976_);
v___x_3978_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3978_, 0, v___y_3910_);
lean_ctor_set(v___x_3978_, 1, v___x_3977_);
v___x_3979_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3979_, 0, v___y_3899_);
lean_ctor_set(v___x_3979_, 1, v___x_3978_);
v___x_3980_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3980_, 0, v___y_3902_);
lean_ctor_set(v___x_3980_, 1, v___x_3979_);
v___x_3981_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3981_, 0, v___y_3890_);
lean_ctor_set(v___x_3981_, 1, v___x_3980_);
v___x_3982_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3982_, 0, v___y_3913_);
lean_ctor_set(v___x_3982_, 1, v___x_3981_);
v___x_3983_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3983_, 0, v___y_3912_);
lean_ctor_set(v___x_3983_, 1, v___x_3982_);
v___x_3984_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3984_, 0, v___y_3908_);
lean_ctor_set(v___x_3984_, 1, v___x_3983_);
v___x_3985_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3985_, 0, v___y_3891_);
lean_ctor_set(v___x_3985_, 1, v___x_3984_);
v___x_3986_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3986_, 0, v___y_3889_);
lean_ctor_set(v___x_3986_, 1, v___x_3985_);
v___x_3987_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3987_, 0, v___y_3896_);
lean_ctor_set(v___x_3987_, 1, v___x_3986_);
v___x_3988_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3988_, 0, v___y_3900_);
lean_ctor_set(v___x_3988_, 1, v___x_3987_);
v___x_3989_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3989_, 0, v___y_3907_);
lean_ctor_set(v___x_3989_, 1, v___x_3988_);
v___x_3990_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3990_, 0, v___y_3892_);
lean_ctor_set(v___x_3990_, 1, v___x_3989_);
v___x_3991_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3991_, 0, v___y_3905_);
lean_ctor_set(v___x_3991_, 1, v___x_3990_);
v___x_3992_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_3992_, 0, v___y_3893_);
lean_ctor_set(v___x_3992_, 1, v___x_3991_);
if (lean_obj_tag(v___y_3906_) == 0)
{
lean_object* v___x_3993_; lean_object* v___x_3994_; 
v___x_3993_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__19));
v___x_3994_ = l_List_appendTR___redArg(v___x_3992_, v___x_3993_);
v___y_3816_ = v___y_3898_;
v___y_3817_ = v___y_3895_;
v_fields_3818_ = v___x_3994_;
goto v___jp_3815_;
}
else
{
lean_object* v_val_3995_; lean_object* v___x_3997_; uint8_t v_isShared_3998_; uint8_t v_isSharedCheck_4030_; 
v_val_3995_ = lean_ctor_get(v___y_3906_, 0);
v_isSharedCheck_4030_ = !lean_is_exclusive(v___y_3906_);
if (v_isSharedCheck_4030_ == 0)
{
v___x_3997_ = v___y_3906_;
v_isShared_3998_ = v_isSharedCheck_4030_;
goto v_resetjp_3996_;
}
else
{
lean_inc(v_val_3995_);
lean_dec(v___y_3906_);
v___x_3997_ = lean_box(0);
v_isShared_3998_ = v_isSharedCheck_4030_;
goto v_resetjp_3996_;
}
v_resetjp_3996_:
{
lean_object* v_pos_3999_; lean_object* v_endPos_4000_; lean_object* v_line_4001_; lean_object* v___x_4003_; uint8_t v_isShared_4004_; uint8_t v_isSharedCheck_4028_; 
v_pos_3999_ = lean_ctor_get(v_val_3995_, 0);
lean_inc_ref(v_pos_3999_);
v_endPos_4000_ = lean_ctor_get(v_val_3995_, 2);
lean_inc_ref(v_endPos_4000_);
lean_dec(v_val_3995_);
v_line_4001_ = lean_ctor_get(v_pos_3999_, 0);
v_isSharedCheck_4028_ = !lean_is_exclusive(v_pos_3999_);
if (v_isSharedCheck_4028_ == 0)
{
lean_object* v_unused_4029_; 
v_unused_4029_ = lean_ctor_get(v_pos_3999_, 1);
lean_dec(v_unused_4029_);
v___x_4003_ = v_pos_3999_;
v_isShared_4004_ = v_isSharedCheck_4028_;
goto v_resetjp_4002_;
}
else
{
lean_inc(v_line_4001_);
lean_dec(v_pos_3999_);
v___x_4003_ = lean_box(0);
v_isShared_4004_ = v_isSharedCheck_4028_;
goto v_resetjp_4002_;
}
v_resetjp_4002_:
{
lean_object* v_line_4005_; lean_object* v___x_4007_; uint8_t v_isShared_4008_; uint8_t v_isSharedCheck_4026_; 
v_line_4005_ = lean_ctor_get(v_endPos_4000_, 0);
v_isSharedCheck_4026_ = !lean_is_exclusive(v_endPos_4000_);
if (v_isSharedCheck_4026_ == 0)
{
lean_object* v_unused_4027_; 
v_unused_4027_ = lean_ctor_get(v_endPos_4000_, 1);
lean_dec(v_unused_4027_);
v___x_4007_ = v_endPos_4000_;
v_isShared_4008_ = v_isSharedCheck_4026_;
goto v_resetjp_4006_;
}
else
{
lean_inc(v_line_4005_);
lean_dec(v_endPos_4000_);
v___x_4007_ = lean_box(0);
v_isShared_4008_ = v_isSharedCheck_4026_;
goto v_resetjp_4006_;
}
v_resetjp_4006_:
{
lean_object* v___x_4009_; lean_object* v___x_4010_; lean_object* v___x_4012_; 
v___x_4009_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__14));
v___x_4010_ = l_Lean_JsonNumber_fromNat(v_line_4001_);
if (v_isShared_3998_ == 0)
{
lean_ctor_set_tag(v___x_3997_, 2);
lean_ctor_set(v___x_3997_, 0, v___x_4010_);
v___x_4012_ = v___x_3997_;
goto v_reusejp_4011_;
}
else
{
lean_object* v_reuseFailAlloc_4025_; 
v_reuseFailAlloc_4025_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4025_, 0, v___x_4010_);
v___x_4012_ = v_reuseFailAlloc_4025_;
goto v_reusejp_4011_;
}
v_reusejp_4011_:
{
lean_object* v___x_4014_; 
if (v_isShared_4008_ == 0)
{
lean_ctor_set(v___x_4007_, 1, v___x_4012_);
lean_ctor_set(v___x_4007_, 0, v___x_4009_);
v___x_4014_ = v___x_4007_;
goto v_reusejp_4013_;
}
else
{
lean_object* v_reuseFailAlloc_4024_; 
v_reuseFailAlloc_4024_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_4024_, 0, v___x_4009_);
lean_ctor_set(v_reuseFailAlloc_4024_, 1, v___x_4012_);
v___x_4014_ = v_reuseFailAlloc_4024_;
goto v_reusejp_4013_;
}
v_reusejp_4013_:
{
lean_object* v___x_4015_; lean_object* v___x_4016_; lean_object* v___x_4017_; lean_object* v___x_4019_; 
v___x_4015_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__16));
v___x_4016_ = l_Lean_JsonNumber_fromNat(v_line_4005_);
v___x_4017_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_4017_, 0, v___x_4016_);
if (v_isShared_4004_ == 0)
{
lean_ctor_set(v___x_4003_, 1, v___x_4017_);
lean_ctor_set(v___x_4003_, 0, v___x_4015_);
v___x_4019_ = v___x_4003_;
goto v_reusejp_4018_;
}
else
{
lean_object* v_reuseFailAlloc_4023_; 
v_reuseFailAlloc_4023_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_4023_, 0, v___x_4015_);
lean_ctor_set(v_reuseFailAlloc_4023_, 1, v___x_4017_);
v___x_4019_ = v_reuseFailAlloc_4023_;
goto v_reusejp_4018_;
}
v_reusejp_4018_:
{
lean_object* v___x_4020_; lean_object* v___x_4021_; lean_object* v___x_4022_; 
v___x_4020_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_4020_, 0, v___x_4019_);
lean_ctor_set(v___x_4020_, 1, v___x_3965_);
v___x_4021_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_4021_, 0, v___x_4014_);
lean_ctor_set(v___x_4021_, 1, v___x_4020_);
v___x_4022_ = l_List_appendTR___redArg(v___x_3992_, v___x_4021_);
v___y_3816_ = v___y_3898_;
v___y_3817_ = v___y_3895_;
v_fields_3818_ = v___x_4022_;
goto v___jp_3815_;
}
}
}
}
}
}
}
}
}
}
}
v___jp_4034_:
{
lean_object* v___x_4060_; lean_object* v___x_4061_; lean_object* v___x_4062_; lean_object* v___x_4063_; lean_object* v___x_4064_; lean_object* v___x_4065_; lean_object* v___x_4066_; lean_object* v___x_4067_; lean_object* v___x_4068_; lean_object* v___x_4069_; lean_object* v___x_4070_; lean_object* v___x_4071_; lean_object* v___x_4072_; lean_object* v___x_4073_; uint8_t v___x_4074_; lean_object* v___x_4075_; lean_object* v___x_4076_; lean_object* v___x_4077_; lean_object* v___x_4078_; lean_object* v___x_4079_; lean_object* v___x_4080_; lean_object* v___x_4081_; lean_object* v___x_4082_; lean_object* v___x_4083_; lean_object* v___x_4084_; lean_object* v___x_4085_; lean_object* v___x_4086_; lean_object* v___x_4087_; lean_object* v___x_4088_; uint8_t v___x_4089_; 
v___x_4060_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_4060_, 0, v___y_4059_);
lean_inc_ref(v___y_4056_);
v___x_4061_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4061_, 0, v___y_4056_);
lean_ctor_set(v___x_4061_, 1, v___x_4060_);
v___x_4062_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__20));
v___x_4063_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_4063_, 0, v___y_4044_);
v___x_4064_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4064_, 0, v___x_4062_);
lean_ctor_set(v___x_4064_, 1, v___x_4063_);
v___x_4065_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__21));
v___x_4066_ = l_Lean_JsonNumber_fromNat(v___y_4050_);
v___x_4067_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_4067_, 0, v___x_4066_);
v___x_4068_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4068_, 0, v___x_4065_);
lean_ctor_set(v___x_4068_, 1, v___x_4067_);
v___x_4069_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__22));
v___x_4070_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_4070_, 0, v___y_4054_);
v___x_4071_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4071_, 0, v___x_4069_);
lean_ctor_set(v___x_4071_, 1, v___x_4070_);
v___x_4072_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__23));
v___x_4073_ = lean_alloc_ctor(1, 0, 1);
v___x_4074_ = lean_unbox(v___y_4039_);
lean_dec(v___y_4039_);
lean_ctor_set_uint8(v___x_4073_, 0, v___x_4074_);
v___x_4075_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4075_, 0, v___x_4072_);
lean_ctor_set(v___x_4075_, 1, v___x_4073_);
v___x_4076_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__24));
v___x_4077_ = l_Lean_JsonNumber_fromNat(v_fst_3882_);
v___x_4078_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_4078_, 0, v___x_4077_);
v___x_4079_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4079_, 0, v___x_4076_);
lean_ctor_set(v___x_4079_, 1, v___x_4078_);
v___x_4080_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__25));
v___x_4081_ = l_Lean_JsonNumber_fromNat(v_snd_3883_);
v___x_4082_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_4082_, 0, v___x_4081_);
v___x_4083_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4083_, 0, v___x_4080_);
lean_ctor_set(v___x_4083_, 1, v___x_4082_);
v___x_4084_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__26));
v___x_4085_ = l_Lean_JsonNumber_fromNat(v___y_4038_);
v___x_4086_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_4086_, 0, v___x_4085_);
v___x_4087_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4087_, 0, v___x_4084_);
lean_ctor_set(v___x_4087_, 1, v___x_4086_);
v___x_4088_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__27));
v___x_4089_ = lean_nat_dec_eq(v___y_4048_, v___x_3814_);
if (v___x_4089_ == 0)
{
lean_object* v___x_4090_; lean_object* v___x_4091_; lean_object* v___x_4092_; 
v___x_4090_ = lean_nat_log2(v___y_4048_);
lean_dec(v___y_4048_);
v___x_4091_ = l_Lean_JsonNumber_fromNat(v___x_4090_);
v___x_4092_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_4092_, 0, v___x_4091_);
v___y_3888_ = v___y_4035_;
v___y_3889_ = v___y_4036_;
v___y_3890_ = v___x_4075_;
v___y_3891_ = v___x_4061_;
v___y_3892_ = v___y_4037_;
v___y_3893_ = v___y_4040_;
v___y_3894_ = v___y_4041_;
v___y_3895_ = v___y_4042_;
v___y_3896_ = v___y_4043_;
v___y_3897_ = v___y_4045_;
v___y_3898_ = v___y_4046_;
v___y_3899_ = v___x_4083_;
v___y_3900_ = v___y_4047_;
v___y_3901_ = v___y_4049_;
v___y_3902_ = v___x_4079_;
v___y_3903_ = v___x_4088_;
v___y_3904_ = v___y_4051_;
v___y_3905_ = v___y_4052_;
v___y_3906_ = v___y_4053_;
v___y_3907_ = v___y_4055_;
v___y_3908_ = v___x_4064_;
v___y_3909_ = v___y_4057_;
v___y_3910_ = v___x_4087_;
v___y_3911_ = v___y_4058_;
v___y_3912_ = v___x_4068_;
v___y_3913_ = v___x_4071_;
v___y_3914_ = v___x_4092_;
goto v___jp_3887_;
}
else
{
lean_object* v___x_4093_; 
lean_dec(v___y_4048_);
v___x_4093_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__29);
v___y_3888_ = v___y_4035_;
v___y_3889_ = v___y_4036_;
v___y_3890_ = v___x_4075_;
v___y_3891_ = v___x_4061_;
v___y_3892_ = v___y_4037_;
v___y_3893_ = v___y_4040_;
v___y_3894_ = v___y_4041_;
v___y_3895_ = v___y_4042_;
v___y_3896_ = v___y_4043_;
v___y_3897_ = v___y_4045_;
v___y_3898_ = v___y_4046_;
v___y_3899_ = v___x_4083_;
v___y_3900_ = v___y_4047_;
v___y_3901_ = v___y_4049_;
v___y_3902_ = v___x_4079_;
v___y_3903_ = v___x_4088_;
v___y_3904_ = v___y_4051_;
v___y_3905_ = v___y_4052_;
v___y_3906_ = v___y_4053_;
v___y_3907_ = v___y_4055_;
v___y_3908_ = v___x_4064_;
v___y_3909_ = v___y_4057_;
v___y_3910_ = v___x_4087_;
v___y_3911_ = v___y_4058_;
v___y_3912_ = v___x_4068_;
v___y_3913_ = v___x_4071_;
v___y_3914_ = v___x_4093_;
goto v___jp_3887_;
}
}
v___jp_4095_:
{
lean_object* v___x_4114_; lean_object* v___x_4115_; lean_object* v___x_4116_; lean_object* v___x_4117_; lean_object* v___x_4118_; lean_object* v___x_4119_; lean_object* v___x_4120_; lean_object* v___x_4121_; lean_object* v___x_4122_; lean_object* v___x_4123_; lean_object* v___x_4124_; lean_object* v___x_4125_; lean_object* v___x_4126_; lean_object* v___x_4127_; lean_object* v___x_4128_; lean_object* v___x_4129_; lean_object* v___x_4130_; lean_object* v___x_4131_; uint8_t v___x_4132_; lean_object* v___x_4133_; lean_object* v___x_4134_; lean_object* v___x_4135_; uint8_t v___x_4136_; lean_object* v___x_4137_; lean_object* v___x_4138_; lean_object* v___x_4139_; uint8_t v___x_4140_; lean_object* v___x_4141_; lean_object* v___x_4142_; lean_object* v___x_4143_; 
v___x_4114_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__30));
lean_inc_n(v_fst_3768_, 2);
v___x_4115_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_3768_, v___x_4094_);
v___x_4116_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_4116_, 0, v___x_4115_);
v___x_4117_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4117_, 0, v___x_4114_);
lean_ctor_set(v___x_4117_, 1, v___x_4116_);
v___x_4118_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__31));
v___x_4119_ = l_Lean_privateToUserName(v_fst_3768_);
v___x_4120_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v___x_4119_, v___x_4094_);
v___x_4121_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_4121_, 0, v___x_4120_);
v___x_4122_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4122_, 0, v___x_4118_);
lean_ctor_set(v___x_4122_, 1, v___x_4121_);
v___x_4123_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__32));
v___x_4124_ = l_NsExport_moduleOf(v_a_3747_, v_fst_3768_);
v___x_4125_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v___x_4124_, v___x_3794_);
v___x_4126_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_4126_, 0, v___x_4125_);
v___x_4127_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4127_, 0, v___x_4123_);
lean_ctor_set(v___x_4127_, 1, v___x_4126_);
v___x_4128_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__33));
lean_inc_ref(v___y_4109_);
v___x_4129_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_4129_, 0, v___y_4109_);
v___x_4130_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4130_, 0, v___x_4128_);
lean_ctor_set(v___x_4130_, 1, v___x_4129_);
v___x_4131_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__34));
lean_inc_ref_n(v_a_3747_, 2);
v___x_4132_ = l_Lean_isClass(v_a_3747_, v_fst_3768_);
v___x_4133_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_4133_, 0, v___x_4132_);
v___x_4134_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4134_, 0, v___x_4131_);
lean_ctor_set(v___x_4134_, 1, v___x_4133_);
v___x_4135_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__35));
v___x_4136_ = l_Lean_Meta_isInstanceCore(v_a_3747_, v_fst_3768_);
v___x_4137_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_4137_, 0, v___x_4136_);
v___x_4138_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4138_, 0, v___x_4135_);
lean_ctor_set(v___x_4138_, 1, v___x_4137_);
v___x_4139_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__36));
v___x_4140_ = l_Lean_isPrivateName(v_fst_3768_);
lean_dec(v_fst_3768_);
v___x_4141_ = lean_alloc_ctor(1, 0, 1);
lean_ctor_set_uint8(v___x_4141_, 0, v___x_4140_);
v___x_4142_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4142_, 0, v___x_4139_);
lean_ctor_set(v___x_4142_, 1, v___x_4141_);
v___x_4143_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__37));
if (lean_obj_tag(v___y_4106_) == 0)
{
v___y_4035_ = v___y_4096_;
v___y_4036_ = v___x_4142_;
v___y_4037_ = v___x_4127_;
v___y_4038_ = v___y_4102_;
v___y_4039_ = v___y_4103_;
v___y_4040_ = v___x_4117_;
v___y_4041_ = v___y_4108_;
v___y_4042_ = v___y_4110_;
v___y_4043_ = v___x_4138_;
v___y_4044_ = v___y_4112_;
v___y_4045_ = v___y_4097_;
v___y_4046_ = v___y_4098_;
v___y_4047_ = v___x_4134_;
v___y_4048_ = v___y_4099_;
v___y_4049_ = v___y_4100_;
v___y_4050_ = v___y_4101_;
v___y_4051_ = v___y_4104_;
v___y_4052_ = v___x_4122_;
v___y_4053_ = v_a_4113_;
v___y_4054_ = v___y_4105_;
v___y_4055_ = v___x_4130_;
v___y_4056_ = v___x_4143_;
v___y_4057_ = v___y_4107_;
v___y_4058_ = v___y_4111_;
v___y_4059_ = v___x_4094_;
goto v___jp_4034_;
}
else
{
lean_dec_ref_known(v___y_4106_, 1);
v___y_4035_ = v___y_4096_;
v___y_4036_ = v___x_4142_;
v___y_4037_ = v___x_4127_;
v___y_4038_ = v___y_4102_;
v___y_4039_ = v___y_4103_;
v___y_4040_ = v___x_4117_;
v___y_4041_ = v___y_4108_;
v___y_4042_ = v___y_4110_;
v___y_4043_ = v___x_4138_;
v___y_4044_ = v___y_4112_;
v___y_4045_ = v___y_4097_;
v___y_4046_ = v___y_4098_;
v___y_4047_ = v___x_4134_;
v___y_4048_ = v___y_4099_;
v___y_4049_ = v___y_4100_;
v___y_4050_ = v___y_4101_;
v___y_4051_ = v___y_4104_;
v___y_4052_ = v___x_4122_;
v___y_4053_ = v_a_4113_;
v___y_4054_ = v___y_4105_;
v___y_4055_ = v___x_4130_;
v___y_4056_ = v___x_4143_;
v___y_4057_ = v___y_4107_;
v___y_4058_ = v___y_4111_;
v___y_4059_ = v___x_3794_;
goto v___jp_4034_;
}
}
v___jp_4144_:
{
lean_object* v___x_4162_; 
v___x_4162_ = lean_box(0);
v___y_4096_ = v___y_4145_;
v___y_4097_ = v___y_4146_;
v___y_4098_ = v___y_4147_;
v___y_4099_ = v___y_4148_;
v___y_4100_ = v___y_4149_;
v___y_4101_ = v___y_4150_;
v___y_4102_ = v___y_4151_;
v___y_4103_ = v___y_4152_;
v___y_4104_ = v___y_4153_;
v___y_4105_ = v___y_4154_;
v___y_4106_ = v___y_4155_;
v___y_4107_ = v___y_4157_;
v___y_4108_ = v___y_4156_;
v___y_4109_ = v___y_4158_;
v___y_4110_ = v___y_4159_;
v___y_4111_ = v___y_4160_;
v___y_4112_ = v___y_4161_;
v_a_4113_ = v___x_4162_;
goto v___jp_4095_;
}
v___jp_4173_:
{
lean_object* v___x_4190_; 
lean_inc(v_fst_3768_);
lean_inc_ref(v_a_3747_);
v___x_4190_ = l_Lean_findDocString_x3f(v_a_3747_, v_fst_3768_, v___x_3794_, v___x_4167_, v___x_4164_, v___x_4170_);
if (lean_obj_tag(v___x_4190_) == 0)
{
lean_object* v_a_4191_; lean_object* v___x_4192_; lean_object* v___x_4193_; 
v_a_4191_ = lean_ctor_get(v___x_4190_, 0);
lean_inc(v_a_4191_);
lean_dec_ref_known(v___x_4190_, 1);
lean_inc(v_fst_3768_);
v___x_4192_ = lean_alloc_closure((void*)(l_Lean_findDeclarationRanges_x3f___at___00Lean_Linter_EnvLinter_sortResults_spec__0___boxed), 4, 1);
lean_closure_set(v___x_4192_, 0, v_fst_3768_);
lean_inc_ref(v_a_3747_);
v___x_4193_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3814_, v___x_3791_, v___x_4164_, v___x_3794_, v_a_3747_, v___x_4168_, v___x_4165_, v___x_4166_, v___x_4169_, v___x_4170_, v___x_4171_, v___x_4172_, v___x_4094_, lean_box(0), v___x_4192_);
if (lean_obj_tag(v___x_4193_) == 0)
{
lean_object* v_a_4194_; 
v_a_4194_ = lean_ctor_get(v___x_4193_, 0);
lean_inc(v_a_4194_);
lean_dec_ref_known(v___x_4193_, 1);
if (lean_obj_tag(v_a_4194_) == 0)
{
v___y_4145_ = v___y_4174_;
v___y_4146_ = v___y_4175_;
v___y_4147_ = v___y_4176_;
v___y_4148_ = v___y_4177_;
v___y_4149_ = v___y_4178_;
v___y_4150_ = v___y_4179_;
v___y_4151_ = v___y_4180_;
v___y_4152_ = v___y_4181_;
v___y_4153_ = v___y_4182_;
v___y_4154_ = v___y_4183_;
v___y_4155_ = v_a_4191_;
v___y_4156_ = v___y_4185_;
v___y_4157_ = v___y_4184_;
v___y_4158_ = v___y_4186_;
v___y_4159_ = v___y_4187_;
v___y_4160_ = v___y_4188_;
v___y_4161_ = v_stmt_4189_;
goto v___jp_4144_;
}
else
{
lean_object* v_val_4195_; 
v_val_4195_ = lean_ctor_get(v_a_4194_, 0);
lean_inc(v_val_4195_);
lean_dec_ref_known(v_a_4194_, 1);
if (lean_obj_tag(v_val_4195_) == 0)
{
v___y_4145_ = v___y_4174_;
v___y_4146_ = v___y_4175_;
v___y_4147_ = v___y_4176_;
v___y_4148_ = v___y_4177_;
v___y_4149_ = v___y_4178_;
v___y_4150_ = v___y_4179_;
v___y_4151_ = v___y_4180_;
v___y_4152_ = v___y_4181_;
v___y_4153_ = v___y_4182_;
v___y_4154_ = v___y_4183_;
v___y_4155_ = v_a_4191_;
v___y_4156_ = v___y_4185_;
v___y_4157_ = v___y_4184_;
v___y_4158_ = v___y_4186_;
v___y_4159_ = v___y_4187_;
v___y_4160_ = v___y_4188_;
v___y_4161_ = v_stmt_4189_;
goto v___jp_4144_;
}
else
{
lean_object* v_val_4196_; lean_object* v___x_4198_; uint8_t v_isShared_4199_; uint8_t v_isSharedCheck_4204_; 
v_val_4196_ = lean_ctor_get(v_val_4195_, 0);
v_isSharedCheck_4204_ = !lean_is_exclusive(v_val_4195_);
if (v_isSharedCheck_4204_ == 0)
{
v___x_4198_ = v_val_4195_;
v_isShared_4199_ = v_isSharedCheck_4204_;
goto v_resetjp_4197_;
}
else
{
lean_inc(v_val_4196_);
lean_dec(v_val_4195_);
v___x_4198_ = lean_box(0);
v_isShared_4199_ = v_isSharedCheck_4204_;
goto v_resetjp_4197_;
}
v_resetjp_4197_:
{
lean_object* v_range_4200_; lean_object* v___x_4202_; 
v_range_4200_ = lean_ctor_get(v_val_4196_, 0);
lean_inc_ref(v_range_4200_);
lean_dec(v_val_4196_);
if (v_isShared_4199_ == 0)
{
lean_ctor_set(v___x_4198_, 0, v_range_4200_);
v___x_4202_ = v___x_4198_;
goto v_reusejp_4201_;
}
else
{
lean_object* v_reuseFailAlloc_4203_; 
v_reuseFailAlloc_4203_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4203_, 0, v_range_4200_);
v___x_4202_ = v_reuseFailAlloc_4203_;
goto v_reusejp_4201_;
}
v_reusejp_4201_:
{
v___y_4096_ = v___y_4174_;
v___y_4097_ = v___y_4175_;
v___y_4098_ = v___y_4176_;
v___y_4099_ = v___y_4177_;
v___y_4100_ = v___y_4178_;
v___y_4101_ = v___y_4179_;
v___y_4102_ = v___y_4180_;
v___y_4103_ = v___y_4181_;
v___y_4104_ = v___y_4182_;
v___y_4105_ = v___y_4183_;
v___y_4106_ = v_a_4191_;
v___y_4107_ = v___y_4184_;
v___y_4108_ = v___y_4185_;
v___y_4109_ = v___y_4186_;
v___y_4110_ = v___y_4187_;
v___y_4111_ = v___y_4188_;
v___y_4112_ = v_stmt_4189_;
v_a_4113_ = v___x_4202_;
goto v___jp_4095_;
}
}
}
}
}
else
{
lean_object* v_a_4205_; lean_object* v___x_4207_; uint8_t v_isShared_4208_; uint8_t v_isSharedCheck_4212_; 
lean_dec(v_a_4191_);
lean_dec_ref(v_stmt_4189_);
lean_dec(v___y_4187_);
lean_dec_ref(v___y_4185_);
lean_dec_ref(v___y_4184_);
lean_dec_ref(v___y_4182_);
lean_dec(v___y_4181_);
lean_dec(v___y_4180_);
lean_dec(v___y_4179_);
lean_dec_ref(v___y_4178_);
lean_dec(v___y_4177_);
lean_dec(v___y_4176_);
lean_dec(v___y_4175_);
lean_dec_ref(v___y_4174_);
lean_del_object(v___x_3885_);
lean_dec(v_snd_3883_);
lean_dec(v_fst_3882_);
lean_del_object(v___x_3880_);
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_del_object(v___x_3771_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4205_ = lean_ctor_get(v___x_4193_, 0);
v_isSharedCheck_4212_ = !lean_is_exclusive(v___x_4193_);
if (v_isSharedCheck_4212_ == 0)
{
v___x_4207_ = v___x_4193_;
v_isShared_4208_ = v_isSharedCheck_4212_;
goto v_resetjp_4206_;
}
else
{
lean_inc(v_a_4205_);
lean_dec(v___x_4193_);
v___x_4207_ = lean_box(0);
v_isShared_4208_ = v_isSharedCheck_4212_;
goto v_resetjp_4206_;
}
v_resetjp_4206_:
{
lean_object* v___x_4210_; 
if (v_isShared_4208_ == 0)
{
v___x_4210_ = v___x_4207_;
goto v_reusejp_4209_;
}
else
{
lean_object* v_reuseFailAlloc_4211_; 
v_reuseFailAlloc_4211_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4211_, 0, v_a_4205_);
v___x_4210_ = v_reuseFailAlloc_4211_;
goto v_reusejp_4209_;
}
v_reusejp_4209_:
{
return v___x_4210_;
}
}
}
}
else
{
lean_object* v_a_4213_; lean_object* v___x_4215_; uint8_t v_isShared_4216_; uint8_t v_isSharedCheck_4220_; 
lean_dec_ref(v_stmt_4189_);
lean_dec(v___y_4187_);
lean_dec_ref(v___y_4185_);
lean_dec_ref(v___y_4184_);
lean_dec_ref(v___y_4182_);
lean_dec(v___y_4181_);
lean_dec(v___y_4180_);
lean_dec(v___y_4179_);
lean_dec_ref(v___y_4178_);
lean_dec(v___y_4177_);
lean_dec(v___y_4176_);
lean_dec(v___y_4175_);
lean_dec_ref(v___y_4174_);
lean_del_object(v___x_3885_);
lean_dec(v_snd_3883_);
lean_dec(v_fst_3882_);
lean_del_object(v___x_3880_);
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_del_object(v___x_3771_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4213_ = lean_ctor_get(v___x_4190_, 0);
v_isSharedCheck_4220_ = !lean_is_exclusive(v___x_4190_);
if (v_isSharedCheck_4220_ == 0)
{
v___x_4215_ = v___x_4190_;
v_isShared_4216_ = v_isSharedCheck_4220_;
goto v_resetjp_4214_;
}
else
{
lean_inc(v_a_4213_);
lean_dec(v___x_4190_);
v___x_4215_ = lean_box(0);
v_isShared_4216_ = v_isSharedCheck_4220_;
goto v_resetjp_4214_;
}
v_resetjp_4214_:
{
lean_object* v___x_4218_; 
if (v_isShared_4216_ == 0)
{
v___x_4218_ = v___x_4215_;
goto v_reusejp_4217_;
}
else
{
lean_object* v_reuseFailAlloc_4219_; 
v_reuseFailAlloc_4219_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4219_, 0, v_a_4213_);
v___x_4218_ = v_reuseFailAlloc_4219_;
goto v_reusejp_4217_;
}
v_reusejp_4217_:
{
return v___x_4218_;
}
}
}
}
v___jp_4221_:
{
lean_object* v___x_4235_; lean_object* v___x_4236_; uint8_t v___x_4237_; 
v___x_4235_ = lean_string_length(v___y_4229_);
v___x_4236_ = lean_unsigned_to_nat(2000u);
v___x_4237_ = lean_nat_dec_lt(v___x_4236_, v___x_4235_);
if (v___x_4237_ == 0)
{
v___y_4174_ = v___y_4222_;
v___y_4175_ = v___y_4223_;
v___y_4176_ = v___x_4236_;
v___y_4177_ = v___y_4226_;
v___y_4178_ = v___y_4228_;
v___y_4179_ = v___x_4235_;
v___y_4180_ = v___y_4233_;
v___y_4181_ = v___y_4232_;
v___y_4182_ = v___y_4231_;
v___y_4183_ = v___x_4237_;
v___y_4184_ = v___y_4225_;
v___y_4185_ = v___y_4224_;
v___y_4186_ = v___y_4227_;
v___y_4187_ = v_ppFail_4234_;
v___y_4188_ = v___y_4230_;
v_stmt_4189_ = v___y_4229_;
goto v___jp_4173_;
}
else
{
lean_object* v___x_4238_; lean_object* v___x_4239_; lean_object* v___x_4240_; lean_object* v___x_4241_; lean_object* v___x_4242_; 
v___x_4238_ = lean_string_utf8_byte_size(v___y_4229_);
lean_inc(v___y_4229_);
v___x_4239_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_4239_, 0, v___y_4229_);
lean_ctor_set(v___x_4239_, 1, v___x_3814_);
lean_ctor_set(v___x_4239_, 2, v___x_4238_);
v___x_4240_ = l_String_Slice_Pos_nextn(v___x_4239_, v___x_3814_, v___x_4236_);
lean_dec_ref_known(v___x_4239_, 3);
v___x_4241_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_4241_, 0, v___y_4229_);
lean_ctor_set(v___x_4241_, 1, v___x_3814_);
lean_ctor_set(v___x_4241_, 2, v___x_4240_);
v___x_4242_ = l_String_Slice_toString(v___x_4241_);
lean_dec_ref_known(v___x_4241_, 3);
v___y_4174_ = v___y_4222_;
v___y_4175_ = v___y_4223_;
v___y_4176_ = v___x_4236_;
v___y_4177_ = v___y_4226_;
v___y_4178_ = v___y_4228_;
v___y_4179_ = v___x_4235_;
v___y_4180_ = v___y_4233_;
v___y_4181_ = v___y_4232_;
v___y_4182_ = v___y_4231_;
v___y_4183_ = v___x_4237_;
v___y_4184_ = v___y_4225_;
v___y_4185_ = v___y_4224_;
v___y_4186_ = v___y_4227_;
v___y_4187_ = v_ppFail_4234_;
v___y_4188_ = v___y_4230_;
v_stmt_4189_ = v___x_4242_;
goto v___jp_4173_;
}
}
v___jp_4243_:
{
lean_object* v___x_4256_; lean_object* v___x_4257_; lean_object* v___x_4258_; 
v___x_4256_ = lean_box(v___y_4252_);
v___x_4257_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4257_, 0, v___y_4251_);
lean_ctor_set(v___x_4257_, 1, v___x_4256_);
lean_inc_ref(v_a_3747_);
v___x_4258_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16(v_a_3747_, v___x_3793_, v_shard_3746_, v___x_3868_, v_sz_3873_, v___x_3874_, v___x_4257_);
lean_dec(v___x_3793_);
if (lean_obj_tag(v___x_4258_) == 0)
{
lean_object* v_a_4259_; lean_object* v_snd_4260_; uint8_t v___x_4261_; 
v_a_4259_ = lean_ctor_get(v___x_4258_, 0);
lean_inc(v_a_4259_);
lean_dec_ref_known(v___x_4258_, 1);
v_snd_4260_ = lean_ctor_get(v_a_4259_, 1);
lean_inc(v_snd_4260_);
v___x_4261_ = lean_unbox(v_snd_4260_);
if (v___x_4261_ == 0)
{
lean_object* v_fst_4262_; lean_object* v___x_4263_; 
v_fst_4262_ = lean_ctor_get(v_a_4259_, 0);
lean_inc(v_fst_4262_);
lean_dec(v_a_4259_);
v___x_4263_ = lean_nat_add(v_fst_3777_, v___x_3791_);
lean_dec(v_fst_3777_);
v___y_4222_ = v___y_4244_;
v___y_4223_ = v___y_4245_;
v___y_4224_ = v___y_4247_;
v___y_4225_ = v___y_4246_;
v___y_4226_ = v___y_4248_;
v___y_4227_ = v___y_4249_;
v___y_4228_ = v___y_4250_;
v___y_4229_ = v_fst_4262_;
v___y_4230_ = v___y_4255_;
v___y_4231_ = v___y_4254_;
v___y_4232_ = v_snd_4260_;
v___y_4233_ = v___y_4253_;
v_ppFail_4234_ = v___x_4263_;
goto v___jp_4221_;
}
else
{
lean_object* v_fst_4264_; 
v_fst_4264_ = lean_ctor_get(v_a_4259_, 0);
lean_inc(v_fst_4264_);
lean_dec(v_a_4259_);
v___y_4222_ = v___y_4244_;
v___y_4223_ = v___y_4245_;
v___y_4224_ = v___y_4247_;
v___y_4225_ = v___y_4246_;
v___y_4226_ = v___y_4248_;
v___y_4227_ = v___y_4249_;
v___y_4228_ = v___y_4250_;
v___y_4229_ = v_fst_4264_;
v___y_4230_ = v___y_4255_;
v___y_4231_ = v___y_4254_;
v___y_4232_ = v_snd_4260_;
v___y_4233_ = v___y_4253_;
v_ppFail_4234_ = v_fst_3777_;
goto v___jp_4221_;
}
}
else
{
lean_object* v_a_4265_; lean_object* v___x_4267_; uint8_t v_isShared_4268_; uint8_t v_isSharedCheck_4272_; 
lean_dec_ref(v___y_4254_);
lean_dec(v___y_4253_);
lean_dec_ref(v___y_4250_);
lean_dec(v___y_4248_);
lean_dec_ref(v___y_4247_);
lean_dec_ref(v___y_4246_);
lean_dec(v___y_4245_);
lean_dec_ref(v___y_4244_);
lean_del_object(v___x_3885_);
lean_dec(v_snd_3883_);
lean_dec(v_fst_3882_);
lean_del_object(v___x_3880_);
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_dec(v_fst_3777_);
lean_del_object(v___x_3771_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4265_ = lean_ctor_get(v___x_4258_, 0);
v_isSharedCheck_4272_ = !lean_is_exclusive(v___x_4258_);
if (v_isSharedCheck_4272_ == 0)
{
v___x_4267_ = v___x_4258_;
v_isShared_4268_ = v_isSharedCheck_4272_;
goto v_resetjp_4266_;
}
else
{
lean_inc(v_a_4265_);
lean_dec(v___x_4258_);
v___x_4267_ = lean_box(0);
v_isShared_4268_ = v_isSharedCheck_4272_;
goto v_resetjp_4266_;
}
v_resetjp_4266_:
{
lean_object* v___x_4270_; 
if (v_isShared_4268_ == 0)
{
v___x_4270_ = v___x_4267_;
goto v_reusejp_4269_;
}
else
{
lean_object* v_reuseFailAlloc_4271_; 
v_reuseFailAlloc_4271_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4271_, 0, v_a_4265_);
v___x_4270_ = v_reuseFailAlloc_4271_;
goto v_reusejp_4269_;
}
v_reusejp_4269_:
{
return v___x_4270_;
}
}
}
}
v___jp_4273_:
{
lean_object* v___x_4286_; 
lean_inc_ref(v_a_3747_);
v___x_4286_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3814_, v___x_3791_, v___x_4164_, v___x_3794_, v_a_3747_, v___x_4168_, v___x_4165_, v___x_4166_, v___x_4169_, v___x_4170_, v___x_4171_, v___x_4172_, v___x_4094_, lean_box(0), v___y_4274_);
if (lean_obj_tag(v___x_4286_) == 0)
{
lean_object* v_a_4287_; 
v_a_4287_ = lean_ctor_get(v___x_4286_, 0);
lean_inc(v_a_4287_);
lean_dec_ref_known(v___x_4286_, 1);
if (lean_obj_tag(v_a_4287_) == 0)
{
v___y_4244_ = v___y_4275_;
v___y_4245_ = v___y_4276_;
v___y_4246_ = v___y_4278_;
v___y_4247_ = v___y_4277_;
v___y_4248_ = v___y_4279_;
v___y_4249_ = v___y_4280_;
v___y_4250_ = v___y_4281_;
v___y_4251_ = v_stmt_4284_;
v___y_4252_ = v_ppOk_4285_;
v___y_4253_ = v___y_4283_;
v___y_4254_ = v___y_4282_;
v___y_4255_ = v___x_4094_;
goto v___jp_4243_;
}
else
{
lean_object* v_val_4288_; uint8_t v___x_4289_; 
v_val_4288_ = lean_ctor_get(v_a_4287_, 0);
lean_inc(v_val_4288_);
lean_dec_ref_known(v_a_4287_, 1);
v___x_4289_ = lean_unbox(v_val_4288_);
lean_dec(v_val_4288_);
v___y_4244_ = v___y_4275_;
v___y_4245_ = v___y_4276_;
v___y_4246_ = v___y_4278_;
v___y_4247_ = v___y_4277_;
v___y_4248_ = v___y_4279_;
v___y_4249_ = v___y_4280_;
v___y_4250_ = v___y_4281_;
v___y_4251_ = v_stmt_4284_;
v___y_4252_ = v_ppOk_4285_;
v___y_4253_ = v___y_4283_;
v___y_4254_ = v___y_4282_;
v___y_4255_ = v___x_4289_;
goto v___jp_4243_;
}
}
else
{
lean_object* v_a_4290_; lean_object* v___x_4292_; uint8_t v_isShared_4293_; uint8_t v_isSharedCheck_4297_; 
lean_dec_ref(v_stmt_4284_);
lean_dec(v___y_4283_);
lean_dec_ref(v___y_4282_);
lean_dec_ref(v___y_4281_);
lean_dec(v___y_4279_);
lean_dec_ref(v___y_4278_);
lean_dec_ref(v___y_4277_);
lean_dec(v___y_4276_);
lean_dec_ref(v___y_4275_);
lean_del_object(v___x_3885_);
lean_dec(v_snd_3883_);
lean_dec(v_fst_3882_);
lean_del_object(v___x_3880_);
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec(v___x_3793_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_dec(v_fst_3777_);
lean_del_object(v___x_3771_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4290_ = lean_ctor_get(v___x_4286_, 0);
v_isSharedCheck_4297_ = !lean_is_exclusive(v___x_4286_);
if (v_isSharedCheck_4297_ == 0)
{
v___x_4292_ = v___x_4286_;
v_isShared_4293_ = v_isSharedCheck_4297_;
goto v_resetjp_4291_;
}
else
{
lean_inc(v_a_4290_);
lean_dec(v___x_4286_);
v___x_4292_ = lean_box(0);
v_isShared_4293_ = v_isSharedCheck_4297_;
goto v_resetjp_4291_;
}
v_resetjp_4291_:
{
lean_object* v___x_4295_; 
if (v_isShared_4293_ == 0)
{
v___x_4295_ = v___x_4292_;
goto v_reusejp_4294_;
}
else
{
lean_object* v_reuseFailAlloc_4296_; 
v_reuseFailAlloc_4296_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4296_, 0, v_a_4290_);
v___x_4295_ = v_reuseFailAlloc_4296_;
goto v_reusejp_4294_;
}
v_reusejp_4294_:
{
return v___x_4295_;
}
}
}
}
v___jp_4298_:
{
uint8_t v___x_4308_; uint8_t v___x_4309_; uint8_t v___x_4310_; lean_object* v___x_4311_; uint64_t v___x_4312_; lean_object* v___x_4313_; lean_object* v___x_4314_; lean_object* v___x_4315_; lean_object* v___x_4316_; lean_object* v___x_4317_; lean_object* v___x_4318_; lean_object* v___x_4319_; lean_object* v___f_4320_; lean_object* v___x_4321_; 
v___x_4308_ = 1;
v___x_4309_ = 0;
v___x_4310_ = 2;
v___x_4311_ = lean_alloc_ctor(0, 0, 20);
lean_ctor_set_uint8(v___x_4311_, 0, v___x_4094_);
lean_ctor_set_uint8(v___x_4311_, 1, v___x_4094_);
lean_ctor_set_uint8(v___x_4311_, 2, v___x_4094_);
lean_ctor_set_uint8(v___x_4311_, 3, v___x_4094_);
lean_ctor_set_uint8(v___x_4311_, 4, v___x_4094_);
lean_ctor_set_uint8(v___x_4311_, 5, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 6, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 7, v___x_4094_);
lean_ctor_set_uint8(v___x_4311_, 8, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 9, v___x_4308_);
lean_ctor_set_uint8(v___x_4311_, 10, v___x_4309_);
lean_ctor_set_uint8(v___x_4311_, 11, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 12, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 13, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 14, v___x_4310_);
lean_ctor_set_uint8(v___x_4311_, 15, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 16, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 17, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 18, v___x_3794_);
lean_ctor_set_uint8(v___x_4311_, 19, v___x_4094_);
v___x_4312_ = l___private_Lean_Meta_Basic_0__Lean_Meta_Config_toKey(v___x_4311_);
v___x_4313_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_4313_, 0, v___x_4311_);
lean_ctor_set_uint64(v___x_4313_, sizeof(void*)*1, v___x_4312_);
v___x_4314_ = lean_box(1);
v___x_4315_ = lean_unsigned_to_nat(32u);
v___x_4316_ = lean_mk_empty_array_with_capacity(v___x_4315_);
lean_dec_ref(v___x_4316_);
v___x_4317_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__4);
v___x_4318_ = lean_alloc_ctor(0, 7, 4);
lean_ctor_set(v___x_4318_, 0, v___x_4313_);
lean_ctor_set(v___x_4318_, 1, v___x_4314_);
lean_ctor_set(v___x_4318_, 2, v___x_4317_);
lean_ctor_set(v___x_4318_, 3, v___x_3867_);
lean_ctor_set(v___x_4318_, 4, v___x_4172_);
lean_ctor_set(v___x_4318_, 5, v___x_3814_);
lean_ctor_set(v___x_4318_, 6, v___x_4172_);
lean_ctor_set_uint8(v___x_4318_, sizeof(void*)*7, v___x_4094_);
lean_ctor_set_uint8(v___x_4318_, sizeof(void*)*7 + 1, v___x_4094_);
lean_ctor_set_uint8(v___x_4318_, sizeof(void*)*7 + 2, v___x_4094_);
lean_ctor_set_uint8(v___x_4318_, sizeof(void*)*7 + 3, v___x_3794_);
v___x_4319_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__16);
lean_inc_ref(v___x_4318_);
lean_inc(v_fst_3768_);
v___f_4320_ = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__2___boxed), 8, 5);
lean_closure_set(v___f_4320_, 0, v___x_4319_);
lean_closure_set(v___f_4320_, 1, v___x_4163_);
lean_closure_set(v___f_4320_, 2, v___x_3814_);
lean_closure_set(v___f_4320_, 3, v_fst_3768_);
lean_closure_set(v___f_4320_, 4, v___x_4318_);
lean_inc_ref(v_a_3747_);
v___x_4321_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3814_, v___x_3791_, v___x_4164_, v___x_3794_, v_a_3747_, v___x_4168_, v___x_4165_, v___x_4166_, v___x_4169_, v___x_4170_, v___x_4171_, v___x_4172_, v___x_4094_, lean_box(0), v___f_4320_);
if (lean_obj_tag(v___x_4321_) == 0)
{
lean_object* v_a_4322_; lean_object* v___f_4323_; 
v_a_4322_ = lean_ctor_get(v___x_4321_, 0);
lean_inc(v_a_4322_);
lean_dec_ref_known(v___x_4321_, 1);
lean_inc_ref(v___x_4318_);
lean_inc_ref(v___x_3802_);
v___f_4323_ = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__3___boxed), 6, 3);
lean_closure_set(v___f_4323_, 0, v___x_4319_);
lean_closure_set(v___f_4323_, 1, v___x_3802_);
lean_closure_set(v___f_4323_, 2, v___x_4318_);
if (lean_obj_tag(v_a_4322_) == 0)
{
lean_object* v___f_4324_; lean_object* v___x_4325_; 
v___f_4324_ = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__4___boxed), 8, 5);
lean_closure_set(v___f_4324_, 0, v___x_4319_);
lean_closure_set(v___f_4324_, 1, v___x_4163_);
lean_closure_set(v___f_4324_, 2, v___x_3814_);
lean_closure_set(v___f_4324_, 3, v___x_3802_);
lean_closure_set(v___f_4324_, 4, v___x_4318_);
lean_inc_ref(v_a_3747_);
v___x_4325_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___lam__1(v___x_3814_, v___x_3791_, v___x_4164_, v___x_3794_, v_a_3747_, v___x_4168_, v___x_4165_, v___x_4166_, v___x_4169_, v___x_4170_, v___x_4171_, v___x_4172_, v___x_4094_, lean_box(0), v___f_4324_);
if (lean_obj_tag(v___x_4325_) == 0)
{
lean_object* v_a_4326_; 
v_a_4326_ = lean_ctor_get(v___x_4325_, 0);
lean_inc(v_a_4326_);
lean_dec_ref_known(v___x_4325_, 1);
if (lean_obj_tag(v_a_4326_) == 0)
{
lean_object* v___x_4327_; 
v___x_4327_ = ((lean_object*)(l_NsExport_hexOf___closed__0));
v___y_4274_ = v___f_4323_;
v___y_4275_ = v___y_4299_;
v___y_4276_ = v___y_4300_;
v___y_4277_ = v___y_4302_;
v___y_4278_ = v___y_4301_;
v___y_4279_ = v___y_4303_;
v___y_4280_ = v___y_4307_;
v___y_4281_ = v___y_4304_;
v___y_4282_ = v___y_4306_;
v___y_4283_ = v___y_4305_;
v_stmt_4284_ = v___x_4327_;
v_ppOk_4285_ = v___x_4094_;
goto v___jp_4273_;
}
else
{
lean_object* v_val_4328_; 
v_val_4328_ = lean_ctor_get(v_a_4326_, 0);
lean_inc(v_val_4328_);
lean_dec_ref_known(v_a_4326_, 1);
v___y_4274_ = v___f_4323_;
v___y_4275_ = v___y_4299_;
v___y_4276_ = v___y_4300_;
v___y_4277_ = v___y_4302_;
v___y_4278_ = v___y_4301_;
v___y_4279_ = v___y_4303_;
v___y_4280_ = v___y_4307_;
v___y_4281_ = v___y_4304_;
v___y_4282_ = v___y_4306_;
v___y_4283_ = v___y_4305_;
v_stmt_4284_ = v_val_4328_;
v_ppOk_4285_ = v___x_3794_;
goto v___jp_4273_;
}
}
else
{
lean_object* v_a_4329_; lean_object* v___x_4331_; uint8_t v_isShared_4332_; uint8_t v_isSharedCheck_4336_; 
lean_dec_ref(v___f_4323_);
lean_dec_ref(v___y_4306_);
lean_dec(v___y_4305_);
lean_dec_ref(v___y_4304_);
lean_dec(v___y_4303_);
lean_dec_ref(v___y_4302_);
lean_dec_ref(v___y_4301_);
lean_dec(v___y_4300_);
lean_dec_ref(v___y_4299_);
lean_del_object(v___x_3885_);
lean_dec(v_snd_3883_);
lean_dec(v_fst_3882_);
lean_del_object(v___x_3880_);
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec(v___x_3793_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_dec(v_fst_3777_);
lean_del_object(v___x_3771_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4329_ = lean_ctor_get(v___x_4325_, 0);
v_isSharedCheck_4336_ = !lean_is_exclusive(v___x_4325_);
if (v_isSharedCheck_4336_ == 0)
{
v___x_4331_ = v___x_4325_;
v_isShared_4332_ = v_isSharedCheck_4336_;
goto v_resetjp_4330_;
}
else
{
lean_inc(v_a_4329_);
lean_dec(v___x_4325_);
v___x_4331_ = lean_box(0);
v_isShared_4332_ = v_isSharedCheck_4336_;
goto v_resetjp_4330_;
}
v_resetjp_4330_:
{
lean_object* v___x_4334_; 
if (v_isShared_4332_ == 0)
{
v___x_4334_ = v___x_4331_;
goto v_reusejp_4333_;
}
else
{
lean_object* v_reuseFailAlloc_4335_; 
v_reuseFailAlloc_4335_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4335_, 0, v_a_4329_);
v___x_4334_ = v_reuseFailAlloc_4335_;
goto v_reusejp_4333_;
}
v_reusejp_4333_:
{
return v___x_4334_;
}
}
}
}
else
{
lean_object* v_val_4337_; 
lean_dec_ref_known(v___x_4318_, 7);
lean_dec_ref(v___x_3802_);
v_val_4337_ = lean_ctor_get(v_a_4322_, 0);
lean_inc(v_val_4337_);
lean_dec_ref_known(v_a_4322_, 1);
v___y_4274_ = v___f_4323_;
v___y_4275_ = v___y_4299_;
v___y_4276_ = v___y_4300_;
v___y_4277_ = v___y_4302_;
v___y_4278_ = v___y_4301_;
v___y_4279_ = v___y_4303_;
v___y_4280_ = v___y_4307_;
v___y_4281_ = v___y_4304_;
v___y_4282_ = v___y_4306_;
v___y_4283_ = v___y_4305_;
v_stmt_4284_ = v_val_4337_;
v_ppOk_4285_ = v___x_3794_;
goto v___jp_4273_;
}
}
else
{
lean_object* v_a_4338_; lean_object* v___x_4340_; uint8_t v_isShared_4341_; uint8_t v_isSharedCheck_4345_; 
lean_dec_ref_known(v___x_4318_, 7);
lean_dec_ref(v___y_4306_);
lean_dec(v___y_4305_);
lean_dec_ref(v___y_4304_);
lean_dec(v___y_4303_);
lean_dec_ref(v___y_4302_);
lean_dec_ref(v___y_4301_);
lean_dec(v___y_4300_);
lean_dec_ref(v___y_4299_);
lean_del_object(v___x_3885_);
lean_dec(v_snd_3883_);
lean_dec(v_fst_3882_);
lean_del_object(v___x_3880_);
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec_ref(v___x_3802_);
lean_dec(v___x_3793_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_dec(v_fst_3777_);
lean_del_object(v___x_3771_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4338_ = lean_ctor_get(v___x_4321_, 0);
v_isSharedCheck_4345_ = !lean_is_exclusive(v___x_4321_);
if (v_isSharedCheck_4345_ == 0)
{
v___x_4340_ = v___x_4321_;
v_isShared_4341_ = v_isSharedCheck_4345_;
goto v_resetjp_4339_;
}
else
{
lean_inc(v_a_4338_);
lean_dec(v___x_4321_);
v___x_4340_ = lean_box(0);
v_isShared_4341_ = v_isSharedCheck_4345_;
goto v_resetjp_4339_;
}
v_resetjp_4339_:
{
lean_object* v___x_4343_; 
if (v_isShared_4341_ == 0)
{
v___x_4343_ = v___x_4340_;
goto v_reusejp_4342_;
}
else
{
lean_object* v_reuseFailAlloc_4344_; 
v_reuseFailAlloc_4344_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4344_, 0, v_a_4338_);
v___x_4343_ = v_reuseFailAlloc_4344_;
goto v_reusejp_4342_;
}
v_reusejp_4342_:
{
return v___x_4343_;
}
}
}
}
v___jp_4346_:
{
lean_object* v___x_4355_; 
v___x_4355_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__38));
v___y_4299_ = v___y_4347_;
v___y_4300_ = v___y_4348_;
v___y_4301_ = v___y_4350_;
v___y_4302_ = v___y_4349_;
v___y_4303_ = v___y_4351_;
v___y_4304_ = v___y_4352_;
v___y_4305_ = v___y_4354_;
v___y_4306_ = v___y_4353_;
v___y_4307_ = v___x_4355_;
goto v___jp_4298_;
}
v___jp_4356_:
{
lean_object* v___x_4360_; lean_object* v___x_4361_; size_t v_sz_4362_; lean_object* v___x_4363_; 
v___x_4360_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(v___x_3749_, v_fst_3768_, v___x_3867_);
v___x_4361_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4361_, 0, v_valConsts_4357_);
lean_ctor_set(v___x_4361_, 1, v___x_3814_);
v_sz_4362_ = lean_array_size(v___x_4360_);
lean_inc_ref(v_a_3747_);
v___x_4363_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__15(v_a_3747_, v___x_4360_, v_sz_4362_, v___x_3874_, v___x_4361_);
if (lean_obj_tag(v___x_4363_) == 0)
{
lean_object* v_a_4364_; lean_object* v___x_4365_; lean_object* v_fst_4366_; lean_object* v_snd_4367_; lean_object* v_fst_4368_; lean_object* v_snd_4369_; lean_object* v___x_4370_; 
v_a_4364_ = lean_ctor_get(v___x_4363_, 0);
lean_inc(v_a_4364_);
lean_dec_ref_known(v___x_4363_, 1);
lean_inc_n(v_fst_3768_, 2);
lean_inc_ref_n(v___x_3750_, 2);
v___x_4365_ = l_NsExport_resolveDeps(v___x_3750_, v_fst_3768_, v_fst_3878_);
v_fst_4366_ = lean_ctor_get(v___x_4365_, 0);
lean_inc(v_fst_4366_);
v_snd_4367_ = lean_ctor_get(v___x_4365_, 1);
lean_inc(v_snd_4367_);
lean_dec_ref(v___x_4365_);
v_fst_4368_ = lean_ctor_get(v_a_4364_, 0);
lean_inc(v_fst_4368_);
v_snd_4369_ = lean_ctor_get(v_a_4364_, 1);
lean_inc(v_snd_4369_);
lean_dec(v_a_4364_);
v___x_4370_ = l_NsExport_resolveDeps(v___x_3750_, v_fst_3768_, v_fst_4368_);
switch(lean_obj_tag(v_snd_3769_))
{
case 0:
{
lean_object* v_fst_4371_; lean_object* v_snd_4372_; lean_object* v___x_4373_; 
lean_dec_ref_known(v_snd_3769_, 1);
v_fst_4371_ = lean_ctor_get(v___x_4370_, 0);
lean_inc(v_fst_4371_);
v_snd_4372_ = lean_ctor_get(v___x_4370_, 1);
lean_inc(v_snd_4372_);
lean_dec_ref(v___x_4370_);
v___x_4373_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__39));
v___y_4299_ = v_snd_4367_;
v___y_4300_ = v_snd_4369_;
v___y_4301_ = v___x_4360_;
v___y_4302_ = v_fst_4366_;
v___y_4303_ = v_proofTree_4359_;
v___y_4304_ = v_snd_4372_;
v___y_4305_ = v_proofSize_4358_;
v___y_4306_ = v_fst_4371_;
v___y_4307_ = v___x_4373_;
goto v___jp_4298_;
}
case 2:
{
lean_object* v_fst_4374_; lean_object* v_snd_4375_; lean_object* v___x_4376_; 
lean_dec_ref_known(v_snd_3769_, 1);
v_fst_4374_ = lean_ctor_get(v___x_4370_, 0);
lean_inc(v_fst_4374_);
v_snd_4375_ = lean_ctor_get(v___x_4370_, 1);
lean_inc(v_snd_4375_);
lean_dec_ref(v___x_4370_);
v___x_4376_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__40));
v___y_4299_ = v_snd_4367_;
v___y_4300_ = v_snd_4369_;
v___y_4301_ = v___x_4360_;
v___y_4302_ = v_fst_4366_;
v___y_4303_ = v_proofTree_4359_;
v___y_4304_ = v_snd_4375_;
v___y_4305_ = v_proofSize_4358_;
v___y_4306_ = v_fst_4374_;
v___y_4307_ = v___x_4376_;
goto v___jp_4298_;
}
case 3:
{
lean_object* v_fst_4377_; lean_object* v_snd_4378_; lean_object* v___x_4379_; 
lean_dec_ref_known(v_snd_3769_, 1);
v_fst_4377_ = lean_ctor_get(v___x_4370_, 0);
lean_inc(v_fst_4377_);
v_snd_4378_ = lean_ctor_get(v___x_4370_, 1);
lean_inc(v_snd_4378_);
lean_dec_ref(v___x_4370_);
v___x_4379_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__41));
v___y_4299_ = v_snd_4367_;
v___y_4300_ = v_snd_4369_;
v___y_4301_ = v___x_4360_;
v___y_4302_ = v_fst_4366_;
v___y_4303_ = v_proofTree_4359_;
v___y_4304_ = v_snd_4378_;
v___y_4305_ = v_proofSize_4358_;
v___y_4306_ = v_fst_4377_;
v___y_4307_ = v___x_4379_;
goto v___jp_4298_;
}
case 1:
{
lean_object* v_fst_4380_; lean_object* v_snd_4381_; uint8_t v___x_4382_; 
lean_dec_ref_known(v_snd_3769_, 1);
v_fst_4380_ = lean_ctor_get(v___x_4370_, 0);
lean_inc(v_fst_4380_);
v_snd_4381_ = lean_ctor_get(v___x_4370_, 1);
lean_inc(v_snd_4381_);
lean_dec_ref(v___x_4370_);
lean_inc_ref(v_a_3747_);
v___x_4382_ = l_Lean_Meta_isInstanceCore(v_a_3747_, v_fst_3768_);
if (v___x_4382_ == 0)
{
lean_object* v___x_4383_; lean_object* v___x_4384_; lean_object* v___x_4385_; uint8_t v___x_4386_; 
v___x_4383_ = l_Lean_Expr_getForallBody(v___x_3802_);
v___x_4384_ = l_Lean_Expr_getAppFn(v___x_4383_);
lean_dec_ref(v___x_4383_);
v___x_4385_ = l_Lean_Expr_constName(v___x_4384_);
lean_dec_ref(v___x_4384_);
lean_inc_ref(v_a_3747_);
v___x_4386_ = l_Lean_isClass(v_a_3747_, v___x_4385_);
lean_dec(v___x_4385_);
if (v___x_4386_ == 0)
{
lean_object* v___x_4387_; 
v___x_4387_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__42));
v___y_4299_ = v_snd_4367_;
v___y_4300_ = v_snd_4369_;
v___y_4301_ = v___x_4360_;
v___y_4302_ = v_fst_4366_;
v___y_4303_ = v_proofTree_4359_;
v___y_4304_ = v_snd_4381_;
v___y_4305_ = v_proofSize_4358_;
v___y_4306_ = v_fst_4380_;
v___y_4307_ = v___x_4387_;
goto v___jp_4298_;
}
else
{
v___y_4347_ = v_snd_4367_;
v___y_4348_ = v_snd_4369_;
v___y_4349_ = v_fst_4366_;
v___y_4350_ = v___x_4360_;
v___y_4351_ = v_proofTree_4359_;
v___y_4352_ = v_snd_4381_;
v___y_4353_ = v_fst_4380_;
v___y_4354_ = v_proofSize_4358_;
goto v___jp_4346_;
}
}
else
{
v___y_4347_ = v_snd_4367_;
v___y_4348_ = v_snd_4369_;
v___y_4349_ = v_fst_4366_;
v___y_4350_ = v___x_4360_;
v___y_4351_ = v_proofTree_4359_;
v___y_4352_ = v_snd_4381_;
v___y_4353_ = v_fst_4380_;
v___y_4354_ = v_proofSize_4358_;
goto v___jp_4346_;
}
}
case 5:
{
lean_object* v_fst_4388_; lean_object* v_snd_4389_; uint8_t v___x_4390_; 
lean_dec_ref_known(v_snd_3769_, 1);
v_fst_4388_ = lean_ctor_get(v___x_4370_, 0);
lean_inc(v_fst_4388_);
v_snd_4389_ = lean_ctor_get(v___x_4370_, 1);
lean_inc(v_snd_4389_);
lean_dec_ref(v___x_4370_);
lean_inc(v_fst_3768_);
lean_inc_ref(v_a_3747_);
v___x_4390_ = l_Lean_isStructure(v_a_3747_, v_fst_3768_);
if (v___x_4390_ == 0)
{
lean_object* v___x_4391_; 
v___x_4391_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__43));
v___y_4299_ = v_snd_4367_;
v___y_4300_ = v_snd_4369_;
v___y_4301_ = v___x_4360_;
v___y_4302_ = v_fst_4366_;
v___y_4303_ = v_proofTree_4359_;
v___y_4304_ = v_snd_4389_;
v___y_4305_ = v_proofSize_4358_;
v___y_4306_ = v_fst_4388_;
v___y_4307_ = v___x_4391_;
goto v___jp_4298_;
}
else
{
lean_object* v___x_4392_; 
v___x_4392_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__44));
v___y_4299_ = v_snd_4367_;
v___y_4300_ = v_snd_4369_;
v___y_4301_ = v___x_4360_;
v___y_4302_ = v_fst_4366_;
v___y_4303_ = v_proofTree_4359_;
v___y_4304_ = v_snd_4389_;
v___y_4305_ = v_proofSize_4358_;
v___y_4306_ = v_fst_4388_;
v___y_4307_ = v___x_4392_;
goto v___jp_4298_;
}
}
default: 
{
lean_object* v_fst_4393_; lean_object* v_snd_4394_; lean_object* v___x_4395_; 
lean_dec(v_snd_3769_);
v_fst_4393_ = lean_ctor_get(v___x_4370_, 0);
lean_inc(v_fst_4393_);
v_snd_4394_ = lean_ctor_get(v___x_4370_, 1);
lean_inc(v_snd_4394_);
lean_dec_ref(v___x_4370_);
v___x_4395_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__45));
v___y_4299_ = v_snd_4367_;
v___y_4300_ = v_snd_4369_;
v___y_4301_ = v___x_4360_;
v___y_4302_ = v_fst_4366_;
v___y_4303_ = v_proofTree_4359_;
v___y_4304_ = v_snd_4394_;
v___y_4305_ = v_proofSize_4358_;
v___y_4306_ = v_fst_4393_;
v___y_4307_ = v___x_4395_;
goto v___jp_4298_;
}
}
}
else
{
lean_object* v_a_4396_; lean_object* v___x_4398_; uint8_t v_isShared_4399_; uint8_t v_isSharedCheck_4403_; 
lean_dec(v___x_4360_);
lean_dec(v_proofTree_4359_);
lean_dec(v_proofSize_4358_);
lean_del_object(v___x_3885_);
lean_dec(v_snd_3883_);
lean_dec(v_fst_3882_);
lean_del_object(v___x_3880_);
lean_dec(v_fst_3878_);
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec_ref(v___x_3802_);
lean_dec(v___x_3793_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_dec(v_fst_3777_);
lean_del_object(v___x_3771_);
lean_dec(v_snd_3769_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4396_ = lean_ctor_get(v___x_4363_, 0);
v_isSharedCheck_4403_ = !lean_is_exclusive(v___x_4363_);
if (v_isSharedCheck_4403_ == 0)
{
v___x_4398_ = v___x_4363_;
v_isShared_4399_ = v_isSharedCheck_4403_;
goto v_resetjp_4397_;
}
else
{
lean_inc(v_a_4396_);
lean_dec(v___x_4363_);
v___x_4398_ = lean_box(0);
v_isShared_4399_ = v_isSharedCheck_4403_;
goto v_resetjp_4397_;
}
v_resetjp_4397_:
{
lean_object* v___x_4401_; 
if (v_isShared_4399_ == 0)
{
v___x_4401_ = v___x_4398_;
goto v_reusejp_4400_;
}
else
{
lean_object* v_reuseFailAlloc_4402_; 
v_reuseFailAlloc_4402_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4402_, 0, v_a_4396_);
v___x_4401_ = v_reuseFailAlloc_4402_;
goto v_reusejp_4400_;
}
v_reusejp_4400_:
{
return v___x_4401_;
}
}
}
}
}
}
}
else
{
lean_object* v_a_4413_; lean_object* v___x_4415_; uint8_t v_isShared_4416_; uint8_t v_isSharedCheck_4420_; 
lean_dec(v___x_3868_);
lean_del_object(v___x_3812_);
lean_dec(v_snd_3810_);
lean_del_object(v___x_3807_);
lean_dec_ref(v___x_3802_);
lean_dec(v___x_3801_);
lean_dec(v___x_3793_);
lean_dec(v___x_3792_);
lean_dec(v_snd_3778_);
lean_dec(v_fst_3777_);
lean_del_object(v___x_3771_);
lean_dec(v_snd_3769_);
lean_dec(v_fst_3768_);
lean_dec_ref(v___x_3752_);
lean_dec_ref(v___x_3750_);
lean_dec_ref(v_a_3747_);
v_a_4413_ = lean_ctor_get(v___x_3875_, 0);
v_isSharedCheck_4420_ = !lean_is_exclusive(v___x_3875_);
if (v_isSharedCheck_4420_ == 0)
{
v___x_4415_ = v___x_3875_;
v_isShared_4416_ = v_isSharedCheck_4420_;
goto v_resetjp_4414_;
}
else
{
lean_inc(v_a_4413_);
lean_dec(v___x_3875_);
v___x_4415_ = lean_box(0);
v_isShared_4416_ = v_isSharedCheck_4420_;
goto v_resetjp_4414_;
}
v_resetjp_4414_:
{
lean_object* v___x_4418_; 
if (v_isShared_4416_ == 0)
{
v___x_4418_ = v___x_4415_;
goto v_reusejp_4417_;
}
else
{
lean_object* v_reuseFailAlloc_4419_; 
v_reuseFailAlloc_4419_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4419_, 0, v_a_4413_);
v___x_4418_ = v_reuseFailAlloc_4419_;
goto v_reusejp_4417_;
}
v_reusejp_4417_:
{
return v___x_4418_;
}
}
}
}
}
}
}
}
}
}
}
}
}
v___jp_3759_:
{
size_t v___x_3761_; size_t v___x_3762_; lean_object* v___x_3763_; 
v___x_3761_ = ((size_t)1ULL);
v___x_3762_ = lean_usize_add(v_i_3756_, v___x_3761_);
v___x_3763_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23(v_a_3744_, v_nshards_3745_, v_shard_3746_, v___x_3748_, v_a_3747_, v___x_3749_, v___x_3750_, v_a_3751_, v___x_3752_, v_a_3753_, v_as_3754_, v_sz_3755_, v___x_3762_, v_a_3760_);
return v___x_3763_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17___boxed(lean_object* v_a_4429_, lean_object* v_nshards_4430_, lean_object* v_shard_4431_, lean_object* v_a_4432_, lean_object* v___x_4433_, lean_object* v___x_4434_, lean_object* v___x_4435_, lean_object* v_a_4436_, lean_object* v___x_4437_, lean_object* v_a_4438_, lean_object* v_as_4439_, lean_object* v_sz_4440_, lean_object* v_i_4441_, lean_object* v_b_4442_, lean_object* v___y_4443_){
_start:
{
size_t v_sz_boxed_4444_; size_t v_i_boxed_4445_; lean_object* v_res_4446_; 
v_sz_boxed_4444_ = lean_unbox_usize(v_sz_4440_);
lean_dec(v_sz_4440_);
v_i_boxed_4445_ = lean_unbox_usize(v_i_4441_);
lean_dec(v_i_4441_);
v_res_4446_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17(v_a_4429_, v_nshards_4430_, v_shard_4431_, v_a_4432_, v___x_4433_, v___x_4434_, v___x_4435_, v_a_4436_, v___x_4437_, v_a_4438_, v_as_4439_, v_sz_boxed_4444_, v_i_boxed_4445_, v_b_4442_);
lean_dec_ref(v_as_4439_);
lean_dec(v_a_4438_);
lean_dec(v_a_4436_);
lean_dec_ref(v___x_4434_);
lean_dec_ref(v___x_4433_);
lean_dec(v_shard_4431_);
lean_dec(v_nshards_4430_);
lean_dec_ref(v_a_4429_);
return v_res_4446_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0(void){
_start:
{
size_t v___x_4447_; lean_object* v___x_4448_; lean_object* v___x_4449_; lean_object* v___x_4450_; lean_object* v___x_4451_; lean_object* v___x_4452_; 
v___x_4447_ = ((size_t)5ULL);
v___x_4448_ = lean_unsigned_to_nat(0u);
v___x_4449_ = lean_unsigned_to_nat(32u);
v___x_4450_ = lean_mk_empty_array_with_capacity(v___x_4449_);
v___x_4451_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__0);
v___x_4452_ = lean_alloc_ctor(0, 4, sizeof(size_t)*1);
lean_ctor_set(v___x_4452_, 0, v___x_4451_);
lean_ctor_set(v___x_4452_, 1, v___x_4450_);
lean_ctor_set(v___x_4452_, 2, v___x_4448_);
lean_ctor_set(v___x_4452_, 3, v___x_4448_);
lean_ctor_set_usize(v___x_4452_, 4, v___x_4447_);
return v___x_4452_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1(void){
_start:
{
lean_object* v___x_4453_; lean_object* v___x_4454_; lean_object* v___x_4455_; 
v___x_4453_ = lean_box(1);
v___x_4454_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0);
v___x_4455_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_4455_, 0, v___x_4454_);
lean_ctor_set(v___x_4455_, 1, v___x_4454_);
lean_ctor_set(v___x_4455_, 2, v___x_4453_);
return v___x_4455_;
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3(void){
_start:
{
lean_object* v___x_4460_; uint64_t v___x_4461_; lean_object* v___x_4462_; 
v___x_4460_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0);
v___x_4461_ = 0ULL;
v___x_4462_ = lean_alloc_ctor(0, 1, 8);
lean_ctor_set(v___x_4462_, 0, v___x_4460_);
lean_ctor_set_uint64(v___x_4462_, sizeof(void*)*1, v___x_4461_);
return v___x_4462_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13(lean_object* v_a_4465_, lean_object* v___x_4466_, lean_object* v_as_4467_, size_t v_sz_4468_, size_t v_i_4469_, lean_object* v_b_4470_){
_start:
{
lean_object* v_a_4473_; uint8_t v___x_4477_; 
v___x_4477_ = lean_usize_dec_lt(v_i_4469_, v_sz_4468_);
if (v___x_4477_ == 0)
{
lean_object* v___x_4478_; 
lean_dec_ref(v_a_4465_);
v___x_4478_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_4478_, 0, v_b_4470_);
return v___x_4478_;
}
else
{
lean_object* v_a_4479_; lean_object* v_fst_4480_; lean_object* v___x_4481_; lean_object* v___x_4482_; uint8_t v___x_4483_; 
v_a_4479_ = lean_array_uget_borrowed(v_as_4467_, v_i_4469_);
v_fst_4480_ = lean_ctor_get(v_a_4479_, 0);
v___x_4481_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_b_4470_, v_fst_4480_);
v___x_4482_ = lean_box(0);
v___x_4483_ = l_NsExport_instBEqCls_beq(v___x_4481_, v___x_4482_);
lean_dec(v___x_4481_);
if (v___x_4483_ == 0)
{
v_a_4473_ = v_b_4470_;
goto v___jp_4472_;
}
else
{
uint8_t v___x_4484_; lean_object* v___y_4486_; lean_object* v_a_4487_; lean_object* v___y_4504_; lean_object* v___x_4506_; lean_object* v___x_4507_; lean_object* v___x_4508_; lean_object* v___x_4509_; lean_object* v___x_4510_; lean_object* v___x_4511_; lean_object* v___y_4513_; uint8_t v___y_4514_; lean_object* v___y_4515_; lean_object* v___y_4516_; lean_object* v___y_4517_; lean_object* v___y_4559_; lean_object* v___y_4560_; uint8_t v___y_4561_; lean_object* v___y_4562_; lean_object* v___y_4563_; uint8_t v___y_4564_; lean_object* v___x_4584_; lean_object* v___x_4585_; lean_object* v___x_4586_; lean_object* v___x_4587_; lean_object* v___x_4588_; lean_object* v___y_4590_; lean_object* v___y_4612_; 
v___x_4484_ = 0;
v___x_4506_ = lean_unsigned_to_nat(1u);
v___x_4507_ = lean_unsigned_to_nat(0u);
v___x_4508_ = lean_box(0);
v___x_4509_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_4510_ = l_Lean_instInhabitedFileMap_default;
v___x_4511_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_4584_ = lean_unsigned_to_nat(1000u);
v___x_4585_ = lean_box(0);
v___x_4586_ = lean_box(0);
v___x_4587_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_4588_ = lean_box(0);
if (lean_obj_tag(v_fst_4480_) == 0)
{
v___y_4612_ = v_fst_4480_;
goto v___jp_4611_;
}
else
{
lean_object* v_pre_4617_; 
v_pre_4617_ = lean_ctor_get(v_fst_4480_, 0);
lean_inc(v_pre_4617_);
v___y_4612_ = v_pre_4617_;
goto v___jp_4611_;
}
v___jp_4485_:
{
lean_object* v___x_4488_; 
v___x_4488_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_4465_, v___y_4486_);
if (lean_obj_tag(v___x_4488_) == 0)
{
lean_dec(v_a_4487_);
lean_dec(v___y_4486_);
v_a_4473_ = v_b_4470_;
goto v___jp_4472_;
}
else
{
lean_object* v_val_4489_; lean_object* v___x_4491_; uint8_t v_isShared_4492_; uint8_t v_isSharedCheck_4502_; 
v_val_4489_ = lean_ctor_get(v___x_4488_, 0);
v_isSharedCheck_4502_ = !lean_is_exclusive(v___x_4488_);
if (v_isSharedCheck_4502_ == 0)
{
v___x_4491_ = v___x_4488_;
v_isShared_4492_ = v_isSharedCheck_4502_;
goto v_resetjp_4490_;
}
else
{
lean_inc(v_val_4489_);
lean_dec(v___x_4488_);
v___x_4491_ = lean_box(0);
v_isShared_4492_ = v_isSharedCheck_4502_;
goto v_resetjp_4490_;
}
v_resetjp_4490_:
{
lean_object* v___x_4493_; lean_object* v___x_4494_; uint8_t v___x_4495_; 
v___x_4493_ = lean_box(v___x_4484_);
v___x_4494_ = lean_array_get(v___x_4493_, v___x_4466_, v_val_4489_);
lean_dec(v_val_4489_);
lean_dec(v___x_4493_);
v___x_4495_ = lean_unbox(v___x_4494_);
lean_dec(v___x_4494_);
if (v___x_4495_ == 0)
{
lean_del_object(v___x_4491_);
lean_dec(v_a_4487_);
lean_dec(v___y_4486_);
v_a_4473_ = v_b_4470_;
goto v___jp_4472_;
}
else
{
lean_object* v___x_4496_; uint8_t v___x_4497_; 
v___x_4496_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_b_4470_, v___y_4486_);
v___x_4497_ = l_NsExport_instBEqCls_beq(v___x_4496_, v___x_4482_);
lean_dec(v___x_4496_);
if (v___x_4497_ == 0)
{
if (lean_obj_tag(v_a_4487_) == 0)
{
lean_object* v___x_4499_; 
if (v_isShared_4492_ == 0)
{
lean_ctor_set_tag(v___x_4491_, 3);
lean_ctor_set(v___x_4491_, 0, v___y_4486_);
v___x_4499_ = v___x_4491_;
goto v_reusejp_4498_;
}
else
{
lean_object* v_reuseFailAlloc_4501_; 
v_reuseFailAlloc_4501_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4501_, 0, v___y_4486_);
v___x_4499_ = v_reuseFailAlloc_4501_;
goto v_reusejp_4498_;
}
v_reusejp_4498_:
{
lean_object* v___x_4500_; 
lean_inc(v_fst_4480_);
v___x_4500_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_b_4470_, v_fst_4480_, v___x_4499_);
v_a_4473_ = v___x_4500_;
goto v___jp_4472_;
}
}
else
{
lean_dec_ref_known(v_a_4487_, 1);
lean_del_object(v___x_4491_);
lean_dec(v___y_4486_);
v_a_4473_ = v_b_4470_;
goto v___jp_4472_;
}
}
else
{
lean_del_object(v___x_4491_);
lean_dec(v_a_4487_);
lean_dec(v___y_4486_);
v_a_4473_ = v_b_4470_;
goto v___jp_4472_;
}
}
}
}
}
v___jp_4503_:
{
lean_object* v___x_4505_; 
v___x_4505_ = lean_box(0);
v___y_4486_ = v___y_4504_;
v_a_4487_ = v___x_4505_;
goto v___jp_4485_;
}
v___jp_4512_:
{
lean_object* v_fileName_4518_; lean_object* v_fileMap_4519_; lean_object* v_currRecDepth_4520_; lean_object* v_ref_4521_; lean_object* v_currNamespace_4522_; lean_object* v_openDecls_4523_; lean_object* v_initHeartbeats_4524_; lean_object* v_maxHeartbeats_4525_; lean_object* v_quotContext_4526_; lean_object* v_currMacroScope_4527_; lean_object* v_cancelTk_x3f_4528_; uint8_t v_suppressElabErrors_4529_; lean_object* v_inheritedTraceOptions_4530_; lean_object* v___x_4532_; uint8_t v_isShared_4533_; uint8_t v_isSharedCheck_4555_; 
v_fileName_4518_ = lean_ctor_get(v___y_4516_, 0);
v_fileMap_4519_ = lean_ctor_get(v___y_4516_, 1);
v_currRecDepth_4520_ = lean_ctor_get(v___y_4516_, 3);
v_ref_4521_ = lean_ctor_get(v___y_4516_, 5);
v_currNamespace_4522_ = lean_ctor_get(v___y_4516_, 6);
v_openDecls_4523_ = lean_ctor_get(v___y_4516_, 7);
v_initHeartbeats_4524_ = lean_ctor_get(v___y_4516_, 8);
v_maxHeartbeats_4525_ = lean_ctor_get(v___y_4516_, 9);
v_quotContext_4526_ = lean_ctor_get(v___y_4516_, 10);
v_currMacroScope_4527_ = lean_ctor_get(v___y_4516_, 11);
v_cancelTk_x3f_4528_ = lean_ctor_get(v___y_4516_, 12);
v_suppressElabErrors_4529_ = lean_ctor_get_uint8(v___y_4516_, sizeof(void*)*14 + 1);
v_inheritedTraceOptions_4530_ = lean_ctor_get(v___y_4516_, 13);
v_isSharedCheck_4555_ = !lean_is_exclusive(v___y_4516_);
if (v_isSharedCheck_4555_ == 0)
{
lean_object* v_unused_4556_; lean_object* v_unused_4557_; 
v_unused_4556_ = lean_ctor_get(v___y_4516_, 4);
lean_dec(v_unused_4556_);
v_unused_4557_ = lean_ctor_get(v___y_4516_, 2);
lean_dec(v_unused_4557_);
v___x_4532_ = v___y_4516_;
v_isShared_4533_ = v_isSharedCheck_4555_;
goto v_resetjp_4531_;
}
else
{
lean_inc(v_inheritedTraceOptions_4530_);
lean_inc(v_cancelTk_x3f_4528_);
lean_inc(v_currMacroScope_4527_);
lean_inc(v_quotContext_4526_);
lean_inc(v_maxHeartbeats_4525_);
lean_inc(v_initHeartbeats_4524_);
lean_inc(v_openDecls_4523_);
lean_inc(v_currNamespace_4522_);
lean_inc(v_ref_4521_);
lean_inc(v_currRecDepth_4520_);
lean_inc(v_fileMap_4519_);
lean_inc(v_fileName_4518_);
lean_dec(v___y_4516_);
v___x_4532_ = lean_box(0);
v_isShared_4533_ = v_isSharedCheck_4555_;
goto v_resetjp_4531_;
}
v_resetjp_4531_:
{
lean_object* v___x_4534_; lean_object* v___x_4536_; 
v___x_4534_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18);
if (v_isShared_4533_ == 0)
{
lean_ctor_set(v___x_4532_, 4, v___x_4534_);
lean_ctor_set(v___x_4532_, 2, v___x_4511_);
v___x_4536_ = v___x_4532_;
goto v_reusejp_4535_;
}
else
{
lean_object* v_reuseFailAlloc_4554_; 
v_reuseFailAlloc_4554_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v_reuseFailAlloc_4554_, 0, v_fileName_4518_);
lean_ctor_set(v_reuseFailAlloc_4554_, 1, v_fileMap_4519_);
lean_ctor_set(v_reuseFailAlloc_4554_, 2, v___x_4511_);
lean_ctor_set(v_reuseFailAlloc_4554_, 3, v_currRecDepth_4520_);
lean_ctor_set(v_reuseFailAlloc_4554_, 4, v___x_4534_);
lean_ctor_set(v_reuseFailAlloc_4554_, 5, v_ref_4521_);
lean_ctor_set(v_reuseFailAlloc_4554_, 6, v_currNamespace_4522_);
lean_ctor_set(v_reuseFailAlloc_4554_, 7, v_openDecls_4523_);
lean_ctor_set(v_reuseFailAlloc_4554_, 8, v_initHeartbeats_4524_);
lean_ctor_set(v_reuseFailAlloc_4554_, 9, v_maxHeartbeats_4525_);
lean_ctor_set(v_reuseFailAlloc_4554_, 10, v_quotContext_4526_);
lean_ctor_set(v_reuseFailAlloc_4554_, 11, v_currMacroScope_4527_);
lean_ctor_set(v_reuseFailAlloc_4554_, 12, v_cancelTk_x3f_4528_);
lean_ctor_set(v_reuseFailAlloc_4554_, 13, v_inheritedTraceOptions_4530_);
lean_ctor_set_uint8(v_reuseFailAlloc_4554_, sizeof(void*)*14 + 1, v_suppressElabErrors_4529_);
v___x_4536_ = v_reuseFailAlloc_4554_;
goto v_reusejp_4535_;
}
v_reusejp_4535_:
{
lean_object* v___x_4537_; 
lean_ctor_set_uint8(v___x_4536_, sizeof(void*)*14, v___y_4514_);
lean_inc(v_fst_4480_);
v___x_4537_ = l_Lean_findDeclarationRanges_x3f___at___00Lean_Linter_EnvLinter_sortResults_spec__0(v_fst_4480_, v___x_4536_, v___y_4517_);
lean_dec(v___y_4517_);
lean_dec_ref(v___x_4536_);
if (lean_obj_tag(v___x_4537_) == 0)
{
lean_object* v_a_4538_; lean_object* v___x_4539_; 
v_a_4538_ = lean_ctor_get(v___x_4537_, 0);
lean_inc(v_a_4538_);
lean_dec_ref_known(v___x_4537_, 1);
v___x_4539_ = lean_st_ref_get(v___y_4515_);
lean_dec(v___y_4515_);
lean_dec(v___x_4539_);
if (lean_obj_tag(v_a_4538_) == 0)
{
v___y_4504_ = v___y_4513_;
goto v___jp_4503_;
}
else
{
lean_object* v_val_4540_; lean_object* v___x_4542_; uint8_t v_isShared_4543_; uint8_t v_isSharedCheck_4548_; 
v_val_4540_ = lean_ctor_get(v_a_4538_, 0);
v_isSharedCheck_4548_ = !lean_is_exclusive(v_a_4538_);
if (v_isSharedCheck_4548_ == 0)
{
v___x_4542_ = v_a_4538_;
v_isShared_4543_ = v_isSharedCheck_4548_;
goto v_resetjp_4541_;
}
else
{
lean_inc(v_val_4540_);
lean_dec(v_a_4538_);
v___x_4542_ = lean_box(0);
v_isShared_4543_ = v_isSharedCheck_4548_;
goto v_resetjp_4541_;
}
v_resetjp_4541_:
{
lean_object* v_range_4544_; lean_object* v___x_4546_; 
v_range_4544_ = lean_ctor_get(v_val_4540_, 0);
lean_inc_ref(v_range_4544_);
lean_dec(v_val_4540_);
if (v_isShared_4543_ == 0)
{
lean_ctor_set(v___x_4542_, 0, v_range_4544_);
v___x_4546_ = v___x_4542_;
goto v_reusejp_4545_;
}
else
{
lean_object* v_reuseFailAlloc_4547_; 
v_reuseFailAlloc_4547_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4547_, 0, v_range_4544_);
v___x_4546_ = v_reuseFailAlloc_4547_;
goto v_reusejp_4545_;
}
v_reusejp_4545_:
{
v___y_4486_ = v___y_4513_;
v_a_4487_ = v___x_4546_;
goto v___jp_4485_;
}
}
}
}
else
{
lean_object* v_a_4549_; 
lean_dec(v___y_4515_);
v_a_4549_ = lean_ctor_get(v___x_4537_, 0);
lean_inc(v_a_4549_);
lean_dec_ref_known(v___x_4537_, 1);
if (lean_obj_tag(v_a_4549_) == 0)
{
lean_object* v_msg_4550_; lean_object* v___x_4551_; 
v_msg_4550_ = lean_ctor_get(v_a_4549_, 1);
lean_inc_ref(v_msg_4550_);
lean_dec_ref_known(v_a_4549_, 2);
v___x_4551_ = l_Lean_MessageData_toString(v_msg_4550_);
lean_dec_ref(v___x_4551_);
v___y_4504_ = v___y_4513_;
goto v___jp_4503_;
}
else
{
lean_object* v_id_4552_; lean_object* v___x_4553_; 
v_id_4552_ = lean_ctor_get(v_a_4549_, 0);
lean_inc(v_id_4552_);
lean_dec_ref_known(v_a_4549_, 2);
v___x_4553_ = l_Lean_InternalExceptionId_getName(v_id_4552_);
lean_dec(v_id_4552_);
lean_dec_ref(v___x_4553_);
v___y_4504_ = v___y_4513_;
goto v___jp_4503_;
}
}
}
}
}
v___jp_4558_:
{
if (v___y_4564_ == 0)
{
lean_object* v___x_4565_; lean_object* v_env_4566_; lean_object* v_nextMacroScope_4567_; lean_object* v_ngen_4568_; lean_object* v_auxDeclNGen_4569_; lean_object* v_traceState_4570_; lean_object* v_messages_4571_; lean_object* v_infoState_4572_; lean_object* v_snapshotTasks_4573_; lean_object* v___x_4575_; uint8_t v_isShared_4576_; uint8_t v_isSharedCheck_4582_; 
v___x_4565_ = lean_st_ref_take(v___y_4563_);
v_env_4566_ = lean_ctor_get(v___x_4565_, 0);
v_nextMacroScope_4567_ = lean_ctor_get(v___x_4565_, 1);
v_ngen_4568_ = lean_ctor_get(v___x_4565_, 2);
v_auxDeclNGen_4569_ = lean_ctor_get(v___x_4565_, 3);
v_traceState_4570_ = lean_ctor_get(v___x_4565_, 4);
v_messages_4571_ = lean_ctor_get(v___x_4565_, 6);
v_infoState_4572_ = lean_ctor_get(v___x_4565_, 7);
v_snapshotTasks_4573_ = lean_ctor_get(v___x_4565_, 8);
v_isSharedCheck_4582_ = !lean_is_exclusive(v___x_4565_);
if (v_isSharedCheck_4582_ == 0)
{
lean_object* v_unused_4583_; 
v_unused_4583_ = lean_ctor_get(v___x_4565_, 5);
lean_dec(v_unused_4583_);
v___x_4575_ = v___x_4565_;
v_isShared_4576_ = v_isSharedCheck_4582_;
goto v_resetjp_4574_;
}
else
{
lean_inc(v_snapshotTasks_4573_);
lean_inc(v_infoState_4572_);
lean_inc(v_messages_4571_);
lean_inc(v_traceState_4570_);
lean_inc(v_auxDeclNGen_4569_);
lean_inc(v_ngen_4568_);
lean_inc(v_nextMacroScope_4567_);
lean_inc(v_env_4566_);
lean_dec(v___x_4565_);
v___x_4575_ = lean_box(0);
v_isShared_4576_ = v_isSharedCheck_4582_;
goto v_resetjp_4574_;
}
v_resetjp_4574_:
{
lean_object* v___x_4577_; lean_object* v___x_4579_; 
v___x_4577_ = l_Lean_Kernel_enableDiag(v_env_4566_, v___y_4561_);
lean_inc_ref(v___y_4562_);
if (v_isShared_4576_ == 0)
{
lean_ctor_set(v___x_4575_, 5, v___y_4562_);
lean_ctor_set(v___x_4575_, 0, v___x_4577_);
v___x_4579_ = v___x_4575_;
goto v_reusejp_4578_;
}
else
{
lean_object* v_reuseFailAlloc_4581_; 
v_reuseFailAlloc_4581_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_4581_, 0, v___x_4577_);
lean_ctor_set(v_reuseFailAlloc_4581_, 1, v_nextMacroScope_4567_);
lean_ctor_set(v_reuseFailAlloc_4581_, 2, v_ngen_4568_);
lean_ctor_set(v_reuseFailAlloc_4581_, 3, v_auxDeclNGen_4569_);
lean_ctor_set(v_reuseFailAlloc_4581_, 4, v_traceState_4570_);
lean_ctor_set(v_reuseFailAlloc_4581_, 5, v___y_4562_);
lean_ctor_set(v_reuseFailAlloc_4581_, 6, v_messages_4571_);
lean_ctor_set(v_reuseFailAlloc_4581_, 7, v_infoState_4572_);
lean_ctor_set(v_reuseFailAlloc_4581_, 8, v_snapshotTasks_4573_);
v___x_4579_ = v_reuseFailAlloc_4581_;
goto v_reusejp_4578_;
}
v_reusejp_4578_:
{
lean_object* v___x_4580_; 
v___x_4580_ = lean_st_ref_set(v___y_4563_, v___x_4579_);
lean_inc(v___y_4563_);
v___y_4513_ = v___y_4559_;
v___y_4514_ = v___y_4561_;
v___y_4515_ = v___y_4563_;
v___y_4516_ = v___y_4560_;
v___y_4517_ = v___y_4563_;
goto v___jp_4512_;
}
}
}
else
{
lean_inc(v___y_4563_);
v___y_4513_ = v___y_4559_;
v___y_4514_ = v___y_4561_;
v___y_4515_ = v___y_4563_;
v___y_4516_ = v___y_4560_;
v___y_4517_ = v___y_4563_;
goto v___jp_4512_;
}
}
v___jp_4589_:
{
lean_object* v___x_4591_; lean_object* v___x_4592_; lean_object* v___x_4593_; lean_object* v___x_4594_; lean_object* v___x_4595_; lean_object* v___x_4596_; lean_object* v___x_4597_; lean_object* v___x_4598_; lean_object* v___x_4599_; lean_object* v___x_4600_; lean_object* v___x_4601_; lean_object* v___x_4602_; lean_object* v___x_4603_; lean_object* v___x_4604_; lean_object* v___x_4605_; lean_object* v___x_4606_; lean_object* v___x_4607_; lean_object* v_env_4608_; uint8_t v___x_4609_; uint8_t v___x_4610_; 
v___x_4591_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0);
v___x_4592_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2);
v___x_4593_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3);
v___x_4594_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1);
v___x_4595_ = lean_io_get_num_heartbeats();
v___x_4596_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11));
v___x_4597_ = lean_unsigned_to_nat(2u);
v___x_4598_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__2));
v___x_4599_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3);
v___x_4600_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_4600_, 0, v___x_4592_);
lean_ctor_set(v___x_4600_, 1, v___x_4592_);
lean_ctor_set(v___x_4600_, 2, v___x_4591_);
lean_ctor_set_uint8(v___x_4600_, sizeof(void*)*3, v___x_4483_);
v___x_4601_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__4));
lean_inc_ref(v_a_4465_);
v___x_4602_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_4602_, 0, v_a_4465_);
lean_ctor_set(v___x_4602_, 1, v___x_4597_);
lean_ctor_set(v___x_4602_, 2, v___x_4596_);
lean_ctor_set(v___x_4602_, 3, v___x_4598_);
lean_ctor_set(v___x_4602_, 4, v___x_4599_);
lean_ctor_set(v___x_4602_, 5, v___x_4593_);
lean_ctor_set(v___x_4602_, 6, v___x_4594_);
lean_ctor_set(v___x_4602_, 7, v___x_4600_);
lean_ctor_set(v___x_4602_, 8, v___x_4601_);
v___x_4603_ = lean_st_mk_ref(v___x_4602_);
v___x_4604_ = l_Lean_inheritedTraceOptions;
v___x_4605_ = lean_st_ref_get(v___x_4604_);
v___x_4606_ = lean_st_ref_get(v___x_4603_);
v___x_4607_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_4607_, 0, v___x_4509_);
lean_ctor_set(v___x_4607_, 1, v___x_4510_);
lean_ctor_set(v___x_4607_, 2, v___x_4511_);
lean_ctor_set(v___x_4607_, 3, v___x_4507_);
lean_ctor_set(v___x_4607_, 4, v___x_4584_);
lean_ctor_set(v___x_4607_, 5, v___x_4585_);
lean_ctor_set(v___x_4607_, 6, v___x_4508_);
lean_ctor_set(v___x_4607_, 7, v___x_4586_);
lean_ctor_set(v___x_4607_, 8, v___x_4595_);
lean_ctor_set(v___x_4607_, 9, v___x_4587_);
lean_ctor_set(v___x_4607_, 10, v___x_4508_);
lean_ctor_set(v___x_4607_, 11, v___x_4506_);
lean_ctor_set(v___x_4607_, 12, v___x_4588_);
lean_ctor_set(v___x_4607_, 13, v___x_4605_);
lean_ctor_set_uint8(v___x_4607_, sizeof(void*)*14, v___x_4484_);
lean_ctor_set_uint8(v___x_4607_, sizeof(void*)*14 + 1, v___x_4484_);
v_env_4608_ = lean_ctor_get(v___x_4606_, 0);
lean_inc_ref(v_env_4608_);
lean_dec(v___x_4606_);
v___x_4609_ = lean_uint8_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17);
v___x_4610_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_4608_);
lean_dec_ref(v_env_4608_);
if (v___x_4610_ == 0)
{
if (v___x_4609_ == 0)
{
v___y_4559_ = v___y_4590_;
v___y_4560_ = v___x_4607_;
v___y_4561_ = v___x_4609_;
v___y_4562_ = v___x_4593_;
v___y_4563_ = v___x_4603_;
v___y_4564_ = v___x_4483_;
goto v___jp_4558_;
}
else
{
v___y_4559_ = v___y_4590_;
v___y_4560_ = v___x_4607_;
v___y_4561_ = v___x_4609_;
v___y_4562_ = v___x_4593_;
v___y_4563_ = v___x_4603_;
v___y_4564_ = v___x_4610_;
goto v___jp_4558_;
}
}
else
{
v___y_4559_ = v___y_4590_;
v___y_4560_ = v___x_4607_;
v___y_4561_ = v___x_4609_;
v___y_4562_ = v___x_4593_;
v___y_4563_ = v___x_4603_;
v___y_4564_ = v___x_4609_;
goto v___jp_4558_;
}
}
v___jp_4611_:
{
uint8_t v___x_4613_; 
lean_inc(v___y_4612_);
lean_inc_ref(v_a_4465_);
v___x_4613_ = l_Lean_Environment_contains(v_a_4465_, v___y_4612_, v___x_4483_);
if (v___x_4613_ == 0)
{
uint8_t v___x_4614_; 
v___x_4614_ = l_Lean_isPrivateName(v___y_4612_);
if (v___x_4614_ == 0)
{
v___y_4590_ = v___y_4612_;
goto v___jp_4589_;
}
else
{
lean_object* v___x_4615_; uint8_t v___x_4616_; 
lean_inc(v___y_4612_);
v___x_4615_ = l_Lean_privateToUserName(v___y_4612_);
lean_inc(v___x_4615_);
lean_inc_ref(v_a_4465_);
v___x_4616_ = l_Lean_Environment_contains(v_a_4465_, v___x_4615_, v___x_4483_);
if (v___x_4616_ == 0)
{
lean_dec(v___x_4615_);
v___y_4590_ = v___y_4612_;
goto v___jp_4589_;
}
else
{
lean_dec(v___y_4612_);
v___y_4590_ = v___x_4615_;
goto v___jp_4589_;
}
}
}
else
{
v___y_4590_ = v___y_4612_;
goto v___jp_4589_;
}
}
}
}
v___jp_4472_:
{
size_t v___x_4474_; size_t v___x_4475_; 
v___x_4474_ = ((size_t)1ULL);
v___x_4475_ = lean_usize_add(v_i_4469_, v___x_4474_);
v_i_4469_ = v___x_4475_;
v_b_4470_ = v_a_4473_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___boxed(lean_object* v_a_4618_, lean_object* v___x_4619_, lean_object* v_as_4620_, lean_object* v_sz_4621_, lean_object* v_i_4622_, lean_object* v_b_4623_, lean_object* v___y_4624_){
_start:
{
size_t v_sz_boxed_4625_; size_t v_i_boxed_4626_; lean_object* v_res_4627_; 
v_sz_boxed_4625_ = lean_unbox_usize(v_sz_4621_);
lean_dec(v_sz_4621_);
v_i_boxed_4626_ = lean_unbox_usize(v_i_4622_);
lean_dec(v_i_4622_);
v_res_4627_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13(v_a_4618_, v___x_4619_, v_as_4620_, v_sz_boxed_4625_, v_i_boxed_4626_, v_b_4623_);
lean_dec_ref(v_as_4620_);
lean_dec_ref(v___x_4619_);
return v_res_4627_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10(lean_object* v_a_4628_, lean_object* v___x_4629_, lean_object* v_as_4630_, size_t v_sz_4631_, size_t v_i_4632_, lean_object* v_b_4633_){
_start:
{
lean_object* v_a_4636_; uint8_t v___x_4640_; 
v___x_4640_ = lean_usize_dec_lt(v_i_4632_, v_sz_4631_);
if (v___x_4640_ == 0)
{
lean_object* v___x_4641_; 
lean_dec_ref(v_a_4628_);
v___x_4641_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_4641_, 0, v_b_4633_);
return v___x_4641_;
}
else
{
lean_object* v_a_4642_; lean_object* v_fst_4643_; lean_object* v___x_4644_; lean_object* v___x_4645_; uint8_t v___x_4646_; 
v_a_4642_ = lean_array_uget_borrowed(v_as_4630_, v_i_4632_);
v_fst_4643_ = lean_ctor_get(v_a_4642_, 0);
v___x_4644_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_b_4633_, v_fst_4643_);
v___x_4645_ = lean_box(0);
v___x_4646_ = l_NsExport_instBEqCls_beq(v___x_4644_, v___x_4645_);
lean_dec(v___x_4644_);
if (v___x_4646_ == 0)
{
v_a_4636_ = v_b_4633_;
goto v___jp_4635_;
}
else
{
lean_object* v___x_4647_; lean_object* v___x_4648_; lean_object* v___x_4649_; lean_object* v___x_4650_; lean_object* v___x_4651_; lean_object* v___x_4652_; lean_object* v___x_4653_; lean_object* v___x_4654_; lean_object* v___x_4655_; lean_object* v___x_4656_; uint8_t v___x_4657_; lean_object* v___x_4658_; lean_object* v___y_4660_; lean_object* v_a_4661_; lean_object* v___y_4678_; lean_object* v___y_4680_; uint8_t v___y_4681_; lean_object* v___y_4682_; lean_object* v___y_4683_; lean_object* v___y_4684_; lean_object* v___y_4726_; lean_object* v___y_4727_; uint8_t v___y_4728_; lean_object* v___y_4729_; lean_object* v___y_4730_; uint8_t v___y_4731_; lean_object* v___y_4752_; lean_object* v___y_4776_; 
v___x_4647_ = lean_unsigned_to_nat(1u);
v___x_4648_ = lean_unsigned_to_nat(0u);
v___x_4649_ = lean_box(0);
v___x_4650_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_4651_ = l_Lean_instInhabitedFileMap_default;
v___x_4652_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_4653_ = lean_unsigned_to_nat(1000u);
v___x_4654_ = lean_box(0);
v___x_4655_ = lean_box(0);
v___x_4656_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_4657_ = 0;
v___x_4658_ = lean_box(0);
if (lean_obj_tag(v_fst_4643_) == 0)
{
v___y_4776_ = v_fst_4643_;
goto v___jp_4775_;
}
else
{
lean_object* v_pre_4781_; 
v_pre_4781_ = lean_ctor_get(v_fst_4643_, 0);
lean_inc(v_pre_4781_);
v___y_4776_ = v_pre_4781_;
goto v___jp_4775_;
}
v___jp_4659_:
{
lean_object* v___x_4662_; 
v___x_4662_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_4628_, v___y_4660_);
if (lean_obj_tag(v___x_4662_) == 0)
{
lean_dec(v_a_4661_);
lean_dec(v___y_4660_);
v_a_4636_ = v_b_4633_;
goto v___jp_4635_;
}
else
{
lean_object* v_val_4663_; lean_object* v___x_4665_; uint8_t v_isShared_4666_; uint8_t v_isSharedCheck_4676_; 
v_val_4663_ = lean_ctor_get(v___x_4662_, 0);
v_isSharedCheck_4676_ = !lean_is_exclusive(v___x_4662_);
if (v_isSharedCheck_4676_ == 0)
{
v___x_4665_ = v___x_4662_;
v_isShared_4666_ = v_isSharedCheck_4676_;
goto v_resetjp_4664_;
}
else
{
lean_inc(v_val_4663_);
lean_dec(v___x_4662_);
v___x_4665_ = lean_box(0);
v_isShared_4666_ = v_isSharedCheck_4676_;
goto v_resetjp_4664_;
}
v_resetjp_4664_:
{
lean_object* v___x_4667_; lean_object* v___x_4668_; uint8_t v___x_4669_; 
v___x_4667_ = lean_box(v___x_4657_);
v___x_4668_ = lean_array_get(v___x_4667_, v___x_4629_, v_val_4663_);
lean_dec(v_val_4663_);
lean_dec(v___x_4667_);
v___x_4669_ = lean_unbox(v___x_4668_);
lean_dec(v___x_4668_);
if (v___x_4669_ == 0)
{
lean_del_object(v___x_4665_);
lean_dec(v_a_4661_);
lean_dec(v___y_4660_);
v_a_4636_ = v_b_4633_;
goto v___jp_4635_;
}
else
{
lean_object* v___x_4670_; uint8_t v___x_4671_; 
v___x_4670_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x21___at___00NsExport_main_spec__9(v_b_4633_, v___y_4660_);
v___x_4671_ = l_NsExport_instBEqCls_beq(v___x_4670_, v___x_4645_);
lean_dec(v___x_4670_);
if (v___x_4671_ == 0)
{
if (lean_obj_tag(v_a_4661_) == 0)
{
lean_object* v___x_4673_; 
if (v_isShared_4666_ == 0)
{
lean_ctor_set_tag(v___x_4665_, 3);
lean_ctor_set(v___x_4665_, 0, v___y_4660_);
v___x_4673_ = v___x_4665_;
goto v_reusejp_4672_;
}
else
{
lean_object* v_reuseFailAlloc_4675_; 
v_reuseFailAlloc_4675_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4675_, 0, v___y_4660_);
v___x_4673_ = v_reuseFailAlloc_4675_;
goto v_reusejp_4672_;
}
v_reusejp_4672_:
{
lean_object* v___x_4674_; 
lean_inc(v_fst_4643_);
v___x_4674_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_b_4633_, v_fst_4643_, v___x_4673_);
v_a_4636_ = v___x_4674_;
goto v___jp_4635_;
}
}
else
{
lean_dec_ref_known(v_a_4661_, 1);
lean_del_object(v___x_4665_);
lean_dec(v___y_4660_);
v_a_4636_ = v_b_4633_;
goto v___jp_4635_;
}
}
else
{
lean_del_object(v___x_4665_);
lean_dec(v_a_4661_);
lean_dec(v___y_4660_);
v_a_4636_ = v_b_4633_;
goto v___jp_4635_;
}
}
}
}
}
v___jp_4677_:
{
v___y_4660_ = v___y_4678_;
v_a_4661_ = v___x_4658_;
goto v___jp_4659_;
}
v___jp_4679_:
{
lean_object* v_fileName_4685_; lean_object* v_fileMap_4686_; lean_object* v_currRecDepth_4687_; lean_object* v_ref_4688_; lean_object* v_currNamespace_4689_; lean_object* v_openDecls_4690_; lean_object* v_initHeartbeats_4691_; lean_object* v_maxHeartbeats_4692_; lean_object* v_quotContext_4693_; lean_object* v_currMacroScope_4694_; lean_object* v_cancelTk_x3f_4695_; uint8_t v_suppressElabErrors_4696_; lean_object* v_inheritedTraceOptions_4697_; lean_object* v___x_4699_; uint8_t v_isShared_4700_; uint8_t v_isSharedCheck_4722_; 
v_fileName_4685_ = lean_ctor_get(v___y_4683_, 0);
v_fileMap_4686_ = lean_ctor_get(v___y_4683_, 1);
v_currRecDepth_4687_ = lean_ctor_get(v___y_4683_, 3);
v_ref_4688_ = lean_ctor_get(v___y_4683_, 5);
v_currNamespace_4689_ = lean_ctor_get(v___y_4683_, 6);
v_openDecls_4690_ = lean_ctor_get(v___y_4683_, 7);
v_initHeartbeats_4691_ = lean_ctor_get(v___y_4683_, 8);
v_maxHeartbeats_4692_ = lean_ctor_get(v___y_4683_, 9);
v_quotContext_4693_ = lean_ctor_get(v___y_4683_, 10);
v_currMacroScope_4694_ = lean_ctor_get(v___y_4683_, 11);
v_cancelTk_x3f_4695_ = lean_ctor_get(v___y_4683_, 12);
v_suppressElabErrors_4696_ = lean_ctor_get_uint8(v___y_4683_, sizeof(void*)*14 + 1);
v_inheritedTraceOptions_4697_ = lean_ctor_get(v___y_4683_, 13);
v_isSharedCheck_4722_ = !lean_is_exclusive(v___y_4683_);
if (v_isSharedCheck_4722_ == 0)
{
lean_object* v_unused_4723_; lean_object* v_unused_4724_; 
v_unused_4723_ = lean_ctor_get(v___y_4683_, 4);
lean_dec(v_unused_4723_);
v_unused_4724_ = lean_ctor_get(v___y_4683_, 2);
lean_dec(v_unused_4724_);
v___x_4699_ = v___y_4683_;
v_isShared_4700_ = v_isSharedCheck_4722_;
goto v_resetjp_4698_;
}
else
{
lean_inc(v_inheritedTraceOptions_4697_);
lean_inc(v_cancelTk_x3f_4695_);
lean_inc(v_currMacroScope_4694_);
lean_inc(v_quotContext_4693_);
lean_inc(v_maxHeartbeats_4692_);
lean_inc(v_initHeartbeats_4691_);
lean_inc(v_openDecls_4690_);
lean_inc(v_currNamespace_4689_);
lean_inc(v_ref_4688_);
lean_inc(v_currRecDepth_4687_);
lean_inc(v_fileMap_4686_);
lean_inc(v_fileName_4685_);
lean_dec(v___y_4683_);
v___x_4699_ = lean_box(0);
v_isShared_4700_ = v_isSharedCheck_4722_;
goto v_resetjp_4698_;
}
v_resetjp_4698_:
{
lean_object* v___x_4701_; lean_object* v___x_4703_; 
v___x_4701_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__18);
if (v_isShared_4700_ == 0)
{
lean_ctor_set(v___x_4699_, 4, v___x_4701_);
lean_ctor_set(v___x_4699_, 2, v___x_4652_);
v___x_4703_ = v___x_4699_;
goto v_reusejp_4702_;
}
else
{
lean_object* v_reuseFailAlloc_4721_; 
v_reuseFailAlloc_4721_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v_reuseFailAlloc_4721_, 0, v_fileName_4685_);
lean_ctor_set(v_reuseFailAlloc_4721_, 1, v_fileMap_4686_);
lean_ctor_set(v_reuseFailAlloc_4721_, 2, v___x_4652_);
lean_ctor_set(v_reuseFailAlloc_4721_, 3, v_currRecDepth_4687_);
lean_ctor_set(v_reuseFailAlloc_4721_, 4, v___x_4701_);
lean_ctor_set(v_reuseFailAlloc_4721_, 5, v_ref_4688_);
lean_ctor_set(v_reuseFailAlloc_4721_, 6, v_currNamespace_4689_);
lean_ctor_set(v_reuseFailAlloc_4721_, 7, v_openDecls_4690_);
lean_ctor_set(v_reuseFailAlloc_4721_, 8, v_initHeartbeats_4691_);
lean_ctor_set(v_reuseFailAlloc_4721_, 9, v_maxHeartbeats_4692_);
lean_ctor_set(v_reuseFailAlloc_4721_, 10, v_quotContext_4693_);
lean_ctor_set(v_reuseFailAlloc_4721_, 11, v_currMacroScope_4694_);
lean_ctor_set(v_reuseFailAlloc_4721_, 12, v_cancelTk_x3f_4695_);
lean_ctor_set(v_reuseFailAlloc_4721_, 13, v_inheritedTraceOptions_4697_);
lean_ctor_set_uint8(v_reuseFailAlloc_4721_, sizeof(void*)*14 + 1, v_suppressElabErrors_4696_);
v___x_4703_ = v_reuseFailAlloc_4721_;
goto v_reusejp_4702_;
}
v_reusejp_4702_:
{
lean_object* v___x_4704_; 
lean_ctor_set_uint8(v___x_4703_, sizeof(void*)*14, v___y_4681_);
lean_inc(v_fst_4643_);
v___x_4704_ = l_Lean_findDeclarationRanges_x3f___at___00Lean_Linter_EnvLinter_sortResults_spec__0(v_fst_4643_, v___x_4703_, v___y_4684_);
lean_dec(v___y_4684_);
lean_dec_ref(v___x_4703_);
if (lean_obj_tag(v___x_4704_) == 0)
{
lean_object* v_a_4705_; lean_object* v___x_4706_; 
v_a_4705_ = lean_ctor_get(v___x_4704_, 0);
lean_inc(v_a_4705_);
lean_dec_ref_known(v___x_4704_, 1);
v___x_4706_ = lean_st_ref_get(v___y_4682_);
lean_dec(v___y_4682_);
lean_dec(v___x_4706_);
if (lean_obj_tag(v_a_4705_) == 0)
{
v___y_4678_ = v___y_4680_;
goto v___jp_4677_;
}
else
{
lean_object* v_val_4707_; lean_object* v___x_4709_; uint8_t v_isShared_4710_; uint8_t v_isSharedCheck_4715_; 
v_val_4707_ = lean_ctor_get(v_a_4705_, 0);
v_isSharedCheck_4715_ = !lean_is_exclusive(v_a_4705_);
if (v_isSharedCheck_4715_ == 0)
{
v___x_4709_ = v_a_4705_;
v_isShared_4710_ = v_isSharedCheck_4715_;
goto v_resetjp_4708_;
}
else
{
lean_inc(v_val_4707_);
lean_dec(v_a_4705_);
v___x_4709_ = lean_box(0);
v_isShared_4710_ = v_isSharedCheck_4715_;
goto v_resetjp_4708_;
}
v_resetjp_4708_:
{
lean_object* v_range_4711_; lean_object* v___x_4713_; 
v_range_4711_ = lean_ctor_get(v_val_4707_, 0);
lean_inc_ref(v_range_4711_);
lean_dec(v_val_4707_);
if (v_isShared_4710_ == 0)
{
lean_ctor_set(v___x_4709_, 0, v_range_4711_);
v___x_4713_ = v___x_4709_;
goto v_reusejp_4712_;
}
else
{
lean_object* v_reuseFailAlloc_4714_; 
v_reuseFailAlloc_4714_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_4714_, 0, v_range_4711_);
v___x_4713_ = v_reuseFailAlloc_4714_;
goto v_reusejp_4712_;
}
v_reusejp_4712_:
{
v___y_4660_ = v___y_4680_;
v_a_4661_ = v___x_4713_;
goto v___jp_4659_;
}
}
}
}
else
{
lean_object* v_a_4716_; 
lean_dec(v___y_4682_);
v_a_4716_ = lean_ctor_get(v___x_4704_, 0);
lean_inc(v_a_4716_);
lean_dec_ref_known(v___x_4704_, 1);
if (lean_obj_tag(v_a_4716_) == 0)
{
lean_object* v_msg_4717_; lean_object* v___x_4718_; 
v_msg_4717_ = lean_ctor_get(v_a_4716_, 1);
lean_inc_ref(v_msg_4717_);
lean_dec_ref_known(v_a_4716_, 2);
v___x_4718_ = l_Lean_MessageData_toString(v_msg_4717_);
lean_dec_ref(v___x_4718_);
v___y_4678_ = v___y_4680_;
goto v___jp_4677_;
}
else
{
lean_object* v_id_4719_; lean_object* v___x_4720_; 
v_id_4719_ = lean_ctor_get(v_a_4716_, 0);
lean_inc(v_id_4719_);
lean_dec_ref_known(v_a_4716_, 2);
v___x_4720_ = l_Lean_InternalExceptionId_getName(v_id_4719_);
lean_dec(v_id_4719_);
lean_dec_ref(v___x_4720_);
v___y_4678_ = v___y_4680_;
goto v___jp_4677_;
}
}
}
}
}
v___jp_4725_:
{
if (v___y_4731_ == 0)
{
lean_object* v___x_4732_; lean_object* v_env_4733_; lean_object* v_nextMacroScope_4734_; lean_object* v_ngen_4735_; lean_object* v_auxDeclNGen_4736_; lean_object* v_traceState_4737_; lean_object* v_messages_4738_; lean_object* v_infoState_4739_; lean_object* v_snapshotTasks_4740_; lean_object* v___x_4742_; uint8_t v_isShared_4743_; uint8_t v_isSharedCheck_4749_; 
v___x_4732_ = lean_st_ref_take(v___y_4729_);
v_env_4733_ = lean_ctor_get(v___x_4732_, 0);
v_nextMacroScope_4734_ = lean_ctor_get(v___x_4732_, 1);
v_ngen_4735_ = lean_ctor_get(v___x_4732_, 2);
v_auxDeclNGen_4736_ = lean_ctor_get(v___x_4732_, 3);
v_traceState_4737_ = lean_ctor_get(v___x_4732_, 4);
v_messages_4738_ = lean_ctor_get(v___x_4732_, 6);
v_infoState_4739_ = lean_ctor_get(v___x_4732_, 7);
v_snapshotTasks_4740_ = lean_ctor_get(v___x_4732_, 8);
v_isSharedCheck_4749_ = !lean_is_exclusive(v___x_4732_);
if (v_isSharedCheck_4749_ == 0)
{
lean_object* v_unused_4750_; 
v_unused_4750_ = lean_ctor_get(v___x_4732_, 5);
lean_dec(v_unused_4750_);
v___x_4742_ = v___x_4732_;
v_isShared_4743_ = v_isSharedCheck_4749_;
goto v_resetjp_4741_;
}
else
{
lean_inc(v_snapshotTasks_4740_);
lean_inc(v_infoState_4739_);
lean_inc(v_messages_4738_);
lean_inc(v_traceState_4737_);
lean_inc(v_auxDeclNGen_4736_);
lean_inc(v_ngen_4735_);
lean_inc(v_nextMacroScope_4734_);
lean_inc(v_env_4733_);
lean_dec(v___x_4732_);
v___x_4742_ = lean_box(0);
v_isShared_4743_ = v_isSharedCheck_4749_;
goto v_resetjp_4741_;
}
v_resetjp_4741_:
{
lean_object* v___x_4744_; lean_object* v___x_4746_; 
v___x_4744_ = l_Lean_Kernel_enableDiag(v_env_4733_, v___y_4728_);
lean_inc_ref(v___y_4726_);
if (v_isShared_4743_ == 0)
{
lean_ctor_set(v___x_4742_, 5, v___y_4726_);
lean_ctor_set(v___x_4742_, 0, v___x_4744_);
v___x_4746_ = v___x_4742_;
goto v_reusejp_4745_;
}
else
{
lean_object* v_reuseFailAlloc_4748_; 
v_reuseFailAlloc_4748_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_4748_, 0, v___x_4744_);
lean_ctor_set(v_reuseFailAlloc_4748_, 1, v_nextMacroScope_4734_);
lean_ctor_set(v_reuseFailAlloc_4748_, 2, v_ngen_4735_);
lean_ctor_set(v_reuseFailAlloc_4748_, 3, v_auxDeclNGen_4736_);
lean_ctor_set(v_reuseFailAlloc_4748_, 4, v_traceState_4737_);
lean_ctor_set(v_reuseFailAlloc_4748_, 5, v___y_4726_);
lean_ctor_set(v_reuseFailAlloc_4748_, 6, v_messages_4738_);
lean_ctor_set(v_reuseFailAlloc_4748_, 7, v_infoState_4739_);
lean_ctor_set(v_reuseFailAlloc_4748_, 8, v_snapshotTasks_4740_);
v___x_4746_ = v_reuseFailAlloc_4748_;
goto v_reusejp_4745_;
}
v_reusejp_4745_:
{
lean_object* v___x_4747_; 
v___x_4747_ = lean_st_ref_set(v___y_4729_, v___x_4746_);
lean_inc(v___y_4729_);
v___y_4680_ = v___y_4727_;
v___y_4681_ = v___y_4728_;
v___y_4682_ = v___y_4729_;
v___y_4683_ = v___y_4730_;
v___y_4684_ = v___y_4729_;
goto v___jp_4679_;
}
}
}
else
{
lean_inc(v___y_4729_);
v___y_4680_ = v___y_4727_;
v___y_4681_ = v___y_4728_;
v___y_4682_ = v___y_4729_;
v___y_4683_ = v___y_4730_;
v___y_4684_ = v___y_4729_;
goto v___jp_4679_;
}
}
v___jp_4751_:
{
lean_object* v___x_4753_; lean_object* v___x_4754_; lean_object* v___x_4755_; lean_object* v___x_4756_; lean_object* v___x_4757_; lean_object* v___x_4758_; lean_object* v___x_4759_; lean_object* v___x_4760_; lean_object* v___x_4761_; lean_object* v___x_4762_; lean_object* v___x_4763_; lean_object* v___x_4764_; lean_object* v___x_4765_; lean_object* v___x_4766_; lean_object* v___x_4767_; lean_object* v___x_4768_; lean_object* v___x_4769_; lean_object* v___x_4770_; lean_object* v___x_4771_; lean_object* v_env_4772_; uint8_t v___x_4773_; uint8_t v___x_4774_; 
v___x_4753_ = lean_unsigned_to_nat(32u);
v___x_4754_ = lean_mk_empty_array_with_capacity(v___x_4753_);
lean_dec_ref(v___x_4754_);
v___x_4755_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0);
v___x_4756_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2);
v___x_4757_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3);
v___x_4758_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1);
v___x_4759_ = lean_io_get_num_heartbeats();
v___x_4760_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11));
v___x_4761_ = lean_unsigned_to_nat(2u);
v___x_4762_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__2));
v___x_4763_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3);
v___x_4764_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_4764_, 0, v___x_4756_);
lean_ctor_set(v___x_4764_, 1, v___x_4756_);
lean_ctor_set(v___x_4764_, 2, v___x_4755_);
lean_ctor_set_uint8(v___x_4764_, sizeof(void*)*3, v___x_4646_);
v___x_4765_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__4));
lean_inc_ref(v_a_4628_);
v___x_4766_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_4766_, 0, v_a_4628_);
lean_ctor_set(v___x_4766_, 1, v___x_4761_);
lean_ctor_set(v___x_4766_, 2, v___x_4760_);
lean_ctor_set(v___x_4766_, 3, v___x_4762_);
lean_ctor_set(v___x_4766_, 4, v___x_4763_);
lean_ctor_set(v___x_4766_, 5, v___x_4757_);
lean_ctor_set(v___x_4766_, 6, v___x_4758_);
lean_ctor_set(v___x_4766_, 7, v___x_4764_);
lean_ctor_set(v___x_4766_, 8, v___x_4765_);
v___x_4767_ = lean_st_mk_ref(v___x_4766_);
v___x_4768_ = l_Lean_inheritedTraceOptions;
v___x_4769_ = lean_st_ref_get(v___x_4768_);
v___x_4770_ = lean_st_ref_get(v___x_4767_);
v___x_4771_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_4771_, 0, v___x_4650_);
lean_ctor_set(v___x_4771_, 1, v___x_4651_);
lean_ctor_set(v___x_4771_, 2, v___x_4652_);
lean_ctor_set(v___x_4771_, 3, v___x_4648_);
lean_ctor_set(v___x_4771_, 4, v___x_4653_);
lean_ctor_set(v___x_4771_, 5, v___x_4654_);
lean_ctor_set(v___x_4771_, 6, v___x_4649_);
lean_ctor_set(v___x_4771_, 7, v___x_4655_);
lean_ctor_set(v___x_4771_, 8, v___x_4759_);
lean_ctor_set(v___x_4771_, 9, v___x_4656_);
lean_ctor_set(v___x_4771_, 10, v___x_4649_);
lean_ctor_set(v___x_4771_, 11, v___x_4647_);
lean_ctor_set(v___x_4771_, 12, v___x_4658_);
lean_ctor_set(v___x_4771_, 13, v___x_4769_);
lean_ctor_set_uint8(v___x_4771_, sizeof(void*)*14, v___x_4657_);
lean_ctor_set_uint8(v___x_4771_, sizeof(void*)*14 + 1, v___x_4657_);
v_env_4772_ = lean_ctor_get(v___x_4770_, 0);
lean_inc_ref(v_env_4772_);
lean_dec(v___x_4770_);
v___x_4773_ = lean_uint8_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17);
v___x_4774_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_4772_);
lean_dec_ref(v_env_4772_);
if (v___x_4774_ == 0)
{
if (v___x_4773_ == 0)
{
v___y_4726_ = v___x_4757_;
v___y_4727_ = v___y_4752_;
v___y_4728_ = v___x_4773_;
v___y_4729_ = v___x_4767_;
v___y_4730_ = v___x_4771_;
v___y_4731_ = v___x_4646_;
goto v___jp_4725_;
}
else
{
v___y_4726_ = v___x_4757_;
v___y_4727_ = v___y_4752_;
v___y_4728_ = v___x_4773_;
v___y_4729_ = v___x_4767_;
v___y_4730_ = v___x_4771_;
v___y_4731_ = v___x_4774_;
goto v___jp_4725_;
}
}
else
{
v___y_4726_ = v___x_4757_;
v___y_4727_ = v___y_4752_;
v___y_4728_ = v___x_4773_;
v___y_4729_ = v___x_4767_;
v___y_4730_ = v___x_4771_;
v___y_4731_ = v___x_4773_;
goto v___jp_4725_;
}
}
v___jp_4775_:
{
uint8_t v___x_4777_; 
lean_inc(v___y_4776_);
lean_inc_ref(v_a_4628_);
v___x_4777_ = l_Lean_Environment_contains(v_a_4628_, v___y_4776_, v___x_4646_);
if (v___x_4777_ == 0)
{
uint8_t v___x_4778_; 
v___x_4778_ = l_Lean_isPrivateName(v___y_4776_);
if (v___x_4778_ == 0)
{
v___y_4752_ = v___y_4776_;
goto v___jp_4751_;
}
else
{
lean_object* v___x_4779_; uint8_t v___x_4780_; 
lean_inc(v___y_4776_);
v___x_4779_ = l_Lean_privateToUserName(v___y_4776_);
lean_inc(v___x_4779_);
lean_inc_ref(v_a_4628_);
v___x_4780_ = l_Lean_Environment_contains(v_a_4628_, v___x_4779_, v___x_4646_);
if (v___x_4780_ == 0)
{
lean_dec(v___x_4779_);
v___y_4752_ = v___y_4776_;
goto v___jp_4751_;
}
else
{
lean_dec(v___y_4776_);
v___y_4752_ = v___x_4779_;
goto v___jp_4751_;
}
}
}
else
{
v___y_4752_ = v___y_4776_;
goto v___jp_4751_;
}
}
}
}
v___jp_4635_:
{
size_t v___x_4637_; size_t v___x_4638_; lean_object* v___x_4639_; 
v___x_4637_ = ((size_t)1ULL);
v___x_4638_ = lean_usize_add(v_i_4632_, v___x_4637_);
v___x_4639_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13(v_a_4628_, v___x_4629_, v_as_4630_, v_sz_4631_, v___x_4638_, v_a_4636_);
return v___x_4639_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10___boxed(lean_object* v_a_4782_, lean_object* v___x_4783_, lean_object* v_as_4784_, lean_object* v_sz_4785_, lean_object* v_i_4786_, lean_object* v_b_4787_, lean_object* v___y_4788_){
_start:
{
size_t v_sz_boxed_4789_; size_t v_i_boxed_4790_; lean_object* v_res_4791_; 
v_sz_boxed_4789_ = lean_unbox_usize(v_sz_4785_);
lean_dec(v_sz_4785_);
v_i_boxed_4790_ = lean_unbox_usize(v_i_4786_);
lean_dec(v_i_4786_);
v_res_4791_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10(v_a_4782_, v___x_4783_, v_as_4784_, v_sz_boxed_4789_, v_i_boxed_4790_, v_b_4787_);
lean_dec_ref(v_as_4784_);
lean_dec_ref(v___x_4783_);
return v_res_4791_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___redArg(lean_object* v___y_4792_, lean_object* v_a_4793_, lean_object* v___x_4794_, lean_object* v_range_4795_, lean_object* v_b_4796_, lean_object* v_i_4797_){
_start:
{
lean_object* v_stop_4799_; lean_object* v_step_4800_; uint8_t v___x_4801_; 
v_stop_4799_ = lean_ctor_get(v_range_4795_, 1);
v_step_4800_ = lean_ctor_get(v_range_4795_, 2);
v___x_4801_ = lean_nat_dec_lt(v_i_4797_, v_stop_4799_);
if (v___x_4801_ == 0)
{
lean_object* v___x_4802_; 
lean_dec(v_i_4797_);
lean_dec_ref(v_a_4793_);
v___x_4802_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_4802_, 0, v_b_4796_);
return v___x_4802_;
}
else
{
size_t v_sz_4803_; size_t v___x_4804_; lean_object* v___x_4805_; 
v_sz_4803_ = lean_array_size(v___y_4792_);
v___x_4804_ = ((size_t)0ULL);
lean_inc_ref(v_a_4793_);
v___x_4805_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10(v_a_4793_, v___x_4794_, v___y_4792_, v_sz_4803_, v___x_4804_, v_b_4796_);
if (lean_obj_tag(v___x_4805_) == 0)
{
lean_object* v_a_4806_; lean_object* v___x_4807_; 
v_a_4806_ = lean_ctor_get(v___x_4805_, 0);
lean_inc(v_a_4806_);
lean_dec_ref_known(v___x_4805_, 1);
v___x_4807_ = lean_nat_add(v_i_4797_, v_step_4800_);
lean_dec(v_i_4797_);
v_b_4796_ = v_a_4806_;
v_i_4797_ = v___x_4807_;
goto _start;
}
else
{
lean_dec(v_i_4797_);
lean_dec_ref(v_a_4793_);
return v___x_4805_;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___redArg___boxed(lean_object* v___y_4809_, lean_object* v_a_4810_, lean_object* v___x_4811_, lean_object* v_range_4812_, lean_object* v_b_4813_, lean_object* v_i_4814_, lean_object* v___y_4815_){
_start:
{
lean_object* v_res_4816_; 
v_res_4816_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___redArg(v___y_4809_, v_a_4810_, v___x_4811_, v_range_4812_, v_b_4813_, v_i_4814_);
lean_dec_ref(v_range_4812_);
lean_dec_ref(v___x_4811_);
lean_dec_ref(v___y_4809_);
return v_res_4816_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__23(lean_object* v_as_4817_, size_t v_i_4818_, size_t v_stop_4819_, lean_object* v_b_4820_){
_start:
{
lean_object* v___y_4822_; uint8_t v___x_4826_; 
v___x_4826_ = lean_usize_dec_eq(v_i_4818_, v_stop_4819_);
if (v___x_4826_ == 0)
{
lean_object* v___x_4827_; lean_object* v___x_4830_; uint8_t v___x_4831_; 
v___x_4827_ = lean_array_uget_borrowed(v_as_4817_, v_i_4818_);
v___x_4830_ = ((lean_object*)(l_NsExport_hexOf___closed__0));
v___x_4831_ = lean_string_dec_eq(v___x_4827_, v___x_4830_);
if (v___x_4831_ == 0)
{
goto v___jp_4828_;
}
else
{
if (v___x_4826_ == 0)
{
v___y_4822_ = v_b_4820_;
goto v___jp_4821_;
}
else
{
goto v___jp_4828_;
}
}
v___jp_4828_:
{
lean_object* v___x_4829_; 
lean_inc(v___x_4827_);
v___x_4829_ = lean_array_push(v_b_4820_, v___x_4827_);
v___y_4822_ = v___x_4829_;
goto v___jp_4821_;
}
}
else
{
return v_b_4820_;
}
v___jp_4821_:
{
size_t v___x_4823_; size_t v___x_4824_; 
v___x_4823_ = ((size_t)1ULL);
v___x_4824_ = lean_usize_add(v_i_4818_, v___x_4823_);
v_i_4818_ = v___x_4824_;
v_b_4820_ = v___y_4822_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__23___boxed(lean_object* v_as_4832_, lean_object* v_i_4833_, lean_object* v_stop_4834_, lean_object* v_b_4835_){
_start:
{
size_t v_i_boxed_4836_; size_t v_stop_boxed_4837_; lean_object* v_res_4838_; 
v_i_boxed_4836_ = lean_unbox_usize(v_i_4833_);
lean_dec(v_i_4833_);
v_stop_boxed_4837_ = lean_unbox_usize(v_stop_4834_);
lean_dec(v_stop_4834_);
v_res_4838_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__23(v_as_4832_, v_i_boxed_4836_, v_stop_boxed_4837_, v_b_4835_);
lean_dec_ref(v_as_4832_);
return v_res_4838_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__1(size_t v_sz_4839_, size_t v_i_4840_, lean_object* v_bs_4841_){
_start:
{
uint8_t v___x_4842_; 
v___x_4842_ = lean_usize_dec_lt(v_i_4840_, v_sz_4839_);
if (v___x_4842_ == 0)
{
return v_bs_4841_;
}
else
{
lean_object* v_v_4843_; lean_object* v___x_4844_; lean_object* v_bs_x27_4845_; uint8_t v___x_4846_; lean_object* v___x_4847_; size_t v___x_4848_; size_t v___x_4849_; lean_object* v___x_4850_; 
v_v_4843_ = lean_array_uget(v_bs_4841_, v_i_4840_);
v___x_4844_ = lean_unsigned_to_nat(0u);
v_bs_x27_4845_ = lean_array_uset(v_bs_4841_, v_i_4840_, v___x_4844_);
v___x_4846_ = 0;
v___x_4847_ = lean_alloc_ctor(0, 1, 3);
lean_ctor_set(v___x_4847_, 0, v_v_4843_);
lean_ctor_set_uint8(v___x_4847_, sizeof(void*)*1, v___x_4846_);
lean_ctor_set_uint8(v___x_4847_, sizeof(void*)*1 + 1, v___x_4842_);
lean_ctor_set_uint8(v___x_4847_, sizeof(void*)*1 + 2, v___x_4846_);
v___x_4848_ = ((size_t)1ULL);
v___x_4849_ = lean_usize_add(v_i_4840_, v___x_4848_);
v___x_4850_ = lean_array_uset(v_bs_x27_4845_, v_i_4840_, v___x_4847_);
v_i_4840_ = v___x_4849_;
v_bs_4841_ = v___x_4850_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__1___boxed(lean_object* v_sz_4852_, lean_object* v_i_4853_, lean_object* v_bs_4854_){
_start:
{
size_t v_sz_boxed_4855_; size_t v_i_boxed_4856_; lean_object* v_res_4857_; 
v_sz_boxed_4855_ = lean_unbox_usize(v_sz_4852_);
lean_dec(v_sz_4852_);
v_i_boxed_4856_ = lean_unbox_usize(v_i_4853_);
lean_dec(v_i_4853_);
v_res_4857_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__1(v_sz_boxed_4855_, v_i_boxed_4856_, v_bs_4854_);
return v_res_4857_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__19(size_t v_sz_4858_, size_t v_i_4859_, lean_object* v_bs_4860_){
_start:
{
uint8_t v___x_4861_; 
v___x_4861_ = lean_usize_dec_lt(v_i_4859_, v_sz_4858_);
if (v___x_4861_ == 0)
{
return v_bs_4860_;
}
else
{
lean_object* v_v_4862_; lean_object* v___x_4863_; lean_object* v_bs_x27_4864_; lean_object* v___x_4865_; size_t v___x_4866_; size_t v___x_4867_; lean_object* v___x_4868_; 
v_v_4862_ = lean_array_uget(v_bs_4860_, v_i_4859_);
v___x_4863_ = lean_unsigned_to_nat(0u);
v_bs_x27_4864_ = lean_array_uset(v_bs_4860_, v_i_4859_, v___x_4863_);
v___x_4865_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_v_4862_, v___x_4861_);
v___x_4866_ = ((size_t)1ULL);
v___x_4867_ = lean_usize_add(v_i_4859_, v___x_4866_);
v___x_4868_ = lean_array_uset(v_bs_x27_4864_, v_i_4859_, v___x_4865_);
v_i_4859_ = v___x_4867_;
v_bs_4860_ = v___x_4868_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__19___boxed(lean_object* v_sz_4870_, lean_object* v_i_4871_, lean_object* v_bs_4872_){
_start:
{
size_t v_sz_boxed_4873_; size_t v_i_boxed_4874_; lean_object* v_res_4875_; 
v_sz_boxed_4873_ = lean_unbox_usize(v_sz_4870_);
lean_dec(v_sz_4870_);
v_i_boxed_4874_ = lean_unbox_usize(v_i_4871_);
lean_dec(v_i_4871_);
v_res_4875_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__19(v_sz_boxed_4873_, v_i_boxed_4874_, v_bs_4872_);
return v_res_4875_;
}
}
static lean_object* _init_l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5(void){
_start:
{
lean_object* v___x_4886_; lean_object* v___x_4887_; uint8_t v___x_4888_; lean_object* v___x_4889_; 
v___x_4886_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__0);
v___x_4887_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__2);
v___x_4888_ = 1;
v___x_4889_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_4889_, 0, v___x_4887_);
lean_ctor_set(v___x_4889_, 1, v___x_4887_);
lean_ctor_set(v___x_4889_, 2, v___x_4886_);
lean_ctor_set_uint8(v___x_4889_, sizeof(void*)*3, v___x_4888_);
return v___x_4889_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg(lean_object* v_a_4890_, lean_object* v_as_x27_4891_, lean_object* v_b_4892_){
_start:
{
if (lean_obj_tag(v_as_x27_4891_) == 0)
{
lean_object* v___x_4894_; 
lean_dec_ref(v_a_4890_);
v___x_4894_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_4894_, 0, v_b_4892_);
return v___x_4894_;
}
else
{
lean_object* v_head_4895_; lean_object* v_tail_4896_; uint8_t v___x_4897_; lean_object* v___x_4898_; lean_object* v___y_4900_; lean_object* v___y_4907_; lean_object* v___y_4908_; lean_object* v___y_4909_; lean_object* v___y_4910_; lean_object* v___y_4913_; lean_object* v___y_4914_; lean_object* v___y_4915_; lean_object* v___y_4916_; lean_object* v___x_4918_; uint8_t v___x_4919_; 
v_head_4895_ = lean_ctor_get(v_as_x27_4891_, 0);
v_tail_4896_ = lean_ctor_get(v_as_x27_4891_, 1);
v___x_4897_ = 1;
v___x_4898_ = lean_box(0);
lean_inc(v_head_4895_);
v___x_4918_ = l_String_toName(v_head_4895_);
lean_inc(v___x_4918_);
lean_inc_ref(v_a_4890_);
v___x_4919_ = l_Lean_Environment_contains(v_a_4890_, v___x_4918_, v___x_4897_);
if (v___x_4919_ == 0)
{
lean_object* v___x_4920_; lean_object* v___x_4921_; lean_object* v___x_4922_; lean_object* v___x_4923_; 
lean_dec(v___x_4918_);
v___x_4920_ = ((lean_object*)(l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__3));
lean_inc(v_head_4895_);
v___x_4921_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4921_, 0, v_head_4895_);
lean_ctor_set(v___x_4921_, 1, v___x_4920_);
v___x_4922_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_4922_, 0, v___x_4921_);
lean_ctor_set(v___x_4922_, 1, v___x_4898_);
v___x_4923_ = l_List_appendTR___redArg(v_b_4892_, v___x_4922_);
v_as_x27_4891_ = v_tail_4896_;
v_b_4892_ = v___x_4923_;
goto _start;
}
else
{
lean_object* v___x_4925_; lean_object* v___x_4926_; lean_object* v___x_4927_; lean_object* v___x_4928_; lean_object* v___x_4929_; lean_object* v___x_4930_; lean_object* v___x_4931_; lean_object* v___x_4932_; lean_object* v___x_4933_; lean_object* v___x_4934_; lean_object* v___x_4935_; lean_object* v___x_4936_; lean_object* v___x_4937_; lean_object* v___x_4938_; lean_object* v___y_4940_; lean_object* v___y_4941_; lean_object* v___x_4952_; lean_object* v___x_4953_; lean_object* v___x_4954_; lean_object* v___x_4955_; lean_object* v___x_4956_; lean_object* v___x_4957_; lean_object* v___x_4958_; lean_object* v___x_4959_; lean_object* v___x_4960_; uint8_t v___x_4961_; lean_object* v___x_4962_; lean_object* v___x_4963_; lean_object* v_env_4964_; uint8_t v___x_4965_; uint8_t v___y_4967_; uint8_t v___x_4987_; 
v___x_4925_ = lean_unsigned_to_nat(0u);
v___x_4926_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3);
v___x_4927_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1);
v___x_4928_ = lean_io_get_num_heartbeats();
v___x_4929_ = lean_unsigned_to_nat(1u);
v___x_4930_ = lean_box(0);
v___x_4931_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11));
v___x_4932_ = lean_unsigned_to_nat(2u);
v___x_4933_ = ((lean_object*)(l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__4));
v___x_4934_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3);
v___x_4935_ = lean_obj_once(&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5, &l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5_once, _init_l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5);
v___x_4936_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__4));
lean_inc_ref(v_a_4890_);
v___x_4937_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_4937_, 0, v_a_4890_);
lean_ctor_set(v___x_4937_, 1, v___x_4932_);
lean_ctor_set(v___x_4937_, 2, v___x_4931_);
lean_ctor_set(v___x_4937_, 3, v___x_4933_);
lean_ctor_set(v___x_4937_, 4, v___x_4934_);
lean_ctor_set(v___x_4937_, 5, v___x_4926_);
lean_ctor_set(v___x_4937_, 6, v___x_4927_);
lean_ctor_set(v___x_4937_, 7, v___x_4935_);
lean_ctor_set(v___x_4937_, 8, v___x_4936_);
v___x_4938_ = lean_st_mk_ref(v___x_4937_);
v___x_4952_ = l_Lean_inheritedTraceOptions;
v___x_4953_ = lean_st_ref_get(v___x_4952_);
v___x_4954_ = lean_st_ref_get(v___x_4938_);
v___x_4955_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_4956_ = l_Lean_instInhabitedFileMap_default;
v___x_4957_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_4958_ = lean_unsigned_to_nat(1000u);
v___x_4959_ = lean_box(0);
v___x_4960_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_4961_ = 0;
v___x_4962_ = lean_box(0);
v___x_4963_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_4963_, 0, v___x_4955_);
lean_ctor_set(v___x_4963_, 1, v___x_4956_);
lean_ctor_set(v___x_4963_, 2, v___x_4957_);
lean_ctor_set(v___x_4963_, 3, v___x_4925_);
lean_ctor_set(v___x_4963_, 4, v___x_4958_);
lean_ctor_set(v___x_4963_, 5, v___x_4959_);
lean_ctor_set(v___x_4963_, 6, v___x_4930_);
lean_ctor_set(v___x_4963_, 7, v___x_4898_);
lean_ctor_set(v___x_4963_, 8, v___x_4928_);
lean_ctor_set(v___x_4963_, 9, v___x_4960_);
lean_ctor_set(v___x_4963_, 10, v___x_4930_);
lean_ctor_set(v___x_4963_, 11, v___x_4929_);
lean_ctor_set(v___x_4963_, 12, v___x_4962_);
lean_ctor_set(v___x_4963_, 13, v___x_4953_);
lean_ctor_set_uint8(v___x_4963_, sizeof(void*)*14, v___x_4961_);
lean_ctor_set_uint8(v___x_4963_, sizeof(void*)*14 + 1, v___x_4961_);
v_env_4964_ = lean_ctor_get(v___x_4954_, 0);
lean_inc_ref(v_env_4964_);
lean_dec(v___x_4954_);
v___x_4965_ = lean_uint8_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17);
v___x_4987_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_4964_);
lean_dec_ref(v_env_4964_);
if (v___x_4987_ == 0)
{
if (v___x_4965_ == 0)
{
v___y_4967_ = v___x_4919_;
goto v___jp_4966_;
}
else
{
v___y_4967_ = v___x_4987_;
goto v___jp_4966_;
}
}
else
{
v___y_4967_ = v___x_4965_;
goto v___jp_4966_;
}
v___jp_4939_:
{
lean_object* v___x_4942_; lean_object* v_a_4943_; lean_object* v___x_4944_; size_t v_sz_4945_; size_t v___x_4946_; lean_object* v___x_4947_; lean_object* v___x_4948_; uint8_t v___x_4949_; 
lean_dec_ref(v___y_4940_);
v___x_4942_ = l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg(v___x_4918_, v___y_4941_);
lean_dec(v___y_4941_);
v_a_4943_ = lean_ctor_get(v___x_4942_, 0);
lean_inc(v_a_4943_);
lean_dec_ref(v___x_4942_);
v___x_4944_ = lean_st_ref_get(v___x_4938_);
lean_dec(v___x_4938_);
lean_dec(v___x_4944_);
v_sz_4945_ = lean_array_size(v_a_4943_);
v___x_4946_ = ((size_t)0ULL);
v___x_4947_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__19(v_sz_4945_, v___x_4946_, v_a_4943_);
v___x_4948_ = lean_array_get_size(v___x_4947_);
v___x_4949_ = lean_nat_dec_eq(v___x_4948_, v___x_4925_);
if (v___x_4949_ == 0)
{
lean_object* v___x_4950_; uint8_t v___x_4951_; 
v___x_4950_ = lean_nat_sub(v___x_4948_, v___x_4929_);
v___x_4951_ = lean_nat_dec_le(v___x_4925_, v___x_4950_);
if (v___x_4951_ == 0)
{
lean_inc(v___x_4950_);
v___y_4913_ = v___x_4947_;
v___y_4914_ = v___x_4948_;
v___y_4915_ = v___x_4950_;
v___y_4916_ = v___x_4950_;
goto v___jp_4912_;
}
else
{
v___y_4913_ = v___x_4947_;
v___y_4914_ = v___x_4948_;
v___y_4915_ = v___x_4950_;
v___y_4916_ = v___x_4925_;
goto v___jp_4912_;
}
}
else
{
v___y_4900_ = v___x_4947_;
goto v___jp_4899_;
}
}
v___jp_4966_:
{
if (v___y_4967_ == 0)
{
lean_object* v___x_4968_; lean_object* v_env_4969_; lean_object* v_nextMacroScope_4970_; lean_object* v_ngen_4971_; lean_object* v_auxDeclNGen_4972_; lean_object* v_traceState_4973_; lean_object* v_messages_4974_; lean_object* v_infoState_4975_; lean_object* v_snapshotTasks_4976_; lean_object* v___x_4978_; uint8_t v_isShared_4979_; uint8_t v_isSharedCheck_4985_; 
v___x_4968_ = lean_st_ref_take(v___x_4938_);
v_env_4969_ = lean_ctor_get(v___x_4968_, 0);
v_nextMacroScope_4970_ = lean_ctor_get(v___x_4968_, 1);
v_ngen_4971_ = lean_ctor_get(v___x_4968_, 2);
v_auxDeclNGen_4972_ = lean_ctor_get(v___x_4968_, 3);
v_traceState_4973_ = lean_ctor_get(v___x_4968_, 4);
v_messages_4974_ = lean_ctor_get(v___x_4968_, 6);
v_infoState_4975_ = lean_ctor_get(v___x_4968_, 7);
v_snapshotTasks_4976_ = lean_ctor_get(v___x_4968_, 8);
v_isSharedCheck_4985_ = !lean_is_exclusive(v___x_4968_);
if (v_isSharedCheck_4985_ == 0)
{
lean_object* v_unused_4986_; 
v_unused_4986_ = lean_ctor_get(v___x_4968_, 5);
lean_dec(v_unused_4986_);
v___x_4978_ = v___x_4968_;
v_isShared_4979_ = v_isSharedCheck_4985_;
goto v_resetjp_4977_;
}
else
{
lean_inc(v_snapshotTasks_4976_);
lean_inc(v_infoState_4975_);
lean_inc(v_messages_4974_);
lean_inc(v_traceState_4973_);
lean_inc(v_auxDeclNGen_4972_);
lean_inc(v_ngen_4971_);
lean_inc(v_nextMacroScope_4970_);
lean_inc(v_env_4969_);
lean_dec(v___x_4968_);
v___x_4978_ = lean_box(0);
v_isShared_4979_ = v_isSharedCheck_4985_;
goto v_resetjp_4977_;
}
v_resetjp_4977_:
{
lean_object* v___x_4980_; lean_object* v___x_4982_; 
v___x_4980_ = l_Lean_Kernel_enableDiag(v_env_4969_, v___x_4965_);
if (v_isShared_4979_ == 0)
{
lean_ctor_set(v___x_4978_, 5, v___x_4926_);
lean_ctor_set(v___x_4978_, 0, v___x_4980_);
v___x_4982_ = v___x_4978_;
goto v_reusejp_4981_;
}
else
{
lean_object* v_reuseFailAlloc_4984_; 
v_reuseFailAlloc_4984_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_4984_, 0, v___x_4980_);
lean_ctor_set(v_reuseFailAlloc_4984_, 1, v_nextMacroScope_4970_);
lean_ctor_set(v_reuseFailAlloc_4984_, 2, v_ngen_4971_);
lean_ctor_set(v_reuseFailAlloc_4984_, 3, v_auxDeclNGen_4972_);
lean_ctor_set(v_reuseFailAlloc_4984_, 4, v_traceState_4973_);
lean_ctor_set(v_reuseFailAlloc_4984_, 5, v___x_4926_);
lean_ctor_set(v_reuseFailAlloc_4984_, 6, v_messages_4974_);
lean_ctor_set(v_reuseFailAlloc_4984_, 7, v_infoState_4975_);
lean_ctor_set(v_reuseFailAlloc_4984_, 8, v_snapshotTasks_4976_);
v___x_4982_ = v_reuseFailAlloc_4984_;
goto v_reusejp_4981_;
}
v_reusejp_4981_:
{
lean_object* v___x_4983_; 
v___x_4983_ = lean_st_ref_set(v___x_4938_, v___x_4982_);
lean_inc(v___x_4938_);
v___y_4940_ = v___x_4963_;
v___y_4941_ = v___x_4938_;
goto v___jp_4939_;
}
}
}
else
{
lean_inc(v___x_4938_);
v___y_4940_ = v___x_4963_;
v___y_4941_ = v___x_4938_;
goto v___jp_4939_;
}
}
}
v___jp_4899_:
{
lean_object* v___x_4901_; lean_object* v___x_4902_; lean_object* v___x_4903_; lean_object* v___x_4904_; 
v___x_4901_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___y_4900_);
lean_inc(v_head_4895_);
v___x_4902_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4902_, 0, v_head_4895_);
lean_ctor_set(v___x_4902_, 1, v___x_4901_);
v___x_4903_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_4903_, 0, v___x_4902_);
lean_ctor_set(v___x_4903_, 1, v___x_4898_);
v___x_4904_ = l_List_appendTR___redArg(v_b_4892_, v___x_4903_);
v_as_x27_4891_ = v_tail_4896_;
v_b_4892_ = v___x_4904_;
goto _start;
}
v___jp_4906_:
{
lean_object* v___x_4911_; 
v___x_4911_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00__private_Lean_Elab_DocString_Builtin_0__Lean_Doc_validateCat_spec__3___redArg(v___y_4909_, v___y_4907_, v___y_4908_, v___y_4910_);
lean_dec(v___y_4910_);
lean_dec(v___y_4909_);
v___y_4900_ = v___x_4911_;
goto v___jp_4899_;
}
v___jp_4912_:
{
uint8_t v___x_4917_; 
v___x_4917_ = lean_nat_dec_le(v___y_4916_, v___y_4915_);
if (v___x_4917_ == 0)
{
lean_dec(v___y_4915_);
lean_inc(v___y_4916_);
v___y_4907_ = v___y_4913_;
v___y_4908_ = v___y_4916_;
v___y_4909_ = v___y_4914_;
v___y_4910_ = v___y_4916_;
goto v___jp_4906_;
}
else
{
v___y_4907_ = v___y_4913_;
v___y_4908_ = v___y_4916_;
v___y_4909_ = v___y_4914_;
v___y_4910_ = v___y_4915_;
goto v___jp_4906_;
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___boxed(lean_object* v_a_4988_, lean_object* v_as_x27_4989_, lean_object* v_b_4990_, lean_object* v___y_4991_){
_start:
{
lean_object* v_res_4992_; 
v_res_4992_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg(v_a_4988_, v_as_x27_4989_, v_b_4990_);
lean_dec(v_as_x27_4989_);
return v_res_4992_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20___redArg(lean_object* v_a_4993_, lean_object* v_as_4994_, lean_object* v_as_x27_4995_, lean_object* v_b_4996_){
_start:
{
if (lean_obj_tag(v_as_x27_4995_) == 0)
{
lean_object* v___x_4998_; 
lean_dec_ref(v_a_4993_);
v___x_4998_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_4998_, 0, v_b_4996_);
return v___x_4998_;
}
else
{
lean_object* v_head_4999_; lean_object* v_tail_5000_; uint8_t v___x_5001_; lean_object* v___x_5002_; lean_object* v___y_5004_; lean_object* v___y_5011_; lean_object* v___y_5012_; lean_object* v___y_5013_; lean_object* v___y_5014_; lean_object* v___y_5017_; lean_object* v___y_5018_; lean_object* v___y_5019_; lean_object* v___y_5020_; lean_object* v___x_5022_; uint8_t v___x_5023_; 
v_head_4999_ = lean_ctor_get(v_as_x27_4995_, 0);
v_tail_5000_ = lean_ctor_get(v_as_x27_4995_, 1);
v___x_5001_ = 1;
v___x_5002_ = lean_box(0);
lean_inc(v_head_4999_);
v___x_5022_ = l_String_toName(v_head_4999_);
lean_inc(v___x_5022_);
lean_inc_ref(v_a_4993_);
v___x_5023_ = l_Lean_Environment_contains(v_a_4993_, v___x_5022_, v___x_5001_);
if (v___x_5023_ == 0)
{
lean_object* v___x_5024_; lean_object* v___x_5025_; lean_object* v___x_5026_; lean_object* v___x_5027_; lean_object* v___x_5028_; 
lean_dec(v___x_5022_);
v___x_5024_ = ((lean_object*)(l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__3));
lean_inc(v_head_4999_);
v___x_5025_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5025_, 0, v_head_4999_);
lean_ctor_set(v___x_5025_, 1, v___x_5024_);
v___x_5026_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5026_, 0, v___x_5025_);
lean_ctor_set(v___x_5026_, 1, v___x_5002_);
v___x_5027_ = l_List_appendTR___redArg(v_b_4996_, v___x_5026_);
v___x_5028_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg(v_a_4993_, v_tail_5000_, v___x_5027_);
return v___x_5028_;
}
else
{
lean_object* v___x_5029_; lean_object* v___x_5030_; lean_object* v___x_5031_; lean_object* v___x_5032_; lean_object* v___x_5033_; lean_object* v___x_5034_; lean_object* v___x_5035_; lean_object* v___x_5036_; lean_object* v___x_5037_; lean_object* v___x_5038_; lean_object* v___x_5039_; lean_object* v___x_5040_; lean_object* v___x_5041_; lean_object* v___x_5042_; lean_object* v___x_5043_; lean_object* v___x_5044_; lean_object* v___y_5046_; lean_object* v___y_5047_; lean_object* v___x_5058_; lean_object* v___x_5059_; lean_object* v___x_5060_; lean_object* v___x_5061_; lean_object* v___x_5062_; lean_object* v___x_5063_; lean_object* v___x_5064_; lean_object* v___x_5065_; lean_object* v___x_5066_; uint8_t v___x_5067_; lean_object* v___x_5068_; lean_object* v___x_5069_; lean_object* v_env_5070_; uint8_t v___x_5071_; uint8_t v___y_5073_; uint8_t v___x_5093_; 
v___x_5029_ = lean_unsigned_to_nat(0u);
v___x_5030_ = lean_unsigned_to_nat(32u);
v___x_5031_ = lean_mk_empty_array_with_capacity(v___x_5030_);
lean_dec_ref(v___x_5031_);
v___x_5032_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11___lam__0___closed__3);
v___x_5033_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__1);
v___x_5034_ = lean_io_get_num_heartbeats();
v___x_5035_ = lean_unsigned_to_nat(1u);
v___x_5036_ = lean_box(0);
v___x_5037_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__11));
v___x_5038_ = lean_unsigned_to_nat(2u);
v___x_5039_ = ((lean_object*)(l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__4));
v___x_5040_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__3);
v___x_5041_ = lean_obj_once(&l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5, &l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5_once, _init_l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg___closed__5);
v___x_5042_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__10_spec__13___closed__4));
lean_inc_ref(v_a_4993_);
v___x_5043_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_5043_, 0, v_a_4993_);
lean_ctor_set(v___x_5043_, 1, v___x_5038_);
lean_ctor_set(v___x_5043_, 2, v___x_5037_);
lean_ctor_set(v___x_5043_, 3, v___x_5039_);
lean_ctor_set(v___x_5043_, 4, v___x_5040_);
lean_ctor_set(v___x_5043_, 5, v___x_5032_);
lean_ctor_set(v___x_5043_, 6, v___x_5033_);
lean_ctor_set(v___x_5043_, 7, v___x_5041_);
lean_ctor_set(v___x_5043_, 8, v___x_5042_);
v___x_5044_ = lean_st_mk_ref(v___x_5043_);
v___x_5058_ = l_Lean_inheritedTraceOptions;
v___x_5059_ = lean_st_ref_get(v___x_5058_);
v___x_5060_ = lean_st_ref_get(v___x_5044_);
v___x_5061_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__0));
v___x_5062_ = l_Lean_instInhabitedFileMap_default;
v___x_5063_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__4);
v___x_5064_ = lean_unsigned_to_nat(1000u);
v___x_5065_ = lean_box(0);
v___x_5066_ = lean_obj_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11_spec__15___closed__5);
v___x_5067_ = 0;
v___x_5068_ = lean_box(0);
v___x_5069_ = lean_alloc_ctor(0, 14, 2);
lean_ctor_set(v___x_5069_, 0, v___x_5061_);
lean_ctor_set(v___x_5069_, 1, v___x_5062_);
lean_ctor_set(v___x_5069_, 2, v___x_5063_);
lean_ctor_set(v___x_5069_, 3, v___x_5029_);
lean_ctor_set(v___x_5069_, 4, v___x_5064_);
lean_ctor_set(v___x_5069_, 5, v___x_5065_);
lean_ctor_set(v___x_5069_, 6, v___x_5036_);
lean_ctor_set(v___x_5069_, 7, v___x_5002_);
lean_ctor_set(v___x_5069_, 8, v___x_5034_);
lean_ctor_set(v___x_5069_, 9, v___x_5066_);
lean_ctor_set(v___x_5069_, 10, v___x_5036_);
lean_ctor_set(v___x_5069_, 11, v___x_5035_);
lean_ctor_set(v___x_5069_, 12, v___x_5068_);
lean_ctor_set(v___x_5069_, 13, v___x_5059_);
lean_ctor_set_uint8(v___x_5069_, sizeof(void*)*14, v___x_5067_);
lean_ctor_set_uint8(v___x_5069_, sizeof(void*)*14 + 1, v___x_5067_);
v_env_5070_ = lean_ctor_get(v___x_5060_, 0);
lean_inc_ref(v_env_5070_);
lean_dec(v___x_5060_);
v___x_5071_ = lean_uint8_once(&l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17, &l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17_once, _init_l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__16_spec__21___closed__17);
v___x_5093_ = l_Lean_Kernel_isDiagnosticsEnabled(v_env_5070_);
lean_dec_ref(v_env_5070_);
if (v___x_5093_ == 0)
{
if (v___x_5071_ == 0)
{
v___y_5073_ = v___x_5023_;
goto v___jp_5072_;
}
else
{
v___y_5073_ = v___x_5093_;
goto v___jp_5072_;
}
}
else
{
v___y_5073_ = v___x_5071_;
goto v___jp_5072_;
}
v___jp_5045_:
{
lean_object* v___x_5048_; lean_object* v_a_5049_; lean_object* v___x_5050_; size_t v_sz_5051_; size_t v___x_5052_; lean_object* v___x_5053_; lean_object* v___x_5054_; uint8_t v___x_5055_; 
lean_dec_ref(v___y_5046_);
v___x_5048_ = l_Lean_collectAxioms___at___00NsExport_main_spec__18___redArg(v___x_5022_, v___y_5047_);
lean_dec(v___y_5047_);
v_a_5049_ = lean_ctor_get(v___x_5048_, 0);
lean_inc(v_a_5049_);
lean_dec_ref(v___x_5048_);
v___x_5050_ = lean_st_ref_get(v___x_5044_);
lean_dec(v___x_5044_);
lean_dec(v___x_5050_);
v_sz_5051_ = lean_array_size(v_a_5049_);
v___x_5052_ = ((size_t)0ULL);
v___x_5053_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__19(v_sz_5051_, v___x_5052_, v_a_5049_);
v___x_5054_ = lean_array_get_size(v___x_5053_);
v___x_5055_ = lean_nat_dec_eq(v___x_5054_, v___x_5029_);
if (v___x_5055_ == 0)
{
lean_object* v___x_5056_; uint8_t v___x_5057_; 
v___x_5056_ = lean_nat_sub(v___x_5054_, v___x_5035_);
v___x_5057_ = lean_nat_dec_le(v___x_5029_, v___x_5056_);
if (v___x_5057_ == 0)
{
lean_inc(v___x_5056_);
v___y_5017_ = v___x_5056_;
v___y_5018_ = v___x_5054_;
v___y_5019_ = v___x_5053_;
v___y_5020_ = v___x_5056_;
goto v___jp_5016_;
}
else
{
v___y_5017_ = v___x_5056_;
v___y_5018_ = v___x_5054_;
v___y_5019_ = v___x_5053_;
v___y_5020_ = v___x_5029_;
goto v___jp_5016_;
}
}
else
{
v___y_5004_ = v___x_5053_;
goto v___jp_5003_;
}
}
v___jp_5072_:
{
if (v___y_5073_ == 0)
{
lean_object* v___x_5074_; lean_object* v_env_5075_; lean_object* v_nextMacroScope_5076_; lean_object* v_ngen_5077_; lean_object* v_auxDeclNGen_5078_; lean_object* v_traceState_5079_; lean_object* v_messages_5080_; lean_object* v_infoState_5081_; lean_object* v_snapshotTasks_5082_; lean_object* v___x_5084_; uint8_t v_isShared_5085_; uint8_t v_isSharedCheck_5091_; 
v___x_5074_ = lean_st_ref_take(v___x_5044_);
v_env_5075_ = lean_ctor_get(v___x_5074_, 0);
v_nextMacroScope_5076_ = lean_ctor_get(v___x_5074_, 1);
v_ngen_5077_ = lean_ctor_get(v___x_5074_, 2);
v_auxDeclNGen_5078_ = lean_ctor_get(v___x_5074_, 3);
v_traceState_5079_ = lean_ctor_get(v___x_5074_, 4);
v_messages_5080_ = lean_ctor_get(v___x_5074_, 6);
v_infoState_5081_ = lean_ctor_get(v___x_5074_, 7);
v_snapshotTasks_5082_ = lean_ctor_get(v___x_5074_, 8);
v_isSharedCheck_5091_ = !lean_is_exclusive(v___x_5074_);
if (v_isSharedCheck_5091_ == 0)
{
lean_object* v_unused_5092_; 
v_unused_5092_ = lean_ctor_get(v___x_5074_, 5);
lean_dec(v_unused_5092_);
v___x_5084_ = v___x_5074_;
v_isShared_5085_ = v_isSharedCheck_5091_;
goto v_resetjp_5083_;
}
else
{
lean_inc(v_snapshotTasks_5082_);
lean_inc(v_infoState_5081_);
lean_inc(v_messages_5080_);
lean_inc(v_traceState_5079_);
lean_inc(v_auxDeclNGen_5078_);
lean_inc(v_ngen_5077_);
lean_inc(v_nextMacroScope_5076_);
lean_inc(v_env_5075_);
lean_dec(v___x_5074_);
v___x_5084_ = lean_box(0);
v_isShared_5085_ = v_isSharedCheck_5091_;
goto v_resetjp_5083_;
}
v_resetjp_5083_:
{
lean_object* v___x_5086_; lean_object* v___x_5088_; 
v___x_5086_ = l_Lean_Kernel_enableDiag(v_env_5075_, v___x_5071_);
if (v_isShared_5085_ == 0)
{
lean_ctor_set(v___x_5084_, 5, v___x_5032_);
lean_ctor_set(v___x_5084_, 0, v___x_5086_);
v___x_5088_ = v___x_5084_;
goto v_reusejp_5087_;
}
else
{
lean_object* v_reuseFailAlloc_5090_; 
v_reuseFailAlloc_5090_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_5090_, 0, v___x_5086_);
lean_ctor_set(v_reuseFailAlloc_5090_, 1, v_nextMacroScope_5076_);
lean_ctor_set(v_reuseFailAlloc_5090_, 2, v_ngen_5077_);
lean_ctor_set(v_reuseFailAlloc_5090_, 3, v_auxDeclNGen_5078_);
lean_ctor_set(v_reuseFailAlloc_5090_, 4, v_traceState_5079_);
lean_ctor_set(v_reuseFailAlloc_5090_, 5, v___x_5032_);
lean_ctor_set(v_reuseFailAlloc_5090_, 6, v_messages_5080_);
lean_ctor_set(v_reuseFailAlloc_5090_, 7, v_infoState_5081_);
lean_ctor_set(v_reuseFailAlloc_5090_, 8, v_snapshotTasks_5082_);
v___x_5088_ = v_reuseFailAlloc_5090_;
goto v_reusejp_5087_;
}
v_reusejp_5087_:
{
lean_object* v___x_5089_; 
v___x_5089_ = lean_st_ref_set(v___x_5044_, v___x_5088_);
lean_inc(v___x_5044_);
v___y_5046_ = v___x_5069_;
v___y_5047_ = v___x_5044_;
goto v___jp_5045_;
}
}
}
else
{
lean_inc(v___x_5044_);
v___y_5046_ = v___x_5069_;
v___y_5047_ = v___x_5044_;
goto v___jp_5045_;
}
}
}
v___jp_5003_:
{
lean_object* v___x_5005_; lean_object* v___x_5006_; lean_object* v___x_5007_; lean_object* v___x_5008_; lean_object* v___x_5009_; 
v___x_5005_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___y_5004_);
lean_inc(v_head_4999_);
v___x_5006_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5006_, 0, v_head_4999_);
lean_ctor_set(v___x_5006_, 1, v___x_5005_);
v___x_5007_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5007_, 0, v___x_5006_);
lean_ctor_set(v___x_5007_, 1, v___x_5002_);
v___x_5008_ = l_List_appendTR___redArg(v_b_4996_, v___x_5007_);
v___x_5009_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg(v_a_4993_, v_tail_5000_, v___x_5008_);
return v___x_5009_;
}
v___jp_5010_:
{
lean_object* v___x_5015_; 
v___x_5015_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00__private_Lean_Elab_DocString_Builtin_0__Lean_Doc_validateCat_spec__3___redArg(v___y_5012_, v___y_5013_, v___y_5011_, v___y_5014_);
lean_dec(v___y_5014_);
lean_dec(v___y_5012_);
v___y_5004_ = v___x_5015_;
goto v___jp_5003_;
}
v___jp_5016_:
{
uint8_t v___x_5021_; 
v___x_5021_ = lean_nat_dec_le(v___y_5020_, v___y_5017_);
if (v___x_5021_ == 0)
{
lean_dec(v___y_5017_);
lean_inc(v___y_5020_);
v___y_5011_ = v___y_5020_;
v___y_5012_ = v___y_5018_;
v___y_5013_ = v___y_5019_;
v___y_5014_ = v___y_5020_;
goto v___jp_5010_;
}
else
{
v___y_5011_ = v___y_5020_;
v___y_5012_ = v___y_5018_;
v___y_5013_ = v___y_5019_;
v___y_5014_ = v___y_5017_;
goto v___jp_5010_;
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20___redArg___boxed(lean_object* v_a_5094_, lean_object* v_as_5095_, lean_object* v_as_x27_5096_, lean_object* v_b_5097_, lean_object* v___y_5098_){
_start:
{
lean_object* v_res_5099_; 
v_res_5099_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__20___redArg(v_a_5094_, v_as_5095_, v_as_x27_5096_, v_b_5097_);
lean_dec(v_as_x27_5096_);
lean_dec(v_as_5095_);
return v_res_5099_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00__private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21_spec__29(lean_object* v_as_5100_, size_t v_i_5101_, size_t v_stop_5102_, lean_object* v_b_5103_){
_start:
{
lean_object* v___y_5105_; uint8_t v___x_5109_; 
v___x_5109_ = lean_usize_dec_eq(v_i_5101_, v_stop_5102_);
if (v___x_5109_ == 0)
{
lean_object* v___x_5110_; lean_object* v___x_5111_; lean_object* v___x_5112_; uint8_t v___x_5113_; 
v___x_5110_ = lean_array_uget_borrowed(v_as_5100_, v_i_5101_);
v___x_5111_ = ((lean_object*)(l_NsExport_projectRoots));
v___x_5112_ = l_Lean_Name_getRoot(v___x_5110_);
v___x_5113_ = l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(v___x_5112_, v___x_5111_);
lean_dec(v___x_5112_);
if (v___x_5113_ == 0)
{
v___y_5105_ = v_b_5103_;
goto v___jp_5104_;
}
else
{
lean_object* v___x_5114_; 
lean_inc(v___x_5110_);
v___x_5114_ = lean_array_push(v_b_5103_, v___x_5110_);
v___y_5105_ = v___x_5114_;
goto v___jp_5104_;
}
}
else
{
return v_b_5103_;
}
v___jp_5104_:
{
size_t v___x_5106_; size_t v___x_5107_; 
v___x_5106_ = ((size_t)1ULL);
v___x_5107_ = lean_usize_add(v_i_5101_, v___x_5106_);
v_i_5101_ = v___x_5107_;
v_b_5103_ = v___y_5105_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00__private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21_spec__29___boxed(lean_object* v_as_5115_, lean_object* v_i_5116_, lean_object* v_stop_5117_, lean_object* v_b_5118_){
_start:
{
size_t v_i_boxed_5119_; size_t v_stop_boxed_5120_; lean_object* v_res_5121_; 
v_i_boxed_5119_ = lean_unbox_usize(v_i_5116_);
lean_dec(v_i_5116_);
v_stop_boxed_5120_ = lean_unbox_usize(v_stop_5117_);
lean_dec(v_stop_5117_);
v_res_5121_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00__private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21_spec__29(v_as_5115_, v_i_boxed_5119_, v_stop_boxed_5120_, v_b_5118_);
lean_dec_ref(v_as_5115_);
return v_res_5121_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21(lean_object* v_as_5122_, size_t v_i_5123_, size_t v_stop_5124_, lean_object* v_b_5125_){
_start:
{
lean_object* v___y_5127_; uint8_t v___x_5131_; 
v___x_5131_ = lean_usize_dec_eq(v_i_5123_, v_stop_5124_);
if (v___x_5131_ == 0)
{
lean_object* v___x_5132_; lean_object* v___x_5133_; lean_object* v___x_5134_; uint8_t v___x_5135_; 
v___x_5132_ = lean_array_uget_borrowed(v_as_5122_, v_i_5123_);
v___x_5133_ = ((lean_object*)(l_NsExport_projectRoots));
v___x_5134_ = l_Lean_Name_getRoot(v___x_5132_);
v___x_5135_ = l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(v___x_5134_, v___x_5133_);
lean_dec(v___x_5134_);
if (v___x_5135_ == 0)
{
v___y_5127_ = v_b_5125_;
goto v___jp_5126_;
}
else
{
lean_object* v___x_5136_; 
lean_inc(v___x_5132_);
v___x_5136_ = lean_array_push(v_b_5125_, v___x_5132_);
v___y_5127_ = v___x_5136_;
goto v___jp_5126_;
}
}
else
{
return v_b_5125_;
}
v___jp_5126_:
{
size_t v___x_5128_; size_t v___x_5129_; lean_object* v___x_5130_; 
v___x_5128_ = ((size_t)1ULL);
v___x_5129_ = lean_usize_add(v_i_5123_, v___x_5128_);
v___x_5130_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00__private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21_spec__29(v_as_5122_, v___x_5129_, v_stop_5124_, v___y_5127_);
return v___x_5130_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21___boxed(lean_object* v_as_5137_, lean_object* v_i_5138_, lean_object* v_stop_5139_, lean_object* v_b_5140_){
_start:
{
size_t v_i_boxed_5141_; size_t v_stop_boxed_5142_; lean_object* v_res_5143_; 
v_i_boxed_5141_ = lean_unbox_usize(v_i_5138_);
lean_dec(v_i_5138_);
v_stop_boxed_5142_ = lean_unbox_usize(v_stop_5139_);
lean_dec(v_stop_5139_);
v_res_5143_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21(v_as_5137_, v_i_boxed_5141_, v_stop_boxed_5142_, v_b_5140_);
lean_dec_ref(v_as_5137_);
return v_res_5143_;
}
}
static lean_object* _init_l_NsExport_main___closed__25(void){
_start:
{
lean_object* v___x_5185_; lean_object* v___x_5186_; lean_object* v___x_5187_; 
v___x_5185_ = ((lean_object*)(l_NsExport_main___closed__24));
v___x_5186_ = lean_obj_once(&l_NsExport_resolveDeps___closed__1, &l_NsExport_resolveDeps___closed__1_once, _init_l_NsExport_resolveDeps___closed__1);
v___x_5187_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5187_, 0, v___x_5186_);
lean_ctor_set(v___x_5187_, 1, v___x_5185_);
return v___x_5187_;
}
}
static lean_object* _init_l_NsExport_main___closed__26(void){
_start:
{
lean_object* v___x_5188_; lean_object* v___x_5189_; lean_object* v___x_5190_; 
v___x_5188_ = lean_obj_once(&l_NsExport_main___closed__25, &l_NsExport_main___closed__25_once, _init_l_NsExport_main___closed__25);
v___x_5189_ = lean_obj_once(&l_NsExport_resolveDeps___closed__1, &l_NsExport_resolveDeps___closed__1_once, _init_l_NsExport_resolveDeps___closed__1);
v___x_5190_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5190_, 0, v___x_5189_);
lean_ctor_set(v___x_5190_, 1, v___x_5188_);
return v___x_5190_;
}
}
static lean_object* _init_l_NsExport_main___boxed__const__1(void){
_start:
{
uint32_t v___x_5213_; lean_object* v___x_5214_; 
v___x_5213_ = 0;
v___x_5214_ = lean_box_uint32(v___x_5213_);
return v___x_5214_;
}
}
LEAN_EXPORT lean_object* l_NsExport_main(lean_object* v_args_5215_){
_start:
{
if (lean_obj_tag(v_args_5215_) == 1)
{
lean_object* v_tail_5223_; 
v_tail_5223_ = lean_ctor_get(v_args_5215_, 1);
lean_inc(v_tail_5223_);
if (lean_obj_tag(v_tail_5223_) == 1)
{
lean_object* v_tail_5224_; 
v_tail_5224_ = lean_ctor_get(v_tail_5223_, 1);
lean_inc(v_tail_5224_);
if (lean_obj_tag(v_tail_5224_) == 1)
{
lean_object* v_tail_5225_; 
v_tail_5225_ = lean_ctor_get(v_tail_5224_, 1);
lean_inc(v_tail_5225_);
if (lean_obj_tag(v_tail_5225_) == 1)
{
lean_object* v_tail_5226_; 
v_tail_5226_ = lean_ctor_get(v_tail_5225_, 1);
lean_inc(v_tail_5226_);
if (lean_obj_tag(v_tail_5226_) == 1)
{
lean_object* v_tail_5227_; 
v_tail_5227_ = lean_ctor_get(v_tail_5226_, 1);
lean_inc(v_tail_5227_);
if (lean_obj_tag(v_tail_5227_) == 1)
{
lean_object* v_head_5228_; lean_object* v___x_5230_; uint8_t v_isShared_5231_; uint8_t v_isSharedCheck_5778_; 
v_head_5228_ = lean_ctor_get(v_args_5215_, 0);
v_isSharedCheck_5778_ = !lean_is_exclusive(v_args_5215_);
if (v_isSharedCheck_5778_ == 0)
{
lean_object* v_unused_5779_; 
v_unused_5779_ = lean_ctor_get(v_args_5215_, 1);
lean_dec(v_unused_5779_);
v___x_5230_ = v_args_5215_;
v_isShared_5231_ = v_isSharedCheck_5778_;
goto v_resetjp_5229_;
}
else
{
lean_inc(v_head_5228_);
lean_dec(v_args_5215_);
v___x_5230_ = lean_box(0);
v_isShared_5231_ = v_isSharedCheck_5778_;
goto v_resetjp_5229_;
}
v_resetjp_5229_:
{
lean_object* v_head_5232_; lean_object* v___x_5234_; uint8_t v_isShared_5235_; uint8_t v_isSharedCheck_5776_; 
v_head_5232_ = lean_ctor_get(v_tail_5223_, 0);
v_isSharedCheck_5776_ = !lean_is_exclusive(v_tail_5223_);
if (v_isSharedCheck_5776_ == 0)
{
lean_object* v_unused_5777_; 
v_unused_5777_ = lean_ctor_get(v_tail_5223_, 1);
lean_dec(v_unused_5777_);
v___x_5234_ = v_tail_5223_;
v_isShared_5235_ = v_isSharedCheck_5776_;
goto v_resetjp_5233_;
}
else
{
lean_inc(v_head_5232_);
lean_dec(v_tail_5223_);
v___x_5234_ = lean_box(0);
v_isShared_5235_ = v_isSharedCheck_5776_;
goto v_resetjp_5233_;
}
v_resetjp_5233_:
{
lean_object* v_head_5236_; lean_object* v___x_5238_; uint8_t v_isShared_5239_; uint8_t v_isSharedCheck_5774_; 
v_head_5236_ = lean_ctor_get(v_tail_5224_, 0);
v_isSharedCheck_5774_ = !lean_is_exclusive(v_tail_5224_);
if (v_isSharedCheck_5774_ == 0)
{
lean_object* v_unused_5775_; 
v_unused_5775_ = lean_ctor_get(v_tail_5224_, 1);
lean_dec(v_unused_5775_);
v___x_5238_ = v_tail_5224_;
v_isShared_5239_ = v_isSharedCheck_5774_;
goto v_resetjp_5237_;
}
else
{
lean_inc(v_head_5236_);
lean_dec(v_tail_5224_);
v___x_5238_ = lean_box(0);
v_isShared_5239_ = v_isSharedCheck_5774_;
goto v_resetjp_5237_;
}
v_resetjp_5237_:
{
lean_object* v_head_5240_; lean_object* v___x_5242_; uint8_t v_isShared_5243_; uint8_t v_isSharedCheck_5772_; 
v_head_5240_ = lean_ctor_get(v_tail_5225_, 0);
v_isSharedCheck_5772_ = !lean_is_exclusive(v_tail_5225_);
if (v_isSharedCheck_5772_ == 0)
{
lean_object* v_unused_5773_; 
v_unused_5773_ = lean_ctor_get(v_tail_5225_, 1);
lean_dec(v_unused_5773_);
v___x_5242_ = v_tail_5225_;
v_isShared_5243_ = v_isSharedCheck_5772_;
goto v_resetjp_5241_;
}
else
{
lean_inc(v_head_5240_);
lean_dec(v_tail_5225_);
v___x_5242_ = lean_box(0);
v_isShared_5243_ = v_isSharedCheck_5772_;
goto v_resetjp_5241_;
}
v_resetjp_5241_:
{
lean_object* v_head_5244_; lean_object* v___x_5246_; uint8_t v_isShared_5247_; uint8_t v_isSharedCheck_5770_; 
v_head_5244_ = lean_ctor_get(v_tail_5226_, 0);
v_isSharedCheck_5770_ = !lean_is_exclusive(v_tail_5226_);
if (v_isSharedCheck_5770_ == 0)
{
lean_object* v_unused_5771_; 
v_unused_5771_ = lean_ctor_get(v_tail_5226_, 1);
lean_dec(v_unused_5771_);
v___x_5246_ = v_tail_5226_;
v_isShared_5247_ = v_isSharedCheck_5770_;
goto v_resetjp_5245_;
}
else
{
lean_inc(v_head_5244_);
lean_dec(v_tail_5226_);
v___x_5246_ = lean_box(0);
v_isShared_5247_ = v_isSharedCheck_5770_;
goto v_resetjp_5245_;
}
v_resetjp_5245_:
{
lean_object* v_head_5248_; lean_object* v_tail_5249_; lean_object* v___x_5251_; uint8_t v_isShared_5252_; uint8_t v_isSharedCheck_5769_; 
v_head_5248_ = lean_ctor_get(v_tail_5227_, 0);
v_tail_5249_ = lean_ctor_get(v_tail_5227_, 1);
v_isSharedCheck_5769_ = !lean_is_exclusive(v_tail_5227_);
if (v_isSharedCheck_5769_ == 0)
{
v___x_5251_ = v_tail_5227_;
v_isShared_5252_ = v_isSharedCheck_5769_;
goto v_resetjp_5250_;
}
else
{
lean_inc(v_tail_5249_);
lean_inc(v_head_5248_);
lean_dec(v_tail_5227_);
v___x_5251_ = lean_box(0);
v_isShared_5252_ = v_isSharedCheck_5769_;
goto v_resetjp_5250_;
}
v_resetjp_5250_:
{
lean_object* v___x_5253_; 
v___x_5253_ = l_NsExport_main___lam__0();
if (lean_obj_tag(v___x_5253_) == 0)
{
lean_object* v_a_5254_; lean_object* v___x_5255_; lean_object* v___x_5256_; 
v_a_5254_ = lean_ctor_get(v___x_5253_, 0);
lean_inc(v_a_5254_);
lean_dec_ref_known(v___x_5253_, 1);
v___x_5255_ = ((lean_object*)(l_NsExport_main___closed__2));
v___x_5256_ = l_Lean_findSysroot(v___x_5255_);
if (lean_obj_tag(v___x_5256_) == 0)
{
lean_object* v_a_5257_; lean_object* v___x_5258_; lean_object* v___x_5259_; 
v_a_5257_ = lean_ctor_get(v___x_5256_, 0);
lean_inc(v_a_5257_);
lean_dec_ref_known(v___x_5256_, 1);
v___x_5258_ = lean_box(0);
v___x_5259_ = l_Lean_initSearchPath(v_a_5257_, v___x_5258_);
if (lean_obj_tag(v___x_5259_) == 0)
{
lean_object* v___x_5260_; lean_object* v___x_5261_; 
lean_dec_ref_known(v___x_5259_, 1);
v___x_5260_ = lean_enable_initializer_execution();
v___x_5261_ = l_IO_FS_lines(v_head_5228_);
lean_dec(v_head_5228_);
if (lean_obj_tag(v___x_5261_) == 0)
{
lean_object* v_a_5262_; uint8_t v___x_5263_; lean_object* v___x_5264_; lean_object* v___y_5266_; lean_object* v___y_5267_; lean_object* v___y_5268_; lean_object* v___y_5269_; lean_object* v___y_5270_; lean_object* v___y_5271_; lean_object* v___y_5272_; lean_object* v___y_5273_; lean_object* v___y_5274_; lean_object* v___y_5275_; lean_object* v___y_5276_; lean_object* v___y_5277_; lean_object* v___y_5278_; lean_object* v___y_5279_; lean_object* v___y_5280_; lean_object* v___x_5371_; lean_object* v___x_5372_; lean_object* v___x_5373_; lean_object* v_shard_5374_; lean_object* v___x_5375_; lean_object* v_nshards_5376_; lean_object* v___y_5378_; size_t v___y_5379_; lean_object* v___y_5380_; lean_object* v___y_5381_; lean_object* v___y_5382_; lean_object* v___y_5383_; lean_object* v___y_5384_; lean_object* v___y_5385_; lean_object* v___y_5386_; lean_object* v___y_5387_; lean_object* v___y_5388_; lean_object* v___y_5593_; size_t v___y_5594_; lean_object* v___y_5595_; lean_object* v___y_5596_; lean_object* v___y_5597_; lean_object* v___y_5598_; lean_object* v___y_5599_; lean_object* v___y_5600_; lean_object* v___y_5601_; lean_object* v___y_5602_; lean_object* v___y_5603_; lean_object* v___y_5604_; lean_object* v___y_5605_; lean_object* v___y_5606_; lean_object* v___y_5609_; size_t v___y_5610_; lean_object* v___y_5611_; lean_object* v___y_5612_; lean_object* v___y_5613_; lean_object* v___y_5614_; lean_object* v___y_5615_; lean_object* v___y_5616_; lean_object* v___y_5617_; lean_object* v___y_5618_; lean_object* v___y_5619_; lean_object* v___y_5620_; lean_object* v___y_5621_; lean_object* v___y_5622_; lean_object* v___y_5625_; size_t v___y_5626_; lean_object* v___y_5627_; lean_object* v___y_5628_; lean_object* v___y_5629_; lean_object* v___y_5630_; lean_object* v___y_5631_; lean_object* v___y_5632_; lean_object* v___y_5633_; lean_object* v___y_5634_; lean_object* v___y_5635_; lean_object* v___y_5652_; lean_object* v___x_5727_; lean_object* v___x_5728_; uint8_t v___x_5729_; 
v_a_5262_ = lean_ctor_get(v___x_5261_, 0);
lean_inc(v_a_5262_);
lean_dec_ref_known(v___x_5261_, 1);
v___x_5263_ = 0;
v___x_5264_ = lean_unsigned_to_nat(0u);
v___x_5371_ = lean_string_utf8_byte_size(v_head_5244_);
v___x_5372_ = lean_string_utf8_byte_size(v_head_5248_);
v___x_5373_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_5373_, 0, v_head_5244_);
lean_ctor_set(v___x_5373_, 1, v___x_5264_);
lean_ctor_set(v___x_5373_, 2, v___x_5371_);
v_shard_5374_ = l_String_Slice_toNat_x21(v___x_5373_);
lean_dec_ref_known(v___x_5373_, 3);
v___x_5375_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_5375_, 0, v_head_5248_);
lean_ctor_set(v___x_5375_, 1, v___x_5264_);
lean_ctor_set(v___x_5375_, 2, v___x_5372_);
v_nshards_5376_ = l_String_Slice_toNat_x21(v___x_5375_);
lean_dec_ref_known(v___x_5375_, 3);
v___x_5727_ = lean_array_get_size(v_a_5262_);
v___x_5728_ = ((lean_object*)(l_NsExport_main___closed__17));
v___x_5729_ = lean_nat_dec_lt(v___x_5264_, v___x_5727_);
if (v___x_5729_ == 0)
{
lean_dec(v_a_5262_);
v___y_5652_ = v___x_5728_;
goto v___jp_5651_;
}
else
{
uint8_t v___x_5730_; 
v___x_5730_ = lean_nat_dec_le(v___x_5727_, v___x_5727_);
if (v___x_5730_ == 0)
{
if (v___x_5729_ == 0)
{
lean_dec(v_a_5262_);
v___y_5652_ = v___x_5728_;
goto v___jp_5651_;
}
else
{
size_t v___x_5731_; size_t v___x_5732_; lean_object* v___x_5733_; 
v___x_5731_ = ((size_t)0ULL);
v___x_5732_ = lean_usize_of_nat(v___x_5727_);
v___x_5733_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__23(v_a_5262_, v___x_5731_, v___x_5732_, v___x_5728_);
lean_dec(v_a_5262_);
v___y_5652_ = v___x_5733_;
goto v___jp_5651_;
}
}
else
{
size_t v___x_5734_; size_t v___x_5735_; lean_object* v___x_5736_; 
v___x_5734_ = ((size_t)0ULL);
v___x_5735_ = lean_usize_of_nat(v___x_5727_);
v___x_5736_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__23(v_a_5262_, v___x_5734_, v___x_5735_, v___x_5728_);
lean_dec(v_a_5262_);
v___y_5652_ = v___x_5736_;
goto v___jp_5651_;
}
}
v___jp_5265_:
{
lean_object* v___x_5281_; lean_object* v___x_5282_; lean_object* v___x_5283_; lean_object* v___x_5284_; lean_object* v___x_5285_; lean_object* v___x_5286_; lean_object* v___x_5287_; lean_object* v___x_5288_; lean_object* v___x_5289_; lean_object* v___x_5290_; lean_object* v___x_5291_; lean_object* v___x_5292_; lean_object* v___x_5293_; lean_object* v___x_5294_; lean_object* v___x_5295_; lean_object* v___x_5296_; lean_object* v___x_5297_; lean_object* v___x_5298_; lean_object* v___x_5299_; lean_object* v___x_5300_; lean_object* v___x_5301_; lean_object* v___x_5302_; lean_object* v___x_5303_; lean_object* v___x_5304_; lean_object* v___x_5305_; lean_object* v___x_5306_; lean_object* v___x_5307_; lean_object* v___x_5308_; lean_object* v___x_5309_; lean_object* v___x_5310_; lean_object* v___x_5311_; lean_object* v___x_5312_; lean_object* v___x_5313_; lean_object* v___x_5314_; lean_object* v___x_5315_; lean_object* v___x_5316_; lean_object* v___x_5317_; lean_object* v___x_5318_; lean_object* v___x_5319_; lean_object* v___x_5320_; lean_object* v___x_5321_; lean_object* v___x_5322_; lean_object* v___x_5323_; lean_object* v___x_5324_; lean_object* v___x_5325_; lean_object* v___x_5326_; lean_object* v___x_5327_; lean_object* v___x_5328_; lean_object* v___x_5329_; lean_object* v___x_5330_; lean_object* v___x_5331_; lean_object* v___x_5332_; lean_object* v___x_5333_; lean_object* v___x_5334_; lean_object* v___x_5336_; 
v___x_5281_ = ((lean_object*)(l_NsExport_main___closed__3));
v___x_5282_ = l_Lean_JsonNumber_fromNat(v___y_5276_);
v___x_5283_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5283_, 0, v___x_5282_);
v___x_5284_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5284_, 0, v___x_5281_);
lean_ctor_set(v___x_5284_, 1, v___x_5283_);
v___x_5285_ = ((lean_object*)(l_NsExport_main___closed__4));
v___x_5286_ = l_Lean_JsonNumber_fromNat(v___y_5279_);
v___x_5287_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5287_, 0, v___x_5286_);
v___x_5288_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5288_, 0, v___x_5285_);
lean_ctor_set(v___x_5288_, 1, v___x_5287_);
v___x_5289_ = ((lean_object*)(l_NsExport_main___closed__5));
v___x_5290_ = lean_array_get_size(v___y_5280_);
lean_dec_ref(v___y_5280_);
v___x_5291_ = l_Lean_JsonNumber_fromNat(v___x_5290_);
v___x_5292_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5292_, 0, v___x_5291_);
v___x_5293_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5293_, 0, v___x_5289_);
lean_ctor_set(v___x_5293_, 1, v___x_5292_);
v___x_5294_ = ((lean_object*)(l_NsExport_main___closed__6));
v___x_5295_ = l_Lean_JsonNumber_fromNat(v___y_5266_);
v___x_5296_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5296_, 0, v___x_5295_);
v___x_5297_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5297_, 0, v___x_5294_);
lean_ctor_set(v___x_5297_, 1, v___x_5296_);
v___x_5298_ = ((lean_object*)(l_NsExport_main___closed__7));
v___x_5299_ = l_Lean_JsonNumber_fromNat(v___y_5270_);
v___x_5300_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5300_, 0, v___x_5299_);
v___x_5301_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5301_, 0, v___x_5298_);
lean_ctor_set(v___x_5301_, 1, v___x_5300_);
v___x_5302_ = ((lean_object*)(l_NsExport_main___closed__8));
v___x_5303_ = l_Lean_JsonNumber_fromNat(v___y_5274_);
v___x_5304_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5304_, 0, v___x_5303_);
v___x_5305_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5305_, 0, v___x_5302_);
lean_ctor_set(v___x_5305_, 1, v___x_5304_);
v___x_5306_ = ((lean_object*)(l_NsExport_main___closed__9));
v___x_5307_ = l_Lean_JsonNumber_fromNat(v___y_5275_);
v___x_5308_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5308_, 0, v___x_5307_);
v___x_5309_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5309_, 0, v___x_5306_);
lean_ctor_set(v___x_5309_, 1, v___x_5308_);
v___x_5310_ = ((lean_object*)(l_NsExport_main___closed__10));
v___x_5311_ = l_Lean_JsonNumber_fromNat(v___y_5268_);
v___x_5312_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5312_, 0, v___x_5311_);
v___x_5313_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5313_, 0, v___x_5310_);
lean_ctor_set(v___x_5313_, 1, v___x_5312_);
v___x_5314_ = ((lean_object*)(l_NsExport_main___closed__11));
v___x_5315_ = l_Lean_JsonNumber_fromNat(v___y_5271_);
v___x_5316_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5316_, 0, v___x_5315_);
v___x_5317_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5317_, 0, v___x_5314_);
lean_ctor_set(v___x_5317_, 1, v___x_5316_);
v___x_5318_ = ((lean_object*)(l_NsExport_main___closed__12));
v___x_5319_ = l_Lean_JsonNumber_fromNat(v___y_5273_);
v___x_5320_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5320_, 0, v___x_5319_);
v___x_5321_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5321_, 0, v___x_5318_);
lean_ctor_set(v___x_5321_, 1, v___x_5320_);
v___x_5322_ = ((lean_object*)(l_NsExport_main___closed__13));
v___x_5323_ = l_Lean_JsonNumber_fromNat(v___y_5277_);
v___x_5324_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5324_, 0, v___x_5323_);
v___x_5325_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5325_, 0, v___x_5322_);
lean_ctor_set(v___x_5325_, 1, v___x_5324_);
v___x_5326_ = ((lean_object*)(l_NsExport_main___closed__14));
v___x_5327_ = lean_unsigned_to_nat(200u);
v___x_5328_ = l_Array_extract___redArg(v___y_5267_, v___x_5264_, v___x_5327_);
lean_dec(v___y_5267_);
v___x_5329_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_5328_);
v___x_5330_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5330_, 0, v___x_5326_);
lean_ctor_set(v___x_5330_, 1, v___x_5329_);
v___x_5331_ = ((lean_object*)(l_NsExport_main___closed__15));
v___x_5332_ = l_Lean_JsonNumber_fromNat(v___y_5269_);
v___x_5333_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_5333_, 0, v___x_5332_);
v___x_5334_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_5334_, 0, v___x_5331_);
lean_ctor_set(v___x_5334_, 1, v___x_5333_);
if (v_isShared_5252_ == 0)
{
lean_ctor_set(v___x_5251_, 1, v___y_5272_);
lean_ctor_set(v___x_5251_, 0, v___x_5334_);
v___x_5336_ = v___x_5251_;
goto v_reusejp_5335_;
}
else
{
lean_object* v_reuseFailAlloc_5370_; 
v_reuseFailAlloc_5370_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_5370_, 0, v___x_5334_);
lean_ctor_set(v_reuseFailAlloc_5370_, 1, v___y_5272_);
v___x_5336_ = v_reuseFailAlloc_5370_;
goto v_reusejp_5335_;
}
v_reusejp_5335_:
{
lean_object* v___x_5338_; 
if (v_isShared_5247_ == 0)
{
lean_ctor_set(v___x_5246_, 1, v___x_5336_);
lean_ctor_set(v___x_5246_, 0, v___x_5330_);
v___x_5338_ = v___x_5246_;
goto v_reusejp_5337_;
}
else
{
lean_object* v_reuseFailAlloc_5369_; 
v_reuseFailAlloc_5369_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_5369_, 0, v___x_5330_);
lean_ctor_set(v_reuseFailAlloc_5369_, 1, v___x_5336_);
v___x_5338_ = v_reuseFailAlloc_5369_;
goto v_reusejp_5337_;
}
v_reusejp_5337_:
{
lean_object* v___x_5340_; 
if (v_isShared_5243_ == 0)
{
lean_ctor_set(v___x_5242_, 1, v___x_5338_);
lean_ctor_set(v___x_5242_, 0, v___x_5325_);
v___x_5340_ = v___x_5242_;
goto v_reusejp_5339_;
}
else
{
lean_object* v_reuseFailAlloc_5368_; 
v_reuseFailAlloc_5368_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_5368_, 0, v___x_5325_);
lean_ctor_set(v_reuseFailAlloc_5368_, 1, v___x_5338_);
v___x_5340_ = v_reuseFailAlloc_5368_;
goto v_reusejp_5339_;
}
v_reusejp_5339_:
{
lean_object* v___x_5342_; 
if (v_isShared_5239_ == 0)
{
lean_ctor_set(v___x_5238_, 1, v___x_5340_);
lean_ctor_set(v___x_5238_, 0, v___x_5321_);
v___x_5342_ = v___x_5238_;
goto v_reusejp_5341_;
}
else
{
lean_object* v_reuseFailAlloc_5367_; 
v_reuseFailAlloc_5367_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_5367_, 0, v___x_5321_);
lean_ctor_set(v_reuseFailAlloc_5367_, 1, v___x_5340_);
v___x_5342_ = v_reuseFailAlloc_5367_;
goto v_reusejp_5341_;
}
v_reusejp_5341_:
{
lean_object* v___x_5344_; 
if (v_isShared_5235_ == 0)
{
lean_ctor_set(v___x_5234_, 1, v___x_5342_);
lean_ctor_set(v___x_5234_, 0, v___x_5317_);
v___x_5344_ = v___x_5234_;
goto v_reusejp_5343_;
}
else
{
lean_object* v_reuseFailAlloc_5366_; 
v_reuseFailAlloc_5366_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_5366_, 0, v___x_5317_);
lean_ctor_set(v_reuseFailAlloc_5366_, 1, v___x_5342_);
v___x_5344_ = v_reuseFailAlloc_5366_;
goto v_reusejp_5343_;
}
v_reusejp_5343_:
{
lean_object* v___x_5346_; 
if (v_isShared_5231_ == 0)
{
lean_ctor_set(v___x_5230_, 1, v___x_5344_);
lean_ctor_set(v___x_5230_, 0, v___x_5313_);
v___x_5346_ = v___x_5230_;
goto v_reusejp_5345_;
}
else
{
lean_object* v_reuseFailAlloc_5365_; 
v_reuseFailAlloc_5365_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_5365_, 0, v___x_5313_);
lean_ctor_set(v_reuseFailAlloc_5365_, 1, v___x_5344_);
v___x_5346_ = v_reuseFailAlloc_5365_;
goto v_reusejp_5345_;
}
v_reusejp_5345_:
{
lean_object* v___x_5347_; lean_object* v___x_5348_; lean_object* v___x_5349_; lean_object* v___x_5350_; lean_object* v___x_5351_; lean_object* v___x_5352_; lean_object* v___x_5353_; lean_object* v___x_5354_; lean_object* v___x_5355_; lean_object* v___x_5356_; 
v___x_5347_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5347_, 0, v___x_5309_);
lean_ctor_set(v___x_5347_, 1, v___x_5346_);
v___x_5348_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5348_, 0, v___x_5305_);
lean_ctor_set(v___x_5348_, 1, v___x_5347_);
v___x_5349_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5349_, 0, v___x_5301_);
lean_ctor_set(v___x_5349_, 1, v___x_5348_);
v___x_5350_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5350_, 0, v___x_5297_);
lean_ctor_set(v___x_5350_, 1, v___x_5349_);
v___x_5351_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5351_, 0, v___x_5293_);
lean_ctor_set(v___x_5351_, 1, v___x_5350_);
v___x_5352_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5352_, 0, v___x_5288_);
lean_ctor_set(v___x_5352_, 1, v___x_5351_);
v___x_5353_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_5353_, 0, v___x_5284_);
lean_ctor_set(v___x_5353_, 1, v___x_5352_);
v___x_5354_ = l_Lean_Json_mkObj(v___x_5353_);
lean_dec_ref_known(v___x_5353_, 2);
v___x_5355_ = l_Lean_Json_pretty(v___x_5354_, v___y_5278_);
v___x_5356_ = l_IO_FS_writeFile(v_head_5240_, v___x_5355_);
lean_dec_ref(v___x_5355_);
lean_dec(v_head_5240_);
if (lean_obj_tag(v___x_5356_) == 0)
{
lean_dec_ref_known(v___x_5356_, 1);
goto v___jp_5217_;
}
else
{
lean_object* v_a_5357_; lean_object* v___x_5359_; uint8_t v_isShared_5360_; uint8_t v_isSharedCheck_5364_; 
v_a_5357_ = lean_ctor_get(v___x_5356_, 0);
v_isSharedCheck_5364_ = !lean_is_exclusive(v___x_5356_);
if (v_isSharedCheck_5364_ == 0)
{
v___x_5359_ = v___x_5356_;
v_isShared_5360_ = v_isSharedCheck_5364_;
goto v_resetjp_5358_;
}
else
{
lean_inc(v_a_5357_);
lean_dec(v___x_5356_);
v___x_5359_ = lean_box(0);
v_isShared_5360_ = v_isSharedCheck_5364_;
goto v_resetjp_5358_;
}
v_resetjp_5358_:
{
lean_object* v___x_5362_; 
if (v_isShared_5360_ == 0)
{
v___x_5362_ = v___x_5359_;
goto v_reusejp_5361_;
}
else
{
lean_object* v_reuseFailAlloc_5363_; 
v_reuseFailAlloc_5363_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5363_, 0, v_a_5357_);
v___x_5362_ = v_reuseFailAlloc_5363_;
goto v_reusejp_5361_;
}
v_reusejp_5361_:
{
return v___x_5362_;
}
}
}
}
}
}
}
}
}
}
v___jp_5377_:
{
lean_object* v___x_5389_; lean_object* v___x_5390_; lean_object* v___x_5391_; lean_object* v___x_5392_; lean_object* v___x_5393_; lean_object* v___x_5394_; 
v___x_5389_ = ((lean_object*)(l_NsExport_main___closed__16));
lean_inc_ref(v___y_5384_);
v___x_5390_ = lean_string_append(v___y_5384_, v___x_5389_);
v___x_5391_ = lean_array_get_size(v___y_5388_);
v___x_5392_ = l_Nat_reprFast(v___x_5391_);
v___x_5393_ = lean_string_append(v___x_5390_, v___x_5392_);
lean_dec_ref(v___x_5392_);
v___x_5394_ = l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(v___x_5393_);
if (lean_obj_tag(v___x_5394_) == 0)
{
lean_object* v___x_5395_; size_t v_sz_5396_; lean_object* v___x_5397_; 
lean_dec_ref_known(v___x_5394_, 1);
v___x_5395_ = lean_obj_once(&l_NsExport_resolveDeps___closed__1, &l_NsExport_resolveDeps___closed__1_once, _init_l_NsExport_resolveDeps___closed__1);
v_sz_5396_ = lean_array_size(v___y_5388_);
lean_inc_ref(v___y_5385_);
v___x_5397_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__11(v___y_5385_, v___y_5381_, v___y_5388_, v_sz_5396_, v___y_5379_, v___x_5395_);
if (lean_obj_tag(v___x_5397_) == 0)
{
lean_object* v_a_5398_; lean_object* v___x_5399_; lean_object* v___x_5400_; lean_object* v___x_5401_; 
v_a_5398_ = lean_ctor_get(v___x_5397_, 0);
lean_inc(v_a_5398_);
lean_dec_ref_known(v___x_5397_, 1);
v___x_5399_ = lean_unsigned_to_nat(3u);
v___x_5400_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_5400_, 0, v___x_5264_);
lean_ctor_set(v___x_5400_, 1, v___x_5399_);
lean_ctor_set(v___x_5400_, 2, v___y_5382_);
lean_inc_ref(v___y_5385_);
v___x_5401_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___redArg(v___y_5388_, v___y_5385_, v___y_5381_, v___x_5400_, v_a_5398_, v___x_5264_);
lean_dec_ref_known(v___x_5400_, 3);
lean_dec_ref(v___y_5381_);
if (lean_obj_tag(v___x_5401_) == 0)
{
lean_object* v_a_5402_; lean_object* v___x_5403_; lean_object* v___x_5404_; lean_object* v___x_5405_; lean_object* v___x_5406_; 
v_a_5402_ = lean_ctor_get(v___x_5401_, 0);
lean_inc_n(v_a_5402_, 2);
lean_dec_ref_known(v___x_5401_, 1);
lean_inc_ref(v___y_5385_);
v___x_5403_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_5403_, 0, v___y_5385_);
lean_ctor_set(v___x_5403_, 1, v___y_5386_);
lean_ctor_set(v___x_5403_, 2, v_a_5402_);
v___x_5404_ = ((lean_object*)(l_NsExport_main___closed__17));
v___x_5405_ = lean_obj_once(&l_NsExport_main___closed__26, &l_NsExport_main___closed__26_once, _init_l_NsExport_main___closed__26);
v___x_5406_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__13(v_a_5402_, v___x_5403_, v___y_5388_, v_sz_5396_, v___y_5379_, v___x_5405_);
if (lean_obj_tag(v___x_5406_) == 0)
{
lean_object* v_a_5407_; lean_object* v_snd_5408_; lean_object* v_snd_5409_; lean_object* v_snd_5410_; lean_object* v_snd_5411_; lean_object* v_snd_5412_; lean_object* v_snd_5413_; lean_object* v_snd_5414_; lean_object* v_snd_5415_; lean_object* v_fst_5416_; lean_object* v_fst_5417_; lean_object* v_fst_5418_; lean_object* v_fst_5419_; lean_object* v_fst_5420_; lean_object* v_fst_5421_; lean_object* v_fst_5422_; lean_object* v_fst_5423_; lean_object* v_fst_5424_; lean_object* v_snd_5425_; lean_object* v___x_5426_; lean_object* v___x_5427_; lean_object* v___x_5428_; lean_object* v___x_5429_; lean_object* v___x_5430_; lean_object* v___x_5431_; lean_object* v___x_5432_; lean_object* v___x_5433_; lean_object* v___x_5434_; lean_object* v___x_5435_; lean_object* v___x_5436_; lean_object* v___x_5437_; lean_object* v___x_5438_; lean_object* v___x_5439_; lean_object* v___x_5440_; lean_object* v___x_5441_; lean_object* v___x_5442_; lean_object* v___x_5443_; lean_object* v___x_5444_; lean_object* v___x_5445_; lean_object* v___x_5446_; lean_object* v___x_5447_; lean_object* v___x_5448_; lean_object* v___x_5449_; lean_object* v___x_5450_; lean_object* v___x_5451_; lean_object* v___x_5452_; lean_object* v___x_5453_; lean_object* v___x_5454_; 
v_a_5407_ = lean_ctor_get(v___x_5406_, 0);
lean_inc(v_a_5407_);
lean_dec_ref_known(v___x_5406_, 1);
v_snd_5408_ = lean_ctor_get(v_a_5407_, 1);
lean_inc(v_snd_5408_);
v_snd_5409_ = lean_ctor_get(v_snd_5408_, 1);
lean_inc(v_snd_5409_);
v_snd_5410_ = lean_ctor_get(v_snd_5409_, 1);
lean_inc(v_snd_5410_);
v_snd_5411_ = lean_ctor_get(v_snd_5410_, 1);
lean_inc(v_snd_5411_);
v_snd_5412_ = lean_ctor_get(v_snd_5411_, 1);
lean_inc(v_snd_5412_);
v_snd_5413_ = lean_ctor_get(v_snd_5412_, 1);
lean_inc(v_snd_5413_);
v_snd_5414_ = lean_ctor_get(v_snd_5413_, 1);
lean_inc(v_snd_5414_);
v_snd_5415_ = lean_ctor_get(v_snd_5414_, 1);
lean_inc(v_snd_5415_);
v_fst_5416_ = lean_ctor_get(v_a_5407_, 0);
lean_inc(v_fst_5416_);
lean_dec(v_a_5407_);
v_fst_5417_ = lean_ctor_get(v_snd_5408_, 0);
lean_inc(v_fst_5417_);
lean_dec(v_snd_5408_);
v_fst_5418_ = lean_ctor_get(v_snd_5409_, 0);
lean_inc_n(v_fst_5418_, 2);
lean_dec(v_snd_5409_);
v_fst_5419_ = lean_ctor_get(v_snd_5410_, 0);
lean_inc_n(v_fst_5419_, 2);
lean_dec(v_snd_5410_);
v_fst_5420_ = lean_ctor_get(v_snd_5411_, 0);
lean_inc_n(v_fst_5420_, 2);
lean_dec(v_snd_5411_);
v_fst_5421_ = lean_ctor_get(v_snd_5412_, 0);
lean_inc_n(v_fst_5421_, 2);
lean_dec(v_snd_5412_);
v_fst_5422_ = lean_ctor_get(v_snd_5413_, 0);
lean_inc_n(v_fst_5422_, 2);
lean_dec(v_snd_5413_);
v_fst_5423_ = lean_ctor_get(v_snd_5414_, 0);
lean_inc_n(v_fst_5423_, 2);
lean_dec(v_snd_5414_);
v_fst_5424_ = lean_ctor_get(v_snd_5415_, 0);
lean_inc_n(v_fst_5424_, 2);
v_snd_5425_ = lean_ctor_get(v_snd_5415_, 1);
lean_inc(v_snd_5425_);
lean_dec(v_snd_5415_);
v___x_5426_ = ((lean_object*)(l_NsExport_main___closed__27));
lean_inc_ref(v___y_5384_);
v___x_5427_ = lean_string_append(v___y_5384_, v___x_5426_);
v___x_5428_ = l_Nat_reprFast(v_fst_5418_);
v___x_5429_ = lean_string_append(v___x_5427_, v___x_5428_);
lean_dec_ref(v___x_5428_);
v___x_5430_ = ((lean_object*)(l_NsExport_main___closed__28));
v___x_5431_ = lean_string_append(v___x_5429_, v___x_5430_);
v___x_5432_ = l_Nat_reprFast(v_fst_5419_);
v___x_5433_ = lean_string_append(v___x_5431_, v___x_5432_);
lean_dec_ref(v___x_5432_);
v___x_5434_ = ((lean_object*)(l_NsExport_main___closed__29));
v___x_5435_ = lean_string_append(v___x_5433_, v___x_5434_);
v___x_5436_ = l_Nat_reprFast(v_fst_5420_);
v___x_5437_ = lean_string_append(v___x_5435_, v___x_5436_);
lean_dec_ref(v___x_5436_);
v___x_5438_ = ((lean_object*)(l_NsExport_main___closed__30));
v___x_5439_ = lean_string_append(v___x_5437_, v___x_5438_);
v___x_5440_ = l_Nat_reprFast(v_fst_5421_);
v___x_5441_ = lean_string_append(v___x_5439_, v___x_5440_);
lean_dec_ref(v___x_5440_);
v___x_5442_ = ((lean_object*)(l_NsExport_main___closed__31));
v___x_5443_ = lean_string_append(v___x_5441_, v___x_5442_);
v___x_5444_ = l_Nat_reprFast(v_fst_5422_);
v___x_5445_ = lean_string_append(v___x_5443_, v___x_5444_);
lean_dec_ref(v___x_5444_);
v___x_5446_ = ((lean_object*)(l_NsExport_main___closed__32));
v___x_5447_ = lean_string_append(v___x_5445_, v___x_5446_);
v___x_5448_ = l_Nat_reprFast(v_fst_5424_);
v___x_5449_ = lean_string_append(v___x_5447_, v___x_5448_);
lean_dec_ref(v___x_5448_);
v___x_5450_ = ((lean_object*)(l_NsExport_main___closed__33));
v___x_5451_ = lean_string_append(v___x_5449_, v___x_5450_);
v___x_5452_ = l_Nat_reprFast(v_fst_5423_);
v___x_5453_ = lean_string_append(v___x_5451_, v___x_5452_);
lean_dec_ref(v___x_5452_);
v___x_5454_ = l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(v___x_5453_);
if (lean_obj_tag(v___x_5454_) == 0)
{
uint8_t v___x_5455_; lean_object* v___x_5456_; 
lean_dec_ref_known(v___x_5454_, 1);
v___x_5455_ = 1;
v___x_5456_ = lean_io_prim_handle_mk(v_head_5232_, v___x_5455_);
lean_dec(v_head_5232_);
if (lean_obj_tag(v___x_5456_) == 0)
{
lean_object* v_a_5457_; lean_object* v___x_5458_; lean_object* v___x_5459_; 
v_a_5457_ = lean_ctor_get(v___x_5456_, 0);
lean_inc(v_a_5457_);
lean_dec_ref_known(v___x_5456_, 1);
v___x_5458_ = ((lean_object*)(l_NsExport_main___closed__35));
lean_inc_ref(v___y_5384_);
lean_inc_ref(v___y_5385_);
v___x_5459_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17(v_a_5402_, v_nshards_5376_, v_shard_5374_, v___y_5385_, v_fst_5417_, v_fst_5416_, v___x_5403_, v_a_5457_, v___y_5384_, v_a_5254_, v___y_5388_, v_sz_5396_, v___y_5379_, v___x_5458_);
lean_dec_ref(v___y_5388_);
lean_dec(v_fst_5416_);
lean_dec(v_fst_5417_);
lean_dec(v_nshards_5376_);
lean_dec(v_a_5402_);
if (lean_obj_tag(v___x_5459_) == 0)
{
lean_object* v_a_5460_; lean_object* v___x_5461_; 
v_a_5460_ = lean_ctor_get(v___x_5459_, 0);
lean_inc(v_a_5460_);
lean_dec_ref_known(v___x_5459_, 1);
v___x_5461_ = lean_io_prim_handle_flush(v_a_5457_);
lean_dec(v_a_5457_);
if (lean_obj_tag(v___x_5461_) == 0)
{
lean_object* v___x_5462_; 
lean_dec_ref_known(v___x_5461_, 1);
v___x_5462_ = l_NsExport_main___lam__0();
if (lean_obj_tag(v___x_5462_) == 0)
{
lean_object* v_snd_5463_; lean_object* v_a_5464_; lean_object* v_fst_5465_; lean_object* v_snd_5466_; lean_object* v___x_5467_; lean_object* v___x_5468_; lean_object* v___x_5469_; lean_object* v___x_5470_; lean_object* v___x_5471_; lean_object* v___x_5472_; lean_object* v___x_5473_; lean_object* v___x_5474_; lean_object* v___x_5475_; lean_object* v___x_5476_; lean_object* v___x_5477_; lean_object* v___x_5478_; lean_object* v___x_5479_; lean_object* v___x_5480_; lean_object* v___x_5481_; lean_object* v___x_5482_; 
v_snd_5463_ = lean_ctor_get(v_a_5460_, 1);
lean_inc(v_snd_5463_);
lean_dec(v_a_5460_);
v_a_5464_ = lean_ctor_get(v___x_5462_, 0);
lean_inc(v_a_5464_);
lean_dec_ref_known(v___x_5462_, 1);
v_fst_5465_ = lean_ctor_get(v_snd_5463_, 0);
lean_inc(v_fst_5465_);
v_snd_5466_ = lean_ctor_get(v_snd_5463_, 1);
lean_inc(v_snd_5466_);
lean_dec(v_snd_5463_);
v___x_5467_ = ((lean_object*)(l_NsExport_main___closed__36));
v___x_5468_ = lean_string_append(v___y_5384_, v___x_5467_);
v___x_5469_ = l_Nat_reprFast(v_snd_5466_);
v___x_5470_ = lean_string_append(v___x_5468_, v___x_5469_);
lean_dec_ref(v___x_5469_);
v___x_5471_ = ((lean_object*)(l_NsExport_main___closed__37));
v___x_5472_ = lean_string_append(v___x_5470_, v___x_5471_);
v___x_5473_ = l_Nat_reprFast(v_fst_5465_);
v___x_5474_ = lean_string_append(v___x_5472_, v___x_5473_);
lean_dec_ref(v___x_5473_);
v___x_5475_ = ((lean_object*)(l_NsExport_main___closed__38));
v___x_5476_ = lean_string_append(v___x_5474_, v___x_5475_);
v___x_5477_ = lean_nat_sub(v_a_5464_, v_a_5254_);
lean_dec(v_a_5254_);
lean_dec(v_a_5464_);
v___x_5478_ = l_Nat_reprFast(v___x_5477_);
v___x_5479_ = lean_string_append(v___x_5476_, v___x_5478_);
lean_dec_ref(v___x_5478_);
v___x_5480_ = ((lean_object*)(l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NsExport_main_spec__17_spec__23___closed__2));
v___x_5481_ = lean_string_append(v___x_5479_, v___x_5480_);
v___x_5482_ = l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(v___x_5481_);
if (lean_obj_tag(v___x_5482_) == 0)
{
uint8_t v___x_5483_; 
lean_dec_ref_known(v___x_5482_, 1);
v___x_5483_ = lean_nat_dec_eq(v_shard_5374_, v___x_5264_);
lean_dec(v_shard_5374_);
if (v___x_5483_ == 0)
{
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
goto v___jp_5217_;
}
else
{
lean_object* v___x_5484_; 
v___x_5484_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__20___redArg(v___y_5385_, v_tail_5249_, v_tail_5249_, v___x_5258_);
lean_dec(v_tail_5249_);
if (lean_obj_tag(v___x_5484_) == 0)
{
lean_object* v_a_5485_; lean_object* v___x_5486_; lean_object* v___x_5487_; lean_object* v___x_5488_; lean_object* v___x_5489_; 
v_a_5485_ = lean_ctor_get(v___x_5484_, 0);
lean_inc(v_a_5485_);
lean_dec_ref_known(v___x_5484_, 1);
v___x_5486_ = l_Lean_Json_mkObj(v_a_5485_);
lean_dec(v_a_5485_);
v___x_5487_ = lean_unsigned_to_nat(80u);
v___x_5488_ = l_Lean_Json_pretty(v___x_5486_, v___x_5487_);
v___x_5489_ = l_IO_FS_writeFile(v_head_5236_, v___x_5488_);
lean_dec_ref(v___x_5488_);
lean_dec(v_head_5236_);
if (lean_obj_tag(v___x_5489_) == 0)
{
uint8_t v___x_5490_; 
lean_dec_ref_known(v___x_5489_, 1);
v___x_5490_ = lean_nat_dec_lt(v___x_5264_, v___y_5387_);
if (v___x_5490_ == 0)
{
lean_dec_ref(v___y_5378_);
v___y_5266_ = v___x_5391_;
v___y_5267_ = v_snd_5425_;
v___y_5268_ = v_fst_5421_;
v___y_5269_ = v___y_5383_;
v___y_5270_ = v_fst_5418_;
v___y_5271_ = v_fst_5422_;
v___y_5272_ = v___x_5258_;
v___y_5273_ = v_fst_5424_;
v___y_5274_ = v_fst_5419_;
v___y_5275_ = v_fst_5420_;
v___y_5276_ = v___y_5380_;
v___y_5277_ = v_fst_5423_;
v___y_5278_ = v___x_5487_;
v___y_5279_ = v___y_5387_;
v___y_5280_ = v___x_5404_;
goto v___jp_5265_;
}
else
{
uint8_t v___x_5491_; 
v___x_5491_ = lean_nat_dec_le(v___y_5387_, v___y_5387_);
if (v___x_5491_ == 0)
{
if (v___x_5490_ == 0)
{
lean_dec_ref(v___y_5378_);
v___y_5266_ = v___x_5391_;
v___y_5267_ = v_snd_5425_;
v___y_5268_ = v_fst_5421_;
v___y_5269_ = v___y_5383_;
v___y_5270_ = v_fst_5418_;
v___y_5271_ = v_fst_5422_;
v___y_5272_ = v___x_5258_;
v___y_5273_ = v_fst_5424_;
v___y_5274_ = v_fst_5419_;
v___y_5275_ = v_fst_5420_;
v___y_5276_ = v___y_5380_;
v___y_5277_ = v_fst_5423_;
v___y_5278_ = v___x_5487_;
v___y_5279_ = v___y_5387_;
v___y_5280_ = v___x_5404_;
goto v___jp_5265_;
}
else
{
size_t v___x_5492_; lean_object* v___x_5493_; 
v___x_5492_ = lean_usize_of_nat(v___y_5387_);
v___x_5493_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21(v___y_5378_, v___y_5379_, v___x_5492_, v___x_5404_);
lean_dec_ref(v___y_5378_);
v___y_5266_ = v___x_5391_;
v___y_5267_ = v_snd_5425_;
v___y_5268_ = v_fst_5421_;
v___y_5269_ = v___y_5383_;
v___y_5270_ = v_fst_5418_;
v___y_5271_ = v_fst_5422_;
v___y_5272_ = v___x_5258_;
v___y_5273_ = v_fst_5424_;
v___y_5274_ = v_fst_5419_;
v___y_5275_ = v_fst_5420_;
v___y_5276_ = v___y_5380_;
v___y_5277_ = v_fst_5423_;
v___y_5278_ = v___x_5487_;
v___y_5279_ = v___y_5387_;
v___y_5280_ = v___x_5493_;
goto v___jp_5265_;
}
}
else
{
size_t v___x_5494_; lean_object* v___x_5495_; 
v___x_5494_ = lean_usize_of_nat(v___y_5387_);
v___x_5495_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00NsExport_main_spec__21(v___y_5378_, v___y_5379_, v___x_5494_, v___x_5404_);
lean_dec_ref(v___y_5378_);
v___y_5266_ = v___x_5391_;
v___y_5267_ = v_snd_5425_;
v___y_5268_ = v_fst_5421_;
v___y_5269_ = v___y_5383_;
v___y_5270_ = v_fst_5418_;
v___y_5271_ = v_fst_5422_;
v___y_5272_ = v___x_5258_;
v___y_5273_ = v_fst_5424_;
v___y_5274_ = v_fst_5419_;
v___y_5275_ = v_fst_5420_;
v___y_5276_ = v___y_5380_;
v___y_5277_ = v_fst_5423_;
v___y_5278_ = v___x_5487_;
v___y_5279_ = v___y_5387_;
v___y_5280_ = v___x_5495_;
goto v___jp_5265_;
}
}
}
else
{
lean_object* v_a_5496_; lean_object* v___x_5498_; uint8_t v_isShared_5499_; uint8_t v_isSharedCheck_5503_; 
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v___y_5387_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_del_object(v___x_5251_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
v_a_5496_ = lean_ctor_get(v___x_5489_, 0);
v_isSharedCheck_5503_ = !lean_is_exclusive(v___x_5489_);
if (v_isSharedCheck_5503_ == 0)
{
v___x_5498_ = v___x_5489_;
v_isShared_5499_ = v_isSharedCheck_5503_;
goto v_resetjp_5497_;
}
else
{
lean_inc(v_a_5496_);
lean_dec(v___x_5489_);
v___x_5498_ = lean_box(0);
v_isShared_5499_ = v_isSharedCheck_5503_;
goto v_resetjp_5497_;
}
v_resetjp_5497_:
{
lean_object* v___x_5501_; 
if (v_isShared_5499_ == 0)
{
v___x_5501_ = v___x_5498_;
goto v_reusejp_5500_;
}
else
{
lean_object* v_reuseFailAlloc_5502_; 
v_reuseFailAlloc_5502_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5502_, 0, v_a_5496_);
v___x_5501_ = v_reuseFailAlloc_5502_;
goto v_reusejp_5500_;
}
v_reusejp_5500_:
{
return v___x_5501_;
}
}
}
}
else
{
lean_object* v_a_5504_; lean_object* v___x_5506_; uint8_t v_isShared_5507_; uint8_t v_isSharedCheck_5511_; 
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v___y_5387_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_del_object(v___x_5251_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
v_a_5504_ = lean_ctor_get(v___x_5484_, 0);
v_isSharedCheck_5511_ = !lean_is_exclusive(v___x_5484_);
if (v_isSharedCheck_5511_ == 0)
{
v___x_5506_ = v___x_5484_;
v_isShared_5507_ = v_isSharedCheck_5511_;
goto v_resetjp_5505_;
}
else
{
lean_inc(v_a_5504_);
lean_dec(v___x_5484_);
v___x_5506_ = lean_box(0);
v_isShared_5507_ = v_isSharedCheck_5511_;
goto v_resetjp_5505_;
}
v_resetjp_5505_:
{
lean_object* v___x_5509_; 
if (v_isShared_5507_ == 0)
{
v___x_5509_ = v___x_5506_;
goto v_reusejp_5508_;
}
else
{
lean_object* v_reuseFailAlloc_5510_; 
v_reuseFailAlloc_5510_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5510_, 0, v_a_5504_);
v___x_5509_ = v_reuseFailAlloc_5510_;
goto v_reusejp_5508_;
}
v_reusejp_5508_:
{
return v___x_5509_;
}
}
}
}
}
else
{
lean_object* v_a_5512_; lean_object* v___x_5514_; uint8_t v_isShared_5515_; uint8_t v_isSharedCheck_5519_; 
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_shard_5374_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
v_a_5512_ = lean_ctor_get(v___x_5482_, 0);
v_isSharedCheck_5519_ = !lean_is_exclusive(v___x_5482_);
if (v_isSharedCheck_5519_ == 0)
{
v___x_5514_ = v___x_5482_;
v_isShared_5515_ = v_isSharedCheck_5519_;
goto v_resetjp_5513_;
}
else
{
lean_inc(v_a_5512_);
lean_dec(v___x_5482_);
v___x_5514_ = lean_box(0);
v_isShared_5515_ = v_isSharedCheck_5519_;
goto v_resetjp_5513_;
}
v_resetjp_5513_:
{
lean_object* v___x_5517_; 
if (v_isShared_5515_ == 0)
{
v___x_5517_ = v___x_5514_;
goto v_reusejp_5516_;
}
else
{
lean_object* v_reuseFailAlloc_5518_; 
v_reuseFailAlloc_5518_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5518_, 0, v_a_5512_);
v___x_5517_ = v_reuseFailAlloc_5518_;
goto v_reusejp_5516_;
}
v_reusejp_5516_:
{
return v___x_5517_;
}
}
}
}
else
{
lean_object* v_a_5520_; lean_object* v___x_5522_; uint8_t v_isShared_5523_; uint8_t v_isSharedCheck_5527_; 
lean_dec(v_a_5460_);
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
v_a_5520_ = lean_ctor_get(v___x_5462_, 0);
v_isSharedCheck_5527_ = !lean_is_exclusive(v___x_5462_);
if (v_isSharedCheck_5527_ == 0)
{
v___x_5522_ = v___x_5462_;
v_isShared_5523_ = v_isSharedCheck_5527_;
goto v_resetjp_5521_;
}
else
{
lean_inc(v_a_5520_);
lean_dec(v___x_5462_);
v___x_5522_ = lean_box(0);
v_isShared_5523_ = v_isSharedCheck_5527_;
goto v_resetjp_5521_;
}
v_resetjp_5521_:
{
lean_object* v___x_5525_; 
if (v_isShared_5523_ == 0)
{
v___x_5525_ = v___x_5522_;
goto v_reusejp_5524_;
}
else
{
lean_object* v_reuseFailAlloc_5526_; 
v_reuseFailAlloc_5526_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5526_, 0, v_a_5520_);
v___x_5525_ = v_reuseFailAlloc_5526_;
goto v_reusejp_5524_;
}
v_reusejp_5524_:
{
return v___x_5525_;
}
}
}
}
else
{
lean_object* v_a_5528_; lean_object* v___x_5530_; uint8_t v_isShared_5531_; uint8_t v_isSharedCheck_5535_; 
lean_dec(v_a_5460_);
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
v_a_5528_ = lean_ctor_get(v___x_5461_, 0);
v_isSharedCheck_5535_ = !lean_is_exclusive(v___x_5461_);
if (v_isSharedCheck_5535_ == 0)
{
v___x_5530_ = v___x_5461_;
v_isShared_5531_ = v_isSharedCheck_5535_;
goto v_resetjp_5529_;
}
else
{
lean_inc(v_a_5528_);
lean_dec(v___x_5461_);
v___x_5530_ = lean_box(0);
v_isShared_5531_ = v_isSharedCheck_5535_;
goto v_resetjp_5529_;
}
v_resetjp_5529_:
{
lean_object* v___x_5533_; 
if (v_isShared_5531_ == 0)
{
v___x_5533_ = v___x_5530_;
goto v_reusejp_5532_;
}
else
{
lean_object* v_reuseFailAlloc_5534_; 
v_reuseFailAlloc_5534_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5534_, 0, v_a_5528_);
v___x_5533_ = v_reuseFailAlloc_5534_;
goto v_reusejp_5532_;
}
v_reusejp_5532_:
{
return v___x_5533_;
}
}
}
}
else
{
lean_object* v_a_5536_; lean_object* v___x_5538_; uint8_t v_isShared_5539_; uint8_t v_isSharedCheck_5543_; 
lean_dec(v_a_5457_);
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
v_a_5536_ = lean_ctor_get(v___x_5459_, 0);
v_isSharedCheck_5543_ = !lean_is_exclusive(v___x_5459_);
if (v_isSharedCheck_5543_ == 0)
{
v___x_5538_ = v___x_5459_;
v_isShared_5539_ = v_isSharedCheck_5543_;
goto v_resetjp_5537_;
}
else
{
lean_inc(v_a_5536_);
lean_dec(v___x_5459_);
v___x_5538_ = lean_box(0);
v_isShared_5539_ = v_isSharedCheck_5543_;
goto v_resetjp_5537_;
}
v_resetjp_5537_:
{
lean_object* v___x_5541_; 
if (v_isShared_5539_ == 0)
{
v___x_5541_ = v___x_5538_;
goto v_reusejp_5540_;
}
else
{
lean_object* v_reuseFailAlloc_5542_; 
v_reuseFailAlloc_5542_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5542_, 0, v_a_5536_);
v___x_5541_ = v_reuseFailAlloc_5542_;
goto v_reusejp_5540_;
}
v_reusejp_5540_:
{
return v___x_5541_;
}
}
}
}
else
{
lean_object* v_a_5544_; lean_object* v___x_5546_; uint8_t v_isShared_5547_; uint8_t v_isSharedCheck_5551_; 
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v_fst_5417_);
lean_dec(v_fst_5416_);
lean_dec_ref_known(v___x_5403_, 3);
lean_dec(v_a_5402_);
lean_dec_ref(v___y_5388_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_del_object(v___x_5230_);
v_a_5544_ = lean_ctor_get(v___x_5456_, 0);
v_isSharedCheck_5551_ = !lean_is_exclusive(v___x_5456_);
if (v_isSharedCheck_5551_ == 0)
{
v___x_5546_ = v___x_5456_;
v_isShared_5547_ = v_isSharedCheck_5551_;
goto v_resetjp_5545_;
}
else
{
lean_inc(v_a_5544_);
lean_dec(v___x_5456_);
v___x_5546_ = lean_box(0);
v_isShared_5547_ = v_isSharedCheck_5551_;
goto v_resetjp_5545_;
}
v_resetjp_5545_:
{
lean_object* v___x_5549_; 
if (v_isShared_5547_ == 0)
{
v___x_5549_ = v___x_5546_;
goto v_reusejp_5548_;
}
else
{
lean_object* v_reuseFailAlloc_5550_; 
v_reuseFailAlloc_5550_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5550_, 0, v_a_5544_);
v___x_5549_ = v_reuseFailAlloc_5550_;
goto v_reusejp_5548_;
}
v_reusejp_5548_:
{
return v___x_5549_;
}
}
}
}
else
{
lean_object* v_a_5552_; lean_object* v___x_5554_; uint8_t v_isShared_5555_; uint8_t v_isSharedCheck_5559_; 
lean_dec(v_snd_5425_);
lean_dec(v_fst_5424_);
lean_dec(v_fst_5423_);
lean_dec(v_fst_5422_);
lean_dec(v_fst_5421_);
lean_dec(v_fst_5420_);
lean_dec(v_fst_5419_);
lean_dec(v_fst_5418_);
lean_dec(v_fst_5417_);
lean_dec(v_fst_5416_);
lean_dec_ref_known(v___x_5403_, 3);
lean_dec(v_a_5402_);
lean_dec_ref(v___y_5388_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5552_ = lean_ctor_get(v___x_5454_, 0);
v_isSharedCheck_5559_ = !lean_is_exclusive(v___x_5454_);
if (v_isSharedCheck_5559_ == 0)
{
v___x_5554_ = v___x_5454_;
v_isShared_5555_ = v_isSharedCheck_5559_;
goto v_resetjp_5553_;
}
else
{
lean_inc(v_a_5552_);
lean_dec(v___x_5454_);
v___x_5554_ = lean_box(0);
v_isShared_5555_ = v_isSharedCheck_5559_;
goto v_resetjp_5553_;
}
v_resetjp_5553_:
{
lean_object* v___x_5557_; 
if (v_isShared_5555_ == 0)
{
v___x_5557_ = v___x_5554_;
goto v_reusejp_5556_;
}
else
{
lean_object* v_reuseFailAlloc_5558_; 
v_reuseFailAlloc_5558_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5558_, 0, v_a_5552_);
v___x_5557_ = v_reuseFailAlloc_5558_;
goto v_reusejp_5556_;
}
v_reusejp_5556_:
{
return v___x_5557_;
}
}
}
}
else
{
lean_object* v_a_5560_; lean_object* v___x_5562_; uint8_t v_isShared_5563_; uint8_t v_isSharedCheck_5567_; 
lean_dec_ref_known(v___x_5403_, 3);
lean_dec(v_a_5402_);
lean_dec_ref(v___y_5388_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5560_ = lean_ctor_get(v___x_5406_, 0);
v_isSharedCheck_5567_ = !lean_is_exclusive(v___x_5406_);
if (v_isSharedCheck_5567_ == 0)
{
v___x_5562_ = v___x_5406_;
v_isShared_5563_ = v_isSharedCheck_5567_;
goto v_resetjp_5561_;
}
else
{
lean_inc(v_a_5560_);
lean_dec(v___x_5406_);
v___x_5562_ = lean_box(0);
v_isShared_5563_ = v_isSharedCheck_5567_;
goto v_resetjp_5561_;
}
v_resetjp_5561_:
{
lean_object* v___x_5565_; 
if (v_isShared_5563_ == 0)
{
v___x_5565_ = v___x_5562_;
goto v_reusejp_5564_;
}
else
{
lean_object* v_reuseFailAlloc_5566_; 
v_reuseFailAlloc_5566_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5566_, 0, v_a_5560_);
v___x_5565_ = v_reuseFailAlloc_5566_;
goto v_reusejp_5564_;
}
v_reusejp_5564_:
{
return v___x_5565_;
}
}
}
}
else
{
lean_object* v_a_5568_; lean_object* v___x_5570_; uint8_t v_isShared_5571_; uint8_t v_isSharedCheck_5575_; 
lean_dec_ref(v___y_5388_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5386_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5568_ = lean_ctor_get(v___x_5401_, 0);
v_isSharedCheck_5575_ = !lean_is_exclusive(v___x_5401_);
if (v_isSharedCheck_5575_ == 0)
{
v___x_5570_ = v___x_5401_;
v_isShared_5571_ = v_isSharedCheck_5575_;
goto v_resetjp_5569_;
}
else
{
lean_inc(v_a_5568_);
lean_dec(v___x_5401_);
v___x_5570_ = lean_box(0);
v_isShared_5571_ = v_isSharedCheck_5575_;
goto v_resetjp_5569_;
}
v_resetjp_5569_:
{
lean_object* v___x_5573_; 
if (v_isShared_5571_ == 0)
{
v___x_5573_ = v___x_5570_;
goto v_reusejp_5572_;
}
else
{
lean_object* v_reuseFailAlloc_5574_; 
v_reuseFailAlloc_5574_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5574_, 0, v_a_5568_);
v___x_5573_ = v_reuseFailAlloc_5574_;
goto v_reusejp_5572_;
}
v_reusejp_5572_:
{
return v___x_5573_;
}
}
}
}
else
{
lean_object* v_a_5576_; lean_object* v___x_5578_; uint8_t v_isShared_5579_; uint8_t v_isSharedCheck_5583_; 
lean_dec_ref(v___y_5388_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5386_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5382_);
lean_dec_ref(v___y_5381_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5576_ = lean_ctor_get(v___x_5397_, 0);
v_isSharedCheck_5583_ = !lean_is_exclusive(v___x_5397_);
if (v_isSharedCheck_5583_ == 0)
{
v___x_5578_ = v___x_5397_;
v_isShared_5579_ = v_isSharedCheck_5583_;
goto v_resetjp_5577_;
}
else
{
lean_inc(v_a_5576_);
lean_dec(v___x_5397_);
v___x_5578_ = lean_box(0);
v_isShared_5579_ = v_isSharedCheck_5583_;
goto v_resetjp_5577_;
}
v_resetjp_5577_:
{
lean_object* v___x_5581_; 
if (v_isShared_5579_ == 0)
{
v___x_5581_ = v___x_5578_;
goto v_reusejp_5580_;
}
else
{
lean_object* v_reuseFailAlloc_5582_; 
v_reuseFailAlloc_5582_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5582_, 0, v_a_5576_);
v___x_5581_ = v_reuseFailAlloc_5582_;
goto v_reusejp_5580_;
}
v_reusejp_5580_:
{
return v___x_5581_;
}
}
}
}
else
{
lean_object* v_a_5584_; lean_object* v___x_5586_; uint8_t v_isShared_5587_; uint8_t v_isSharedCheck_5591_; 
lean_dec_ref(v___y_5388_);
lean_dec(v___y_5387_);
lean_dec_ref(v___y_5386_);
lean_dec_ref(v___y_5385_);
lean_dec_ref(v___y_5384_);
lean_dec(v___y_5383_);
lean_dec(v___y_5382_);
lean_dec_ref(v___y_5381_);
lean_dec(v___y_5380_);
lean_dec_ref(v___y_5378_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5584_ = lean_ctor_get(v___x_5394_, 0);
v_isSharedCheck_5591_ = !lean_is_exclusive(v___x_5394_);
if (v_isSharedCheck_5591_ == 0)
{
v___x_5586_ = v___x_5394_;
v_isShared_5587_ = v_isSharedCheck_5591_;
goto v_resetjp_5585_;
}
else
{
lean_inc(v_a_5584_);
lean_dec(v___x_5394_);
v___x_5586_ = lean_box(0);
v_isShared_5587_ = v_isSharedCheck_5591_;
goto v_resetjp_5585_;
}
v_resetjp_5585_:
{
lean_object* v___x_5589_; 
if (v_isShared_5587_ == 0)
{
v___x_5589_ = v___x_5586_;
goto v_reusejp_5588_;
}
else
{
lean_object* v_reuseFailAlloc_5590_; 
v_reuseFailAlloc_5590_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5590_, 0, v_a_5584_);
v___x_5589_ = v_reuseFailAlloc_5590_;
goto v_reusejp_5588_;
}
v_reusejp_5588_:
{
return v___x_5589_;
}
}
}
}
v___jp_5592_:
{
lean_object* v___x_5607_; 
v___x_5607_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg(v___y_5595_, v___y_5598_, v___y_5602_, v___y_5606_);
lean_dec(v___y_5606_);
lean_dec(v___y_5595_);
v___y_5378_ = v___y_5593_;
v___y_5379_ = v___y_5594_;
v___y_5380_ = v___y_5599_;
v___y_5381_ = v___y_5600_;
v___y_5382_ = v___y_5601_;
v___y_5383_ = v___y_5596_;
v___y_5384_ = v___y_5603_;
v___y_5385_ = v___y_5597_;
v___y_5386_ = v___y_5604_;
v___y_5387_ = v___y_5605_;
v___y_5388_ = v___x_5607_;
goto v___jp_5377_;
}
v___jp_5608_:
{
uint8_t v___x_5623_; 
v___x_5623_ = lean_nat_dec_le(v___y_5622_, v___y_5618_);
if (v___x_5623_ == 0)
{
lean_dec(v___y_5618_);
lean_inc(v___y_5622_);
v___y_5593_ = v___y_5609_;
v___y_5594_ = v___y_5610_;
v___y_5595_ = v___y_5611_;
v___y_5596_ = v___y_5612_;
v___y_5597_ = v___y_5613_;
v___y_5598_ = v___y_5614_;
v___y_5599_ = v___y_5615_;
v___y_5600_ = v___y_5616_;
v___y_5601_ = v___y_5617_;
v___y_5602_ = v___y_5622_;
v___y_5603_ = v___y_5619_;
v___y_5604_ = v___y_5620_;
v___y_5605_ = v___y_5621_;
v___y_5606_ = v___y_5622_;
goto v___jp_5592_;
}
else
{
v___y_5593_ = v___y_5609_;
v___y_5594_ = v___y_5610_;
v___y_5595_ = v___y_5611_;
v___y_5596_ = v___y_5612_;
v___y_5597_ = v___y_5613_;
v___y_5598_ = v___y_5614_;
v___y_5599_ = v___y_5615_;
v___y_5600_ = v___y_5616_;
v___y_5601_ = v___y_5617_;
v___y_5602_ = v___y_5622_;
v___y_5603_ = v___y_5619_;
v___y_5604_ = v___y_5620_;
v___y_5605_ = v___y_5621_;
v___y_5606_ = v___y_5618_;
goto v___jp_5592_;
}
}
v___jp_5624_:
{
lean_object* v___x_5636_; 
v___x_5636_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__3___redArg(v___y_5632_, v___y_5629_, v___y_5635_, v___y_5635_, v___y_5627_);
lean_dec(v___y_5635_);
if (lean_obj_tag(v___x_5636_) == 0)
{
lean_object* v_a_5637_; lean_object* v___x_5638_; lean_object* v___x_5639_; uint8_t v___x_5640_; 
v_a_5637_ = lean_ctor_get(v___x_5636_, 0);
lean_inc(v_a_5637_);
lean_dec_ref_known(v___x_5636_, 1);
v___x_5638_ = lean_unsigned_to_nat(1u);
v___x_5639_ = lean_array_get_size(v_a_5637_);
v___x_5640_ = lean_nat_dec_eq(v___x_5639_, v___x_5264_);
if (v___x_5640_ == 0)
{
lean_object* v___x_5641_; uint8_t v___x_5642_; 
v___x_5641_ = lean_nat_sub(v___x_5639_, v___x_5638_);
v___x_5642_ = lean_nat_dec_le(v___x_5264_, v___x_5641_);
if (v___x_5642_ == 0)
{
lean_inc(v___x_5641_);
v___y_5609_ = v___y_5625_;
v___y_5610_ = v___y_5626_;
v___y_5611_ = v___x_5639_;
v___y_5612_ = v___y_5631_;
v___y_5613_ = v___y_5632_;
v___y_5614_ = v_a_5637_;
v___y_5615_ = v___y_5628_;
v___y_5616_ = v___y_5629_;
v___y_5617_ = v___x_5638_;
v___y_5618_ = v___x_5641_;
v___y_5619_ = v___y_5630_;
v___y_5620_ = v___y_5633_;
v___y_5621_ = v___y_5634_;
v___y_5622_ = v___x_5641_;
goto v___jp_5608_;
}
else
{
v___y_5609_ = v___y_5625_;
v___y_5610_ = v___y_5626_;
v___y_5611_ = v___x_5639_;
v___y_5612_ = v___y_5631_;
v___y_5613_ = v___y_5632_;
v___y_5614_ = v_a_5637_;
v___y_5615_ = v___y_5628_;
v___y_5616_ = v___y_5629_;
v___y_5617_ = v___x_5638_;
v___y_5618_ = v___x_5641_;
v___y_5619_ = v___y_5630_;
v___y_5620_ = v___y_5633_;
v___y_5621_ = v___y_5634_;
v___y_5622_ = v___x_5264_;
goto v___jp_5608_;
}
}
else
{
v___y_5378_ = v___y_5625_;
v___y_5379_ = v___y_5626_;
v___y_5380_ = v___y_5628_;
v___y_5381_ = v___y_5629_;
v___y_5382_ = v___x_5638_;
v___y_5383_ = v___y_5631_;
v___y_5384_ = v___y_5630_;
v___y_5385_ = v___y_5632_;
v___y_5386_ = v___y_5633_;
v___y_5387_ = v___y_5634_;
v___y_5388_ = v_a_5637_;
goto v___jp_5377_;
}
}
else
{
lean_object* v_a_5643_; lean_object* v___x_5645_; uint8_t v_isShared_5646_; uint8_t v_isSharedCheck_5650_; 
lean_dec(v___y_5634_);
lean_dec_ref(v___y_5633_);
lean_dec_ref(v___y_5632_);
lean_dec(v___y_5631_);
lean_dec_ref(v___y_5630_);
lean_dec_ref(v___y_5629_);
lean_dec(v___y_5628_);
lean_dec_ref(v___y_5625_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5643_ = lean_ctor_get(v___x_5636_, 0);
v_isSharedCheck_5650_ = !lean_is_exclusive(v___x_5636_);
if (v_isSharedCheck_5650_ == 0)
{
v___x_5645_ = v___x_5636_;
v_isShared_5646_ = v_isSharedCheck_5650_;
goto v_resetjp_5644_;
}
else
{
lean_inc(v_a_5643_);
lean_dec(v___x_5636_);
v___x_5645_ = lean_box(0);
v_isShared_5646_ = v_isSharedCheck_5650_;
goto v_resetjp_5644_;
}
v_resetjp_5644_:
{
lean_object* v___x_5648_; 
if (v_isShared_5646_ == 0)
{
v___x_5648_ = v___x_5645_;
goto v_reusejp_5647_;
}
else
{
lean_object* v_reuseFailAlloc_5649_; 
v_reuseFailAlloc_5649_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5649_, 0, v_a_5643_);
v___x_5648_ = v_reuseFailAlloc_5649_;
goto v_reusejp_5647_;
}
v_reusejp_5647_:
{
return v___x_5648_;
}
}
}
}
v___jp_5651_:
{
size_t v_sz_5653_; size_t v___x_5654_; lean_object* v___x_5655_; size_t v_sz_5656_; lean_object* v___x_5657_; lean_object* v___x_5658_; uint32_t v___x_5659_; lean_object* v___x_5660_; uint8_t v___x_5661_; uint8_t v___x_5662_; lean_object* v___x_5663_; lean_object* v___x_5664_; 
v_sz_5653_ = lean_array_size(v___y_5652_);
v___x_5654_ = ((size_t)0ULL);
v___x_5655_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__0(v_sz_5653_, v___x_5654_, v___y_5652_);
v_sz_5656_ = lean_array_size(v___x_5655_);
lean_inc_ref(v___x_5655_);
v___x_5657_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__1(v_sz_5656_, v___x_5654_, v___x_5655_);
v___x_5658_ = l_Lean_Options_empty;
v___x_5659_ = 1024;
v___x_5660_ = ((lean_object*)(l_NsExport_main___closed__39));
v___x_5661_ = 1;
v___x_5662_ = 2;
v___x_5663_ = lean_box(1);
v___x_5664_ = l_Lean_importModules(v___x_5657_, v___x_5658_, v___x_5659_, v___x_5660_, v___x_5263_, v___x_5661_, v___x_5662_, v___x_5663_);
if (lean_obj_tag(v___x_5664_) == 0)
{
lean_object* v_a_5665_; lean_object* v___x_5666_; 
v_a_5665_ = lean_ctor_get(v___x_5664_, 0);
lean_inc(v_a_5665_);
lean_dec_ref_known(v___x_5664_, 1);
v___x_5666_ = l_NsExport_main___lam__0();
if (lean_obj_tag(v___x_5666_) == 0)
{
lean_object* v_a_5667_; lean_object* v___x_5668_; lean_object* v___x_5669_; lean_object* v___x_5670_; lean_object* v___x_5671_; lean_object* v___x_5672_; lean_object* v___x_5673_; lean_object* v___x_5674_; lean_object* v___x_5675_; lean_object* v___x_5676_; lean_object* v___x_5677_; lean_object* v___x_5678_; lean_object* v___x_5679_; lean_object* v___x_5680_; lean_object* v___x_5681_; lean_object* v___x_5682_; lean_object* v___x_5683_; lean_object* v___x_5684_; lean_object* v___x_5685_; lean_object* v___x_5686_; lean_object* v___x_5687_; lean_object* v___x_5688_; lean_object* v___x_5689_; lean_object* v___x_5690_; 
v_a_5667_ = lean_ctor_get(v___x_5666_, 0);
lean_inc(v_a_5667_);
lean_dec_ref_known(v___x_5666_, 1);
v___x_5668_ = ((lean_object*)(l_NsExport_main___closed__40));
lean_inc(v_shard_5374_);
v___x_5669_ = l_Nat_reprFast(v_shard_5374_);
v___x_5670_ = lean_string_append(v___x_5668_, v___x_5669_);
lean_dec_ref(v___x_5669_);
v___x_5671_ = ((lean_object*)(l_NsExport_main___closed__41));
lean_inc_ref(v___x_5670_);
v___x_5672_ = lean_string_append(v___x_5670_, v___x_5671_);
v___x_5673_ = lean_array_get_size(v___x_5655_);
lean_dec_ref(v___x_5655_);
v___x_5674_ = l_Nat_reprFast(v___x_5673_);
v___x_5675_ = lean_string_append(v___x_5672_, v___x_5674_);
lean_dec_ref(v___x_5674_);
v___x_5676_ = ((lean_object*)(l_NsExport_main___closed__42));
v___x_5677_ = lean_string_append(v___x_5675_, v___x_5676_);
v___x_5678_ = lean_nat_sub(v_a_5667_, v_a_5254_);
lean_dec(v_a_5667_);
lean_inc(v___x_5678_);
v___x_5679_ = l_Nat_reprFast(v___x_5678_);
v___x_5680_ = lean_string_append(v___x_5677_, v___x_5679_);
lean_dec_ref(v___x_5679_);
v___x_5681_ = ((lean_object*)(l_NsExport_main___closed__43));
v___x_5682_ = lean_string_append(v___x_5680_, v___x_5681_);
v___x_5683_ = l_Lean_Environment_header(v_a_5665_);
v___x_5684_ = l_Lean_EnvironmentHeader_moduleNames(v___x_5683_);
v___x_5685_ = lean_array_get_size(v___x_5684_);
v___x_5686_ = l_Nat_reprFast(v___x_5685_);
v___x_5687_ = lean_string_append(v___x_5682_, v___x_5686_);
lean_dec_ref(v___x_5686_);
v___x_5688_ = ((lean_object*)(l_NsExport_main___closed__44));
v___x_5689_ = lean_string_append(v___x_5687_, v___x_5688_);
v___x_5690_ = l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(v___x_5689_);
if (lean_obj_tag(v___x_5690_) == 0)
{
lean_object* v___x_5691_; lean_object* v_map_u2081_5692_; lean_object* v_buckets_5693_; size_t v_sz_5694_; lean_object* v___x_5695_; lean_object* v___x_5696_; lean_object* v___x_5697_; lean_object* v___f_5698_; lean_object* v___x_5699_; uint8_t v___x_5700_; 
lean_dec_ref_known(v___x_5690_, 1);
lean_inc_n(v_a_5665_, 2);
v___x_5691_ = l_Lean_Environment_constants(v_a_5665_);
v_map_u2081_5692_ = lean_ctor_get(v___x_5691_, 0);
lean_inc_ref(v_map_u2081_5692_);
lean_dec_ref(v___x_5691_);
v_buckets_5693_ = lean_ctor_get(v_map_u2081_5692_, 1);
lean_inc_ref(v_buckets_5693_);
lean_dec_ref(v_map_u2081_5692_);
v_sz_5694_ = lean_array_size(v___x_5684_);
lean_inc_ref(v___x_5684_);
v___x_5695_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NsExport_main_spec__2(v_sz_5694_, v___x_5654_, v___x_5684_);
v___x_5696_ = lean_box(v___x_5263_);
v___x_5697_ = lean_box(v___x_5263_);
lean_inc_ref(v___x_5695_);
v___f_5698_ = lean_alloc_closure((void*)(l_NsExport_main___lam__1___boxed), 5, 4);
lean_closure_set(v___f_5698_, 0, v_a_5665_);
lean_closure_set(v___f_5698_, 1, v___x_5696_);
lean_closure_set(v___f_5698_, 2, v___x_5697_);
lean_closure_set(v___f_5698_, 3, v___x_5695_);
v___x_5699_ = lean_array_get_size(v_buckets_5693_);
v___x_5700_ = lean_nat_dec_lt(v___x_5264_, v___x_5699_);
if (v___x_5700_ == 0)
{
lean_dec_ref(v_buckets_5693_);
v___y_5625_ = v___x_5684_;
v___y_5626_ = v___x_5654_;
v___y_5627_ = v___x_5660_;
v___y_5628_ = v___x_5673_;
v___y_5629_ = v___x_5695_;
v___y_5630_ = v___x_5670_;
v___y_5631_ = v___x_5678_;
v___y_5632_ = v_a_5665_;
v___y_5633_ = v___f_5698_;
v___y_5634_ = v___x_5685_;
v___y_5635_ = v___x_5258_;
goto v___jp_5624_;
}
else
{
size_t v___x_5701_; lean_object* v___x_5702_; 
v___x_5701_ = lean_usize_of_nat(v___x_5699_);
v___x_5702_ = l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00Lean_Kernel_Environment_replay_spec__2(v_buckets_5693_, v___x_5701_, v___x_5654_, v___x_5258_);
lean_dec_ref(v_buckets_5693_);
v___y_5625_ = v___x_5684_;
v___y_5626_ = v___x_5654_;
v___y_5627_ = v___x_5660_;
v___y_5628_ = v___x_5673_;
v___y_5629_ = v___x_5695_;
v___y_5630_ = v___x_5670_;
v___y_5631_ = v___x_5678_;
v___y_5632_ = v_a_5665_;
v___y_5633_ = v___f_5698_;
v___y_5634_ = v___x_5685_;
v___y_5635_ = v___x_5702_;
goto v___jp_5624_;
}
}
else
{
lean_object* v_a_5703_; lean_object* v___x_5705_; uint8_t v_isShared_5706_; uint8_t v_isSharedCheck_5710_; 
lean_dec_ref(v___x_5684_);
lean_dec(v___x_5678_);
lean_dec_ref(v___x_5670_);
lean_dec(v_a_5665_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5703_ = lean_ctor_get(v___x_5690_, 0);
v_isSharedCheck_5710_ = !lean_is_exclusive(v___x_5690_);
if (v_isSharedCheck_5710_ == 0)
{
v___x_5705_ = v___x_5690_;
v_isShared_5706_ = v_isSharedCheck_5710_;
goto v_resetjp_5704_;
}
else
{
lean_inc(v_a_5703_);
lean_dec(v___x_5690_);
v___x_5705_ = lean_box(0);
v_isShared_5706_ = v_isSharedCheck_5710_;
goto v_resetjp_5704_;
}
v_resetjp_5704_:
{
lean_object* v___x_5708_; 
if (v_isShared_5706_ == 0)
{
v___x_5708_ = v___x_5705_;
goto v_reusejp_5707_;
}
else
{
lean_object* v_reuseFailAlloc_5709_; 
v_reuseFailAlloc_5709_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5709_, 0, v_a_5703_);
v___x_5708_ = v_reuseFailAlloc_5709_;
goto v_reusejp_5707_;
}
v_reusejp_5707_:
{
return v___x_5708_;
}
}
}
}
else
{
lean_object* v_a_5711_; lean_object* v___x_5713_; uint8_t v_isShared_5714_; uint8_t v_isSharedCheck_5718_; 
lean_dec(v_a_5665_);
lean_dec_ref(v___x_5655_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5711_ = lean_ctor_get(v___x_5666_, 0);
v_isSharedCheck_5718_ = !lean_is_exclusive(v___x_5666_);
if (v_isSharedCheck_5718_ == 0)
{
v___x_5713_ = v___x_5666_;
v_isShared_5714_ = v_isSharedCheck_5718_;
goto v_resetjp_5712_;
}
else
{
lean_inc(v_a_5711_);
lean_dec(v___x_5666_);
v___x_5713_ = lean_box(0);
v_isShared_5714_ = v_isSharedCheck_5718_;
goto v_resetjp_5712_;
}
v_resetjp_5712_:
{
lean_object* v___x_5716_; 
if (v_isShared_5714_ == 0)
{
v___x_5716_ = v___x_5713_;
goto v_reusejp_5715_;
}
else
{
lean_object* v_reuseFailAlloc_5717_; 
v_reuseFailAlloc_5717_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5717_, 0, v_a_5711_);
v___x_5716_ = v_reuseFailAlloc_5717_;
goto v_reusejp_5715_;
}
v_reusejp_5715_:
{
return v___x_5716_;
}
}
}
}
else
{
lean_object* v_a_5719_; lean_object* v___x_5721_; uint8_t v_isShared_5722_; uint8_t v_isSharedCheck_5726_; 
lean_dec_ref(v___x_5655_);
lean_dec(v_nshards_5376_);
lean_dec(v_shard_5374_);
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_del_object(v___x_5246_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5719_ = lean_ctor_get(v___x_5664_, 0);
v_isSharedCheck_5726_ = !lean_is_exclusive(v___x_5664_);
if (v_isSharedCheck_5726_ == 0)
{
v___x_5721_ = v___x_5664_;
v_isShared_5722_ = v_isSharedCheck_5726_;
goto v_resetjp_5720_;
}
else
{
lean_inc(v_a_5719_);
lean_dec(v___x_5664_);
v___x_5721_ = lean_box(0);
v_isShared_5722_ = v_isSharedCheck_5726_;
goto v_resetjp_5720_;
}
v_resetjp_5720_:
{
lean_object* v___x_5724_; 
if (v_isShared_5722_ == 0)
{
v___x_5724_ = v___x_5721_;
goto v_reusejp_5723_;
}
else
{
lean_object* v_reuseFailAlloc_5725_; 
v_reuseFailAlloc_5725_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5725_, 0, v_a_5719_);
v___x_5724_ = v_reuseFailAlloc_5725_;
goto v_reusejp_5723_;
}
v_reusejp_5723_:
{
return v___x_5724_;
}
}
}
}
}
else
{
lean_object* v_a_5737_; lean_object* v___x_5739_; uint8_t v_isShared_5740_; uint8_t v_isSharedCheck_5744_; 
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_dec(v_head_5248_);
lean_del_object(v___x_5246_);
lean_dec(v_head_5244_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
v_a_5737_ = lean_ctor_get(v___x_5261_, 0);
v_isSharedCheck_5744_ = !lean_is_exclusive(v___x_5261_);
if (v_isSharedCheck_5744_ == 0)
{
v___x_5739_ = v___x_5261_;
v_isShared_5740_ = v_isSharedCheck_5744_;
goto v_resetjp_5738_;
}
else
{
lean_inc(v_a_5737_);
lean_dec(v___x_5261_);
v___x_5739_ = lean_box(0);
v_isShared_5740_ = v_isSharedCheck_5744_;
goto v_resetjp_5738_;
}
v_resetjp_5738_:
{
lean_object* v___x_5742_; 
if (v_isShared_5740_ == 0)
{
v___x_5742_ = v___x_5739_;
goto v_reusejp_5741_;
}
else
{
lean_object* v_reuseFailAlloc_5743_; 
v_reuseFailAlloc_5743_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5743_, 0, v_a_5737_);
v___x_5742_ = v_reuseFailAlloc_5743_;
goto v_reusejp_5741_;
}
v_reusejp_5741_:
{
return v___x_5742_;
}
}
}
}
else
{
lean_object* v_a_5745_; lean_object* v___x_5747_; uint8_t v_isShared_5748_; uint8_t v_isSharedCheck_5752_; 
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_dec(v_head_5248_);
lean_del_object(v___x_5246_);
lean_dec(v_head_5244_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
lean_dec(v_head_5228_);
v_a_5745_ = lean_ctor_get(v___x_5259_, 0);
v_isSharedCheck_5752_ = !lean_is_exclusive(v___x_5259_);
if (v_isSharedCheck_5752_ == 0)
{
v___x_5747_ = v___x_5259_;
v_isShared_5748_ = v_isSharedCheck_5752_;
goto v_resetjp_5746_;
}
else
{
lean_inc(v_a_5745_);
lean_dec(v___x_5259_);
v___x_5747_ = lean_box(0);
v_isShared_5748_ = v_isSharedCheck_5752_;
goto v_resetjp_5746_;
}
v_resetjp_5746_:
{
lean_object* v___x_5750_; 
if (v_isShared_5748_ == 0)
{
v___x_5750_ = v___x_5747_;
goto v_reusejp_5749_;
}
else
{
lean_object* v_reuseFailAlloc_5751_; 
v_reuseFailAlloc_5751_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5751_, 0, v_a_5745_);
v___x_5750_ = v_reuseFailAlloc_5751_;
goto v_reusejp_5749_;
}
v_reusejp_5749_:
{
return v___x_5750_;
}
}
}
}
else
{
lean_object* v_a_5753_; lean_object* v___x_5755_; uint8_t v_isShared_5756_; uint8_t v_isSharedCheck_5760_; 
lean_dec(v_a_5254_);
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_dec(v_head_5248_);
lean_del_object(v___x_5246_);
lean_dec(v_head_5244_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
lean_dec(v_head_5228_);
v_a_5753_ = lean_ctor_get(v___x_5256_, 0);
v_isSharedCheck_5760_ = !lean_is_exclusive(v___x_5256_);
if (v_isSharedCheck_5760_ == 0)
{
v___x_5755_ = v___x_5256_;
v_isShared_5756_ = v_isSharedCheck_5760_;
goto v_resetjp_5754_;
}
else
{
lean_inc(v_a_5753_);
lean_dec(v___x_5256_);
v___x_5755_ = lean_box(0);
v_isShared_5756_ = v_isSharedCheck_5760_;
goto v_resetjp_5754_;
}
v_resetjp_5754_:
{
lean_object* v___x_5758_; 
if (v_isShared_5756_ == 0)
{
v___x_5758_ = v___x_5755_;
goto v_reusejp_5757_;
}
else
{
lean_object* v_reuseFailAlloc_5759_; 
v_reuseFailAlloc_5759_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5759_, 0, v_a_5753_);
v___x_5758_ = v_reuseFailAlloc_5759_;
goto v_reusejp_5757_;
}
v_reusejp_5757_:
{
return v___x_5758_;
}
}
}
}
else
{
lean_object* v_a_5761_; lean_object* v___x_5763_; uint8_t v_isShared_5764_; uint8_t v_isSharedCheck_5768_; 
lean_del_object(v___x_5251_);
lean_dec(v_tail_5249_);
lean_dec(v_head_5248_);
lean_del_object(v___x_5246_);
lean_dec(v_head_5244_);
lean_del_object(v___x_5242_);
lean_dec(v_head_5240_);
lean_del_object(v___x_5238_);
lean_dec(v_head_5236_);
lean_del_object(v___x_5234_);
lean_dec(v_head_5232_);
lean_del_object(v___x_5230_);
lean_dec(v_head_5228_);
v_a_5761_ = lean_ctor_get(v___x_5253_, 0);
v_isSharedCheck_5768_ = !lean_is_exclusive(v___x_5253_);
if (v_isSharedCheck_5768_ == 0)
{
v___x_5763_ = v___x_5253_;
v_isShared_5764_ = v_isSharedCheck_5768_;
goto v_resetjp_5762_;
}
else
{
lean_inc(v_a_5761_);
lean_dec(v___x_5253_);
v___x_5763_ = lean_box(0);
v_isShared_5764_ = v_isSharedCheck_5768_;
goto v_resetjp_5762_;
}
v_resetjp_5762_:
{
lean_object* v___x_5766_; 
if (v_isShared_5764_ == 0)
{
v___x_5766_ = v___x_5763_;
goto v_reusejp_5765_;
}
else
{
lean_object* v_reuseFailAlloc_5767_; 
v_reuseFailAlloc_5767_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_5767_, 0, v_a_5761_);
v___x_5766_ = v_reuseFailAlloc_5767_;
goto v_reusejp_5765_;
}
v_reusejp_5765_:
{
return v___x_5766_;
}
}
}
}
}
}
}
}
}
}
else
{
lean_dec_ref_known(v_tail_5226_, 2);
lean_dec(v_tail_5227_);
lean_dec_ref_known(v_tail_5225_, 2);
lean_dec_ref_known(v_tail_5224_, 2);
lean_dec_ref_known(v_tail_5223_, 2);
lean_dec_ref_known(v_args_5215_, 2);
goto v___jp_5220_;
}
}
else
{
lean_dec(v_tail_5226_);
lean_dec_ref_known(v_tail_5225_, 2);
lean_dec_ref_known(v_tail_5224_, 2);
lean_dec_ref_known(v_tail_5223_, 2);
lean_dec_ref_known(v_args_5215_, 2);
goto v___jp_5220_;
}
}
else
{
lean_dec_ref_known(v_tail_5224_, 2);
lean_dec(v_tail_5225_);
lean_dec_ref_known(v_tail_5223_, 2);
lean_dec_ref_known(v_args_5215_, 2);
goto v___jp_5220_;
}
}
else
{
lean_dec_ref_known(v_tail_5223_, 2);
lean_dec(v_tail_5224_);
lean_dec_ref_known(v_args_5215_, 2);
goto v___jp_5220_;
}
}
else
{
lean_dec(v_tail_5223_);
lean_dec_ref_known(v_args_5215_, 2);
goto v___jp_5220_;
}
}
else
{
lean_dec(v_args_5215_);
goto v___jp_5220_;
}
v___jp_5217_:
{
lean_object* v___x_5218_; lean_object* v___x_5219_; 
v___x_5218_ = l_NsExport_main___boxed__const__1;
v___x_5219_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_5219_, 0, v___x_5218_);
return v___x_5219_;
}
v___jp_5220_:
{
lean_object* v___x_5221_; lean_object* v___x_5222_; 
v___x_5221_ = ((lean_object*)(l_NsExport_main___closed__1));
v___x_5222_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_5222_, 0, v___x_5221_);
return v___x_5222_;
}
}
}
LEAN_EXPORT lean_object* l_NsExport_main___boxed(lean_object* v_args_5780_, lean_object* v_a_5781_){
_start:
{
lean_object* v_res_5782_; 
v_res_5782_ = l_NsExport_main(v_args_5780_);
return v_res_5782_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3(lean_object* v_a_5783_, lean_object* v___x_5784_, lean_object* v_as_5785_, lean_object* v_as_x27_5786_, lean_object* v_b_5787_, lean_object* v_a_5788_){
_start:
{
lean_object* v___x_5790_; 
v___x_5790_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__3___redArg(v_a_5783_, v___x_5784_, v_as_5785_, v_as_x27_5786_, v_b_5787_);
return v___x_5790_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__3___boxed(lean_object* v_a_5791_, lean_object* v___x_5792_, lean_object* v_as_5793_, lean_object* v_as_x27_5794_, lean_object* v_b_5795_, lean_object* v_a_5796_, lean_object* v___y_5797_){
_start:
{
lean_object* v_res_5798_; 
v_res_5798_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__3(v_a_5791_, v___x_5792_, v_as_5793_, v_as_x27_5794_, v_b_5795_, v_a_5796_);
lean_dec(v_as_x27_5794_);
lean_dec(v_as_5793_);
lean_dec_ref(v___x_5792_);
lean_dec_ref(v_a_5791_);
return v_res_5798_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12(lean_object* v___y_5799_, lean_object* v_a_5800_, lean_object* v___x_5801_, lean_object* v_range_5802_, lean_object* v_b_5803_, lean_object* v_i_5804_, lean_object* v_hs_5805_, lean_object* v_hl_5806_){
_start:
{
lean_object* v___x_5808_; 
v___x_5808_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___redArg(v___y_5799_, v_a_5800_, v___x_5801_, v_range_5802_, v_b_5803_, v_i_5804_);
return v___x_5808_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12___boxed(lean_object* v___y_5809_, lean_object* v_a_5810_, lean_object* v___x_5811_, lean_object* v_range_5812_, lean_object* v_b_5813_, lean_object* v_i_5814_, lean_object* v_hs_5815_, lean_object* v_hl_5816_, lean_object* v___y_5817_){
_start:
{
lean_object* v_res_5818_; 
v_res_5818_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00NsExport_main_spec__12(v___y_5809_, v_a_5810_, v___x_5811_, v_range_5812_, v_b_5813_, v_i_5814_, v_hs_5815_, v_hl_5816_);
lean_dec_ref(v_range_5812_);
lean_dec_ref(v___x_5811_);
lean_dec_ref(v___y_5809_);
return v_res_5818_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20(lean_object* v_a_5819_, lean_object* v_as_5820_, lean_object* v_as_x27_5821_, lean_object* v_b_5822_, lean_object* v_a_5823_){
_start:
{
lean_object* v___x_5825_; 
v___x_5825_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__20___redArg(v_a_5819_, v_as_5820_, v_as_x27_5821_, v_b_5822_);
return v___x_5825_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NsExport_main_spec__20___boxed(lean_object* v_a_5826_, lean_object* v_as_5827_, lean_object* v_as_x27_5828_, lean_object* v_b_5829_, lean_object* v_a_5830_, lean_object* v___y_5831_){
_start:
{
lean_object* v_res_5832_; 
v_res_5832_ = l_List_forIn_x27_loop___at___00NsExport_main_spec__20(v_a_5826_, v_as_5827_, v_as_x27_5828_, v_b_5829_, v_a_5830_);
lean_dec(v_as_x27_5828_);
lean_dec(v_as_5827_);
return v_res_5832_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22(lean_object* v_n_5833_, lean_object* v_as_5834_, lean_object* v_lo_5835_, lean_object* v_hi_5836_, lean_object* v_w_5837_, lean_object* v_hlo_5838_, lean_object* v_hhi_5839_){
_start:
{
lean_object* v___x_5840_; 
v___x_5840_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___redArg(v_n_5833_, v_as_5834_, v_lo_5835_, v_hi_5836_);
return v___x_5840_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22___boxed(lean_object* v_n_5841_, lean_object* v_as_5842_, lean_object* v_lo_5843_, lean_object* v_hi_5844_, lean_object* v_w_5845_, lean_object* v_hlo_5846_, lean_object* v_hhi_5847_){
_start:
{
lean_object* v_res_5848_; 
v_res_5848_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22(v_n_5841_, v_as_5842_, v_lo_5843_, v_hi_5844_, v_w_5845_, v_hlo_5846_, v_hhi_5847_);
lean_dec(v_hi_5844_);
lean_dec(v_n_5841_);
return v_res_5848_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4(lean_object* v_a_5849_, lean_object* v___x_5850_, lean_object* v_as_5851_, lean_object* v_as_x27_5852_, lean_object* v_b_5853_, lean_object* v_a_5854_){
_start:
{
lean_object* v___x_5856_; 
v___x_5856_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___redArg(v_a_5849_, v___x_5850_, v_as_x27_5852_, v_b_5853_);
return v___x_5856_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4___boxed(lean_object* v_a_5857_, lean_object* v___x_5858_, lean_object* v_as_5859_, lean_object* v_as_x27_5860_, lean_object* v_b_5861_, lean_object* v_a_5862_, lean_object* v___y_5863_){
_start:
{
lean_object* v_res_5864_; 
v_res_5864_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__3_spec__4(v_a_5857_, v___x_5858_, v_as_5859_, v_as_x27_5860_, v_b_5861_, v_a_5862_);
lean_dec(v_as_x27_5860_);
lean_dec(v_as_5859_);
lean_dec_ref(v___x_5858_);
lean_dec_ref(v_a_5857_);
return v_res_5864_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27(lean_object* v_a_5865_, lean_object* v_as_5866_, lean_object* v_as_x27_5867_, lean_object* v_b_5868_, lean_object* v_a_5869_){
_start:
{
lean_object* v___x_5871_; 
v___x_5871_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___redArg(v_a_5865_, v_as_x27_5867_, v_b_5868_);
return v___x_5871_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27___boxed(lean_object* v_a_5872_, lean_object* v_as_5873_, lean_object* v_as_x27_5874_, lean_object* v_b_5875_, lean_object* v_a_5876_, lean_object* v___y_5877_){
_start:
{
lean_object* v_res_5878_; 
v_res_5878_ = l_List_forIn_x27_loop___at___00List_forIn_x27_loop___at___00NsExport_main_spec__20_spec__27(v_a_5872_, v_as_5873_, v_as_x27_5874_, v_b_5875_, v_a_5876_);
lean_dec(v_as_x27_5874_);
lean_dec(v_as_5873_);
return v_res_5878_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31(lean_object* v_n_5879_, lean_object* v_lo_5880_, lean_object* v_hi_5881_, lean_object* v_hhi_5882_, lean_object* v_pivot_5883_, lean_object* v_as_5884_, lean_object* v_i_5885_, lean_object* v_k_5886_, lean_object* v_ilo_5887_, lean_object* v_ik_5888_, lean_object* v_w_5889_){
_start:
{
lean_object* v___x_5890_; 
v___x_5890_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___redArg(v_hi_5881_, v_pivot_5883_, v_as_5884_, v_i_5885_, v_k_5886_);
return v___x_5890_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31___boxed(lean_object* v_n_5891_, lean_object* v_lo_5892_, lean_object* v_hi_5893_, lean_object* v_hhi_5894_, lean_object* v_pivot_5895_, lean_object* v_as_5896_, lean_object* v_i_5897_, lean_object* v_k_5898_, lean_object* v_ilo_5899_, lean_object* v_ik_5900_, lean_object* v_w_5901_){
_start:
{
lean_object* v_res_5902_; 
v_res_5902_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00NsExport_main_spec__22_spec__31(v_n_5891_, v_lo_5892_, v_hi_5893_, v_hhi_5894_, v_pivot_5895_, v_as_5896_, v_i_5897_, v_k_5898_, v_ilo_5899_, v_ik_5900_, v_w_5901_);
lean_dec(v_hi_5893_);
lean_dec(v_lo_5892_);
lean_dec(v_n_5891_);
return v_res_5902_;
}
}
LEAN_EXPORT lean_object* _lean_main(lean_object* v_args_5903_){
_start:
{
lean_object* v___x_5905_; 
v___x_5905_ = l_NsExport_main(v_args_5903_);
return v___x_5905_;
}
}
LEAN_EXPORT lean_object* l_main___boxed(lean_object* v_args_5906_, lean_object* v_a_5907_){
_start:
{
lean_object* v_res_5908_; 
v_res_5908_ = _lean_main(v_args_5906_);
return v_res_5908_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Lean(uint8_t builtin);
void lean_initialize();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_Export(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize();
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Lean(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
l_NsExport_instInhabitedCls_default = _init_l_NsExport_instInhabitedCls_default();
lean_mark_persistent(l_NsExport_instInhabitedCls_default);
l_NsExport_instInhabitedCls = _init_l_NsExport_instInhabitedCls();
lean_mark_persistent(l_NsExport_instInhabitedCls);
l_NsExport_main___boxed__const__1 = _init_l_NsExport_main___boxed__const__1();
lean_mark_persistent(l_NsExport_main___boxed__const__1);
return lean_io_result_mk_ok(lean_box(0));
}
char ** lean_setup_args(int argc, char ** argv);
#if defined(WIN32) || defined(_WIN32)
#include <windows.h>
#endif
lean_object* run_main(int argc, char ** argv) {
    lean_object* in = lean_box(0);
    int i = argc;
    while (i > 1) {
      lean_object* n;
      i--;
      n = lean_alloc_ctor(1,2,0); lean_ctor_set(n, 0, lean_mk_string(argv[i])); lean_ctor_set(n, 1, in);
      in = n;
    }
    return _lean_main(in);
}
int main(int argc, char ** argv) {
#if defined(WIN32) || defined(_WIN32)
  SetErrorMode(SEM_FAILCRITICALERRORS);
  SetConsoleOutputCP(CP_UTF8);
#endif
  lean_object* res;
  argv = lean_setup_args(argc, argv);
  res = initialize_Export(1 /* builtin */);
  lean_io_mark_end_initialization();
  if (lean_io_result_is_ok(res)) {
    lean_dec_ref(res);
    lean_init_task_manager();
    res = lean_run_main(&run_main, argc, argv);
  }
  lean_finalize_task_manager();
  if (lean_io_result_is_ok(res)) {
    int ret = lean_unbox_uint32(lean_io_result_get_value(res));
    lean_dec_ref(res);
    return ret;
  } else {
    lean_io_result_show_error(res);
    lean_dec_ref(res);
    return 1;
  }
}
#ifdef __cplusplus
}
#endif
