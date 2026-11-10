// Lean compiler output
// Module: StmtKeys
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
size_t lean_usize_add(size_t, size_t);
uint8_t lean_usize_dec_lt(size_t, size_t);
lean_object* lean_array_get(lean_object*, lean_object*, lean_object*);
lean_object* lean_array_set(lean_object*, lean_object*, lean_object*);
lean_object* lean_array_push(lean_object*, lean_object*);
lean_object* lean_array_uget_borrowed(lean_object*, size_t);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
lean_object* lean_array_uget(lean_object*, size_t);
lean_object* lean_array_uset(lean_object*, size_t, lean_object*);
lean_object* l_String_toName(lean_object*);
lean_object* l_Lean_Environment_getModuleIdxFor_x3f(lean_object*, lean_object*);
lean_object* l_Lean_ConstantInfo_type(lean_object*);
lean_object* lean_mk_array(lean_object*, lean_object*);
uint64_t lean_uint64_mix_hash(uint64_t, uint64_t);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Meta_ForEachExpr_0__Lean_Meta_forEachExpr_x27_visit___at___00Lean_Meta_forEachExpr_x27___at___00__private_Lean_Linter_Extra_UnusedDecidableInType_0__Lean_Linter_Extra_UnusedDecidableInType_collectFVarsOutsideOfProofs_spec__0_spec__0_spec__2___redArg(lean_object*, lean_object*, lean_object*);
uint64_t lean_uint64_of_nat(lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00Lean_Elab_Command_elabOmit_spec__7___redArg(lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__0___redArg(lean_object*, lean_object*);
lean_object* lean_array_get_size(lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(lean_object*, lean_object*, lean_object*);
uint64_t lean_string_hash(lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Meta_ForEachExpr_0__Lean_Meta_forEachExpr_x27_visit___at___00Lean_Meta_forEachExpr_x27___at___00__private_Lean_Linter_Extra_UnusedDecidableInType_0__Lean_Linter_Extra_UnusedDecidableInType_collectFVarsOutsideOfProofs_spec__0_spec__0_spec__1___redArg(lean_object*, lean_object*);
lean_object* l_Lean_Expr_getAppFn(lean_object*);
lean_object* l_Lean_Expr_getAppNumArgs(lean_object*);
lean_object* l_Lean_Expr_sort___override(lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
lean_object* l___private_Lean_Expr_0__Lean_Expr_getAppArgsAux(lean_object*, lean_object*, lean_object*);
size_t lean_array_size(lean_object*);
lean_object* l_Lean_Expr_consumeMData(lean_object*);
lean_object* l_Lean_Name_mkStr2(lean_object*, lean_object*);
uint8_t l_Lean_Expr_isConstOf(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
extern lean_object* l_Lean_instInhabitedExpr;
lean_object* l_Lean_Name_mkStr1(lean_object*);
lean_object* lean_array_fget_borrowed(lean_object*, lean_object*);
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
lean_object* lean_array_fswap(lean_object*, lean_object*, lean_object*);
uint8_t lean_uint64_dec_lt(uint64_t, uint64_t);
lean_object* lean_nat_add(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_shiftr(lean_object*, lean_object*);
lean_object* lean_array_get_borrowed(lean_object*, lean_object*, lean_object*);
uint8_t l_Lean_Expr_hasFVar(lean_object*);
uint8_t l_Array_contains___at___00Lean_Meta_CheckAssignment_checkMVar_spec__14(lean_object*, lean_object*);
uint8_t l_Std_DHashMap_Internal_Raw_u2080_contains___at___00__private_Lean_Util_OccursCheck_0__Lean_occursCheck_visit___at___00Lean_occursCheck___at___00Lean_Meta_CheckAssignment_checkMVar_spec__21_spec__24_spec__28___redArg(lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insertIfNew___at___00__private_Lean_Util_OccursCheck_0__Lean_occursCheck_visit___at___00Lean_occursCheck___at___00Lean_Meta_CheckAssignment_checkMVar_spec__21_spec__24_spec__29___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Name_getRoot(lean_object*);
uint8_t l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(lean_object*, lean_object*);
lean_object* lean_array_fget(lean_object*, lean_object*);
uint8_t lean_uint64_dec_eq(uint64_t, uint64_t);
lean_object* l_Array_instInhabited(lean_object*);
uint8_t lean_usize_dec_eq(size_t, size_t);
lean_object* l_Lean_Environment_find_x3f(lean_object*, lean_object*, uint8_t);
lean_object* l_Lean_Name_num___override(lean_object*, lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_insert___at___00Lean_Elab_Command_elabOmit_spec__3___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_findSysroot(lean_object*);
lean_object* l_Lean_initSearchPath(lean_object*, lean_object*);
lean_object* lean_enable_initializer_execution();
lean_object* l_IO_FS_lines(lean_object*);
lean_object* lean_io_prim_handle_mk(lean_object*, uint8_t);
lean_object* lean_expr_instantiate_rev(lean_object*, lean_object*);
lean_object* l_Lean_Expr_fvar___override(lean_object*);
lean_object* l_List_range(lean_object*);
lean_object* l_List_reverse___redArg(lean_object*);
lean_object* l_List_lengthTR___redArg(lean_object*);
lean_object* l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lean_uint64_to_nat(uint64_t);
lean_object* l_Nat_toDigits(lean_object*, lean_object*);
lean_object* lean_string_mk(lean_object*);
lean_object* lean_string_length(lean_object*);
lean_object* l___private_Init_Data_Nat_Basic_0__Nat_repeatTR_loop___at___00Std_Time_instToStringDuration_leftPad_spec__0(lean_object*, lean_object*);
lean_object* lean_string_append(lean_object*, lean_object*);
lean_object* l_Array_extract___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(lean_object*, uint8_t);
lean_object* l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(lean_object*);
lean_object* l_Lean_JsonNumber_fromNat(lean_object*);
lean_object* l_Lean_Json_mkObj(lean_object*);
lean_object* l_Lean_Json_compress(lean_object*);
lean_object* l_IO_FS_Handle_putStrLn(lean_object*, lean_object*);
size_t lean_usize_of_nat(lean_object*);
lean_object* lean_io_prim_handle_flush(lean_object*);
lean_object* l_Nat_reprFast(lean_object*);
lean_object* l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(lean_object*);
extern lean_object* l_Lean_Options_empty;
lean_object* l_Lean_importModules(lean_object*, lean_object*, uint32_t, lean_object*, uint8_t, uint8_t, uint8_t, lean_object*);
lean_object* l_Lean_Environment_header(lean_object*);
lean_object* l_Lean_Environment_constants(lean_object*);
lean_object* l_Lean_EnvironmentHeader_moduleNames(lean_object*);
lean_object* l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00Lean_Kernel_Environment_replay_spec__2(lean_object*, size_t, size_t, lean_object*);
uint8_t lean_string_dec_eq(lean_object*, lean_object*);
static const lean_string_object l_StmtKeys_projectRoots___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "NavierStokes"};
static const lean_object* l_StmtKeys_projectRoots___closed__0 = (const lean_object*)&l_StmtKeys_projectRoots___closed__0_value;
static const lean_ctor_object l_StmtKeys_projectRoots___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_StmtKeys_projectRoots___closed__0_value),LEAN_SCALAR_PTR_LITERAL(254, 13, 58, 167, 114, 207, 206, 89)}};
static const lean_object* l_StmtKeys_projectRoots___closed__1 = (const lean_object*)&l_StmtKeys_projectRoots___closed__1_value;
static const lean_string_object l_StmtKeys_projectRoots___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "Euler"};
static const lean_object* l_StmtKeys_projectRoots___closed__2 = (const lean_object*)&l_StmtKeys_projectRoots___closed__2_value;
static const lean_ctor_object l_StmtKeys_projectRoots___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_StmtKeys_projectRoots___closed__2_value),LEAN_SCALAR_PTR_LITERAL(65, 209, 97, 245, 187, 19, 151, 148)}};
static const lean_object* l_StmtKeys_projectRoots___closed__3 = (const lean_object*)&l_StmtKeys_projectRoots___closed__3_value;
static const lean_string_object l_StmtKeys_projectRoots___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "ComparatorChallenges"};
static const lean_object* l_StmtKeys_projectRoots___closed__4 = (const lean_object*)&l_StmtKeys_projectRoots___closed__4_value;
static const lean_ctor_object l_StmtKeys_projectRoots___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_StmtKeys_projectRoots___closed__4_value),LEAN_SCALAR_PTR_LITERAL(152, 154, 184, 93, 2, 207, 180, 225)}};
static const lean_object* l_StmtKeys_projectRoots___closed__5 = (const lean_object*)&l_StmtKeys_projectRoots___closed__5_value;
static const lean_ctor_object l_StmtKeys_projectRoots___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_StmtKeys_projectRoots___closed__5_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* l_StmtKeys_projectRoots___closed__6 = (const lean_object*)&l_StmtKeys_projectRoots___closed__6_value;
static const lean_ctor_object l_StmtKeys_projectRoots___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_StmtKeys_projectRoots___closed__3_value),((lean_object*)&l_StmtKeys_projectRoots___closed__6_value)}};
static const lean_object* l_StmtKeys_projectRoots___closed__7 = (const lean_object*)&l_StmtKeys_projectRoots___closed__7_value;
static const lean_ctor_object l_StmtKeys_projectRoots___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_StmtKeys_projectRoots___closed__1_value),((lean_object*)&l_StmtKeys_projectRoots___closed__7_value)}};
static const lean_object* l_StmtKeys_projectRoots___closed__8 = (const lean_object*)&l_StmtKeys_projectRoots___closed__8_value;
LEAN_EXPORT const lean_object* l_StmtKeys_projectRoots = (const lean_object*)&l_StmtKeys_projectRoots___closed__8_value;
LEAN_EXPORT uint64_t l_StmtKeys_tokNum;
LEAN_EXPORT uint64_t l_StmtKeys_tokLit;
LEAN_EXPORT uint64_t l_StmtKeys_tokHoleProv;
LEAN_EXPORT uint64_t l_StmtKeys_tokVarProv;
static const lean_ctor_object l_StmtKeys_renameConst___boxed__const__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(251, 3, 0, 0, 0, 0, 0, 0)}};
LEAN_EXPORT const lean_object* l_StmtKeys_renameConst___boxed__const__1 = (const lean_object*)&l_StmtKeys_renameConst___boxed__const__1_value;
LEAN_EXPORT lean_object* l_StmtKeys_renameConst(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t l_StmtKeys_isRawNat(lean_object*);
LEAN_EXPORT lean_object* l_StmtKeys_isRawNat___boxed(lean_object*);
static const lean_ctor_object l_StmtKeys_hx___boxed__const__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(253, 3, 0, 0, 0, 0, 0, 0)}};
LEAN_EXPORT const lean_object* l_StmtKeys_hx___boxed__const__1 = (const lean_object*)&l_StmtKeys_hx___boxed__const__1_value;
static const lean_ctor_object l_StmtKeys_hx___boxed__const__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(41, 0, 0, 0, 0, 0, 0, 0)}};
LEAN_EXPORT const lean_object* l_StmtKeys_hx___boxed__const__2 = (const lean_object*)&l_StmtKeys_hx___boxed__const__2_value;
static const lean_ctor_object l_StmtKeys_hx___boxed__const__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(43, 0, 0, 0, 0, 0, 0, 0)}};
LEAN_EXPORT const lean_object* l_StmtKeys_hx___boxed__const__3 = (const lean_object*)&l_StmtKeys_hx___boxed__const__3_value;
static const lean_ctor_object l_StmtKeys_hx___boxed__const__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(245, 3, 0, 0, 0, 0, 0, 0)}};
LEAN_EXPORT const lean_object* l_StmtKeys_hx___boxed__const__4 = (const lean_object*)&l_StmtKeys_hx___boxed__const__4_value;
static lean_once_cell_t l_StmtKeys_hx___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_StmtKeys_hx___closed__0;
static const lean_string_object l_StmtKeys_hx___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "ofNat"};
static const lean_object* l_StmtKeys_hx___closed__2 = (const lean_object*)&l_StmtKeys_hx___closed__2_value;
static const lean_string_object l_StmtKeys_hx___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "OfNat"};
static const lean_object* l_StmtKeys_hx___closed__1 = (const lean_object*)&l_StmtKeys_hx___closed__1_value;
static const lean_ctor_object l_StmtKeys_hx___closed__3_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l_StmtKeys_hx___closed__1_value),LEAN_SCALAR_PTR_LITERAL(135, 241, 166, 108, 243, 216, 193, 244)}};
static const lean_ctor_object l_StmtKeys_hx___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&l_StmtKeys_hx___closed__3_value_aux_0),((lean_object*)&l_StmtKeys_hx___closed__2_value),LEAN_SCALAR_PTR_LITERAL(2, 108, 58, 34, 100, 49, 50, 216)}};
static const lean_object* l_StmtKeys_hx___closed__3 = (const lean_object*)&l_StmtKeys_hx___closed__3_value;
LEAN_EXPORT lean_object* l_StmtKeys_hx(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_hx_spec__0(lean_object*, lean_object*, lean_object*, size_t, size_t, uint64_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_hx_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint64_t l_StmtKeys_plainKey___lam__0(lean_object*);
LEAN_EXPORT lean_object* l_StmtKeys_plainKey___lam__0___boxed(lean_object*);
static const lean_closure_object l_StmtKeys_plainKey___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_StmtKeys_plainKey___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* l_StmtKeys_plainKey___closed__0 = (const lean_object*)&l_StmtKeys_plainKey___closed__0_value;
static lean_once_cell_t l_StmtKeys_plainKey___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_StmtKeys_plainKey___closed__1;
static lean_once_cell_t l_StmtKeys_plainKey___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_StmtKeys_plainKey___closed__2;
static const lean_array_object l_StmtKeys_plainKey___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l_StmtKeys_plainKey___closed__3 = (const lean_object*)&l_StmtKeys_plainKey___closed__3_value;
static lean_once_cell_t l_StmtKeys_plainKey___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_StmtKeys_plainKey___closed__4;
LEAN_EXPORT lean_object* l_StmtKeys_plainKey(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_StmtKeys_jointKey(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_StmtKeys_fvarOrder(lean_object*, lean_object*);
static lean_once_cell_t l_StmtKeys_fvarsOf___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_StmtKeys_fvarsOf___closed__0;
LEAN_EXPORT lean_object* l_StmtKeys_fvarsOf(lean_object*);
static const lean_string_object l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "v"};
static const lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__0 = (const lean_object*)&l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__0_value;
static const lean_ctor_object l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__0_value),LEAN_SCALAR_PTR_LITERAL(166, 108, 188, 174, 117, 112, 110, 72)}};
static const lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__1 = (const lean_object*)&l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__1_value;
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l_StmtKeys_permKey___lam__1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_StmtKeys_permKey___lam__1___closed__0;
LEAN_EXPORT lean_object* l_StmtKeys_permKey___lam__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_StmtKeys_permKey___lam__1___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2_spec__2(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2_spec__2___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0;
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__7(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__7___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__11(lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__11___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0(uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3_spec__4(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3_spec__4___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__13(lean_object*, lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__13___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__0___redArg(lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___redArg(lean_object*, uint64_t, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint64_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__12(lean_object*, size_t, size_t, uint64_t);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__12___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_filterTR_loop___at___00StmtKeys_permKey_spec__6(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_filterTR_loop___at___00StmtKeys_permKey_spec__6___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__9(lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__9___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_permKey_spec__1(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_permKey_spec__1___boxed(lean_object*, lean_object*, lean_object*);
static const lean_array_object l_StmtKeys_permKey___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l_StmtKeys_permKey___closed__0 = (const lean_object*)&l_StmtKeys_permKey___closed__0_value;
LEAN_EXPORT lean_object* l_StmtKeys_permKey(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16(lean_object*, lean_object*, lean_object*, lean_object*, uint64_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_string_object l_StmtKeys_hex64___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 1, .m_capacity = 1, .m_length = 0, .m_data = ""};
static const lean_object* l_StmtKeys_hex64___closed__0 = (const lean_object*)&l_StmtKeys_hex64___closed__0_value;
LEAN_EXPORT lean_object* l_StmtKeys_hex64(uint64_t);
LEAN_EXPORT lean_object* l_StmtKeys_hex64___boxed(lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__2(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4(uint8_t, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_ctor_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3___boxed__const__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
LEAN_EXPORT const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3___boxed__const__1 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3___boxed__const__1_value;
LEAN_EXPORT uint64_t l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__5(lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__5___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_ctor_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__0 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__0_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "svE"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__1 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__1_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "svN"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__2 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__2_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "svP"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__3 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__3_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "holesSV"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__4 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__4_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "numHolesSV"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__5 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__5_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "numHolesSVThm"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__6 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__6_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "name"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__7 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__7_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "kE"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__8 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__8_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "kN"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__9 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__9_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "kL"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__10 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__10_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "kP"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__11 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__11_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "kLP"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__12 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__12_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "pE"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__13 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__13_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "pN"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__14 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__14_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "pLP"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__15 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__15_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "binders"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__16 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__16_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "floating"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__17 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__17_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "holesL"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__18 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__18_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "holesP"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__19 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__19_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "numHolesL"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__20 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__20_value;
static const lean_string_object l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "numHolesP"};
static const lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__21 = (const lean_object*)&l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__21_value;
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__1(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__1___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__0(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__7(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__7___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_string_object l_StmtKeys_main___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 38, .m_capacity = 38, .m_length = 37, .m_data = "usage: stmtkeys modules.txt out.jsonl"};
static const lean_object* l_StmtKeys_main___closed__0 = (const lean_object*)&l_StmtKeys_main___closed__0_value;
static const lean_ctor_object l_StmtKeys_main___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 18}, .m_objs = {((lean_object*)&l_StmtKeys_main___closed__0_value)}};
static const lean_object* l_StmtKeys_main___closed__1 = (const lean_object*)&l_StmtKeys_main___closed__1_value;
static const lean_string_object l_StmtKeys_main___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "lean"};
static const lean_object* l_StmtKeys_main___closed__2 = (const lean_object*)&l_StmtKeys_main___closed__2_value;
static const lean_string_object l_StmtKeys_main___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "wrote "};
static const lean_object* l_StmtKeys_main___closed__3 = (const lean_object*)&l_StmtKeys_main___closed__3_value;
static const lean_string_object l_StmtKeys_main___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = " theorems"};
static const lean_object* l_StmtKeys_main___closed__4 = (const lean_object*)&l_StmtKeys_main___closed__4_value;
static const lean_array_object l_StmtKeys_main___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l_StmtKeys_main___closed__5 = (const lean_object*)&l_StmtKeys_main___closed__5_value;
static lean_once_cell_t l_StmtKeys_main___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* l_StmtKeys_main___closed__6;
static const lean_array_object l_StmtKeys_main___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* l_StmtKeys_main___closed__7 = (const lean_object*)&l_StmtKeys_main___closed__7_value;
LEAN_EXPORT lean_object* l_StmtKeys_main___boxed__const__1;
LEAN_EXPORT lean_object* l_StmtKeys_main(lean_object*);
LEAN_EXPORT lean_object* l_StmtKeys_main___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* _lean_main(lean_object*);
LEAN_EXPORT lean_object* l_main___boxed(lean_object*, lean_object*);
static uint64_t _init_l_StmtKeys_tokNum(void){
_start:
{
uint64_t v___x_20_; 
v___x_20_ = 1009ULL;
return v___x_20_;
}
}
static uint64_t _init_l_StmtKeys_tokLit(void){
_start:
{
uint64_t v___x_21_; 
v___x_21_ = 1013ULL;
return v___x_21_;
}
}
static uint64_t _init_l_StmtKeys_tokHoleProv(void){
_start:
{
uint64_t v___x_22_; 
v___x_22_ = 1019ULL;
return v___x_22_;
}
}
static uint64_t _init_l_StmtKeys_tokVarProv(void){
_start:
{
uint64_t v___x_23_; 
v___x_23_ = 1021ULL;
return v___x_23_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_renameConst(lean_object* v_cx_26_, lean_object* v_n_27_, lean_object* v_a_28_){
_start:
{
uint8_t v_final_29_; 
v_final_29_ = lean_ctor_get_uint8(v_cx_26_, sizeof(void*)*3);
if (v_final_29_ == 0)
{
lean_object* v___x_30_; lean_object* v___x_31_; 
lean_dec(v_n_27_);
lean_dec_ref(v_cx_26_);
v___x_30_ = ((lean_object*)(l_StmtKeys_renameConst___boxed__const__1));
v___x_31_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_31_, 0, v___x_30_);
lean_ctor_set(v___x_31_, 1, v_a_28_);
return v___x_31_;
}
else
{
lean_object* v_annot_32_; lean_object* v_memo_33_; lean_object* v_ren_34_; lean_object* v_order_35_; lean_object* v_fv_36_; lean_object* v___x_37_; 
v_annot_32_ = lean_ctor_get(v_cx_26_, 2);
lean_inc_ref(v_annot_32_);
lean_dec_ref(v_cx_26_);
v_memo_33_ = lean_ctor_get(v_a_28_, 0);
v_ren_34_ = lean_ctor_get(v_a_28_, 1);
v_order_35_ = lean_ctor_get(v_a_28_, 2);
v_fv_36_ = lean_ctor_get(v_a_28_, 3);
v___x_37_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__0___redArg(v_ren_34_, v_n_27_);
if (lean_obj_tag(v___x_37_) == 0)
{
lean_object* v___x_39_; uint8_t v_isShared_40_; uint8_t v_isSharedCheck_55_; 
lean_inc_ref(v_fv_36_);
lean_inc_ref(v_order_35_);
lean_inc_ref(v_ren_34_);
lean_inc_ref(v_memo_33_);
v_isSharedCheck_55_ = !lean_is_exclusive(v_a_28_);
if (v_isSharedCheck_55_ == 0)
{
lean_object* v_unused_56_; lean_object* v_unused_57_; lean_object* v_unused_58_; lean_object* v_unused_59_; 
v_unused_56_ = lean_ctor_get(v_a_28_, 3);
lean_dec(v_unused_56_);
v_unused_57_ = lean_ctor_get(v_a_28_, 2);
lean_dec(v_unused_57_);
v_unused_58_ = lean_ctor_get(v_a_28_, 1);
lean_dec(v_unused_58_);
v_unused_59_ = lean_ctor_get(v_a_28_, 0);
lean_dec(v_unused_59_);
v___x_39_ = v_a_28_;
v_isShared_40_ = v_isSharedCheck_55_;
goto v_resetjp_38_;
}
else
{
lean_dec(v_a_28_);
v___x_39_ = lean_box(0);
v_isShared_40_ = v_isSharedCheck_55_;
goto v_resetjp_38_;
}
v_resetjp_38_:
{
lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; lean_object* v___x_45_; 
v___x_41_ = lean_array_get_size(v_order_35_);
lean_inc_n(v_n_27_, 2);
v___x_42_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_ren_34_, v_n_27_, v___x_41_);
v___x_43_ = lean_array_push(v_order_35_, v_n_27_);
if (v_isShared_40_ == 0)
{
lean_ctor_set(v___x_39_, 2, v___x_43_);
lean_ctor_set(v___x_39_, 1, v___x_42_);
v___x_45_ = v___x_39_;
goto v_reusejp_44_;
}
else
{
lean_object* v_reuseFailAlloc_54_; 
v_reuseFailAlloc_54_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_54_, 0, v_memo_33_);
lean_ctor_set(v_reuseFailAlloc_54_, 1, v___x_42_);
lean_ctor_set(v_reuseFailAlloc_54_, 2, v___x_43_);
lean_ctor_set(v_reuseFailAlloc_54_, 3, v_fv_36_);
v___x_45_ = v_reuseFailAlloc_54_;
goto v_reusejp_44_;
}
v_reusejp_44_:
{
uint64_t v___x_46_; uint64_t v___x_47_; uint64_t v___x_48_; lean_object* v___x_49_; uint64_t v___x_50_; uint64_t v___x_51_; lean_object* v___x_52_; lean_object* v___x_53_; 
v___x_46_ = 97ULL;
v___x_47_ = lean_uint64_of_nat(v___x_41_);
v___x_48_ = lean_uint64_mix_hash(v___x_46_, v___x_47_);
v___x_49_ = lean_apply_1(v_annot_32_, v_n_27_);
v___x_50_ = lean_unbox_uint64(v___x_49_);
lean_dec_ref(v___x_49_);
v___x_51_ = lean_uint64_mix_hash(v___x_48_, v___x_50_);
v___x_52_ = lean_box_uint64(v___x_51_);
v___x_53_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_53_, 0, v___x_52_);
lean_ctor_set(v___x_53_, 1, v___x_45_);
return v___x_53_;
}
}
}
else
{
lean_object* v_val_60_; uint64_t v___x_61_; uint64_t v___x_62_; uint64_t v___x_63_; lean_object* v___x_64_; uint64_t v___x_65_; uint64_t v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; 
v_val_60_ = lean_ctor_get(v___x_37_, 0);
lean_inc(v_val_60_);
lean_dec_ref_known(v___x_37_, 1);
v___x_61_ = 97ULL;
v___x_62_ = lean_uint64_of_nat(v_val_60_);
lean_dec(v_val_60_);
v___x_63_ = lean_uint64_mix_hash(v___x_61_, v___x_62_);
v___x_64_ = lean_apply_1(v_annot_32_, v_n_27_);
v___x_65_ = lean_unbox_uint64(v___x_64_);
lean_dec_ref(v___x_64_);
v___x_66_ = lean_uint64_mix_hash(v___x_63_, v___x_65_);
v___x_67_ = lean_box_uint64(v___x_66_);
v___x_68_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_68_, 0, v___x_67_);
lean_ctor_set(v___x_68_, 1, v_a_28_);
return v___x_68_;
}
}
}
}
LEAN_EXPORT uint8_t l_StmtKeys_isRawNat(lean_object* v_x_69_){
_start:
{
switch(lean_obj_tag(v_x_69_))
{
case 9:
{
lean_object* v_a_70_; 
v_a_70_ = lean_ctor_get(v_x_69_, 0);
if (lean_obj_tag(v_a_70_) == 0)
{
uint8_t v___x_71_; 
v___x_71_ = 1;
return v___x_71_;
}
else
{
uint8_t v___x_72_; 
v___x_72_ = 0;
return v___x_72_;
}
}
case 10:
{
lean_object* v_expr_73_; 
v_expr_73_ = lean_ctor_get(v_x_69_, 1);
v_x_69_ = v_expr_73_;
goto _start;
}
default: 
{
uint8_t v___x_75_; 
v___x_75_ = 0;
return v___x_75_;
}
}
}
}
LEAN_EXPORT lean_object* l_StmtKeys_isRawNat___boxed(lean_object* v_x_76_){
_start:
{
uint8_t v_res_77_; lean_object* v_r_78_; 
v_res_77_ = l_StmtKeys_isRawNat(v_x_76_);
lean_dec_ref(v_x_76_);
v_r_78_ = lean_box(v_res_77_);
return v_r_78_;
}
}
static lean_object* _init_l_StmtKeys_hx___closed__0(void){
_start:
{
lean_object* v___x_87_; lean_object* v_dummy_88_; 
v___x_87_ = lean_box(0);
v_dummy_88_ = l_Lean_Expr_sort___override(v___x_87_);
return v_dummy_88_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_hx(lean_object* v_cx_94_, lean_object* v_e_95_, lean_object* v_a_96_){
_start:
{
uint64_t v___y_98_; uint64_t v___y_99_; uint64_t v_h_104_; lean_object* v_memo_105_; lean_object* v_ren_106_; lean_object* v_order_107_; lean_object* v_fv_108_; uint64_t v_h_115_; lean_object* v___y_116_; 
switch(lean_obj_tag(v_e_95_))
{
case 10:
{
lean_object* v_expr_121_; 
v_expr_121_ = lean_ctor_get(v_e_95_, 1);
lean_inc_ref(v_expr_121_);
lean_dec_ref_known(v_e_95_, 2);
v_e_95_ = v_expr_121_;
goto _start;
}
case 0:
{
lean_object* v_deBruijnIndex_123_; uint64_t v___x_124_; uint64_t v___x_125_; uint64_t v___x_126_; lean_object* v___x_127_; lean_object* v___x_128_; 
lean_dec_ref(v_cx_94_);
v_deBruijnIndex_123_ = lean_ctor_get(v_e_95_, 0);
lean_inc(v_deBruijnIndex_123_);
lean_dec_ref_known(v_e_95_, 1);
v___x_124_ = 31ULL;
v___x_125_ = lean_uint64_of_nat(v_deBruijnIndex_123_);
lean_dec(v_deBruijnIndex_123_);
v___x_126_ = lean_uint64_mix_hash(v___x_124_, v___x_125_);
v___x_127_ = lean_box_uint64(v___x_126_);
v___x_128_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_128_, 0, v___x_127_);
lean_ctor_set(v___x_128_, 1, v_a_96_);
return v___x_128_;
}
case 1:
{
lean_object* v_fvarId_129_; lean_object* v_fv_130_; lean_object* v___x_131_; 
lean_dec_ref(v_cx_94_);
v_fvarId_129_ = lean_ctor_get(v_e_95_, 0);
lean_inc(v_fvarId_129_);
lean_dec_ref_known(v_e_95_, 1);
v_fv_130_ = lean_ctor_get(v_a_96_, 3);
v___x_131_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00Lean_Elab_Command_elabOmit_spec__7___redArg(v_fv_130_, v_fvarId_129_);
lean_dec(v_fvarId_129_);
if (lean_obj_tag(v___x_131_) == 0)
{
lean_object* v___x_132_; lean_object* v___x_133_; 
v___x_132_ = ((lean_object*)(l_StmtKeys_hx___boxed__const__1));
v___x_133_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_133_, 0, v___x_132_);
lean_ctor_set(v___x_133_, 1, v_a_96_);
return v___x_133_;
}
else
{
lean_object* v_val_134_; uint64_t v___x_135_; uint64_t v___x_136_; uint64_t v___x_137_; lean_object* v___x_138_; lean_object* v___x_139_; 
v_val_134_ = lean_ctor_get(v___x_131_, 0);
lean_inc(v_val_134_);
lean_dec_ref_known(v___x_131_, 1);
v___x_135_ = 37ULL;
v___x_136_ = lean_uint64_of_nat(v_val_134_);
lean_dec(v_val_134_);
v___x_137_ = lean_uint64_mix_hash(v___x_135_, v___x_136_);
v___x_138_ = lean_box_uint64(v___x_137_);
v___x_139_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_139_, 0, v___x_138_);
lean_ctor_set(v___x_139_, 1, v_a_96_);
return v___x_139_;
}
}
case 2:
{
lean_object* v___x_140_; lean_object* v___x_141_; 
lean_dec_ref_known(v_e_95_, 1);
lean_dec_ref(v_cx_94_);
v___x_140_ = ((lean_object*)(l_StmtKeys_hx___boxed__const__2));
v___x_141_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_141_, 0, v___x_140_);
lean_ctor_set(v___x_141_, 1, v_a_96_);
return v___x_141_;
}
case 3:
{
lean_object* v___x_142_; lean_object* v___x_143_; 
lean_dec_ref_known(v_e_95_, 1);
lean_dec_ref(v_cx_94_);
v___x_142_ = ((lean_object*)(l_StmtKeys_hx___boxed__const__3));
v___x_143_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_143_, 0, v___x_142_);
lean_ctor_set(v___x_143_, 1, v_a_96_);
return v___x_143_;
}
case 4:
{
lean_object* v_declName_144_; lean_object* v_o_149_; uint8_t v_proj_150_; 
v_declName_144_ = lean_ctor_get(v_e_95_, 0);
lean_inc(v_declName_144_);
lean_dec_ref_known(v_e_95_, 2);
v_o_149_ = lean_ctor_get(v_cx_94_, 0);
v_proj_150_ = lean_ctor_get_uint8(v_o_149_, 2);
if (v_proj_150_ == 0)
{
lean_dec_ref(v_cx_94_);
goto v___jp_145_;
}
else
{
lean_object* v_isProj_151_; lean_object* v___x_152_; uint8_t v___x_153_; 
v_isProj_151_ = lean_ctor_get(v_cx_94_, 1);
lean_inc_ref(v_isProj_151_);
lean_inc(v_declName_144_);
v___x_152_ = lean_apply_1(v_isProj_151_, v_declName_144_);
v___x_153_ = lean_unbox(v___x_152_);
if (v___x_153_ == 0)
{
lean_dec_ref(v_cx_94_);
goto v___jp_145_;
}
else
{
lean_object* v___x_154_; 
v___x_154_ = l_StmtKeys_renameConst(v_cx_94_, v_declName_144_, v_a_96_);
return v___x_154_;
}
}
v___jp_145_:
{
uint64_t v___x_146_; 
v___x_146_ = 47ULL;
if (lean_obj_tag(v_declName_144_) == 0)
{
uint64_t v___x_147_; 
v___x_147_ = 1723ULL;
v___y_98_ = v___x_146_;
v___y_99_ = v___x_147_;
goto v___jp_97_;
}
else
{
uint64_t v_hash_148_; 
v_hash_148_ = lean_ctor_get_uint64(v_declName_144_, sizeof(void*)*2);
lean_dec(v_declName_144_);
v___y_98_ = v___x_146_;
v___y_99_ = v_hash_148_;
goto v___jp_97_;
}
}
}
case 9:
{
lean_object* v_a_155_; 
v_a_155_ = lean_ctor_get(v_e_95_, 0);
lean_inc_ref(v_a_155_);
lean_dec_ref_known(v_e_95_, 1);
if (lean_obj_tag(v_a_155_) == 0)
{
lean_object* v_o_156_; uint8_t v_nums_157_; 
v_o_156_ = lean_ctor_get(v_cx_94_, 0);
lean_inc_ref(v_o_156_);
lean_dec_ref(v_cx_94_);
v_nums_157_ = lean_ctor_get_uint8(v_o_156_, 0);
lean_dec_ref(v_o_156_);
if (v_nums_157_ == 0)
{
lean_object* v_val_158_; uint64_t v___x_159_; uint64_t v___x_160_; uint64_t v___x_161_; lean_object* v___x_162_; lean_object* v___x_163_; 
v_val_158_ = lean_ctor_get(v_a_155_, 0);
lean_inc(v_val_158_);
lean_dec_ref_known(v_a_155_, 1);
v___x_159_ = 53ULL;
v___x_160_ = lean_uint64_of_nat(v_val_158_);
lean_dec(v_val_158_);
v___x_161_ = lean_uint64_mix_hash(v___x_159_, v___x_160_);
v___x_162_ = lean_box_uint64(v___x_161_);
v___x_163_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_163_, 0, v___x_162_);
lean_ctor_set(v___x_163_, 1, v_a_96_);
return v___x_163_;
}
else
{
lean_object* v___x_164_; lean_object* v___x_165_; 
lean_dec_ref_known(v_a_155_, 1);
v___x_164_ = ((lean_object*)(l_StmtKeys_hx___boxed__const__4));
v___x_165_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_165_, 0, v___x_164_);
lean_ctor_set(v___x_165_, 1, v_a_96_);
return v___x_165_;
}
}
else
{
lean_object* v_val_166_; uint64_t v___x_167_; uint64_t v___x_168_; uint64_t v___x_169_; lean_object* v___x_170_; lean_object* v___x_171_; 
lean_dec_ref(v_cx_94_);
v_val_166_ = lean_ctor_get(v_a_155_, 0);
lean_inc_ref(v_val_166_);
lean_dec_ref_known(v_a_155_, 1);
v___x_167_ = 59ULL;
v___x_168_ = lean_string_hash(v_val_166_);
lean_dec_ref(v_val_166_);
v___x_169_ = lean_uint64_mix_hash(v___x_167_, v___x_168_);
v___x_170_ = lean_box_uint64(v___x_169_);
v___x_171_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_171_, 0, v___x_170_);
lean_ctor_set(v___x_171_, 1, v_a_96_);
return v___x_171_;
}
}
default: 
{
lean_object* v_memo_172_; lean_object* v_ren_173_; lean_object* v_order_174_; lean_object* v_fv_175_; lean_object* v___x_176_; 
v_memo_172_ = lean_ctor_get(v_a_96_, 0);
v_ren_173_ = lean_ctor_get(v_a_96_, 1);
v_order_174_ = lean_ctor_get(v_a_96_, 2);
v_fv_175_ = lean_ctor_get(v_a_96_, 3);
v___x_176_ = l_Std_DHashMap_Internal_Raw_u2080_Const_get_x3f___at___00__private_Lean_Meta_ForEachExpr_0__Lean_Meta_forEachExpr_x27_visit___at___00Lean_Meta_forEachExpr_x27___at___00__private_Lean_Linter_Extra_UnusedDecidableInType_0__Lean_Linter_Extra_UnusedDecidableInType_collectFVarsOutsideOfProofs_spec__0_spec__0_spec__1___redArg(v_memo_172_, v_e_95_);
if (lean_obj_tag(v___x_176_) == 1)
{
lean_object* v_val_177_; lean_object* v___x_178_; 
lean_dec_ref(v_e_95_);
lean_dec_ref(v_cx_94_);
v_val_177_ = lean_ctor_get(v___x_176_, 0);
lean_inc(v_val_177_);
lean_dec_ref_known(v___x_176_, 1);
v___x_178_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_178_, 0, v_val_177_);
lean_ctor_set(v___x_178_, 1, v_a_96_);
return v___x_178_;
}
else
{
lean_dec(v___x_176_);
switch(lean_obj_tag(v_e_95_))
{
case 5:
{
lean_object* v_o_179_; uint8_t v_nums_180_; lean_object* v___x_181_; lean_object* v_nargs_182_; lean_object* v_dummy_183_; lean_object* v___x_184_; lean_object* v___x_185_; lean_object* v___x_186_; lean_object* v___x_187_; 
v_o_179_ = lean_ctor_get(v_cx_94_, 0);
v_nums_180_ = lean_ctor_get_uint8(v_o_179_, 0);
v___x_181_ = l_Lean_Expr_getAppFn(v_e_95_);
v_nargs_182_ = l_Lean_Expr_getAppNumArgs(v_e_95_);
v_dummy_183_ = lean_obj_once(&l_StmtKeys_hx___closed__0, &l_StmtKeys_hx___closed__0_once, _init_l_StmtKeys_hx___closed__0);
lean_inc(v_nargs_182_);
v___x_184_ = lean_mk_array(v_nargs_182_, v_dummy_183_);
v___x_185_ = lean_unsigned_to_nat(1u);
v___x_186_ = lean_nat_sub(v_nargs_182_, v___x_185_);
lean_dec(v_nargs_182_);
lean_inc_ref(v_e_95_);
v___x_187_ = l___private_Lean_Expr_0__Lean_Expr_getAppArgsAux(v_e_95_, v___x_184_, v___x_186_);
if (v_nums_180_ == 0)
{
lean_inc_ref(v_o_179_);
goto v___jp_188_;
}
else
{
lean_object* v___x_204_; uint8_t v___x_205_; 
v___x_204_ = ((lean_object*)(l_StmtKeys_hx___closed__3));
v___x_205_ = l_Lean_Expr_isConstOf(v___x_181_, v___x_204_);
if (v___x_205_ == 0)
{
lean_inc_ref(v_o_179_);
goto v___jp_188_;
}
else
{
lean_object* v___x_206_; lean_object* v___x_207_; uint8_t v___x_208_; 
v___x_206_ = lean_array_get_size(v___x_187_);
v___x_207_ = lean_unsigned_to_nat(3u);
v___x_208_ = lean_nat_dec_eq(v___x_206_, v___x_207_);
if (v___x_208_ == 0)
{
lean_inc_ref(v_o_179_);
goto v___jp_188_;
}
else
{
lean_object* v___x_209_; lean_object* v___x_210_; uint8_t v___x_211_; 
v___x_209_ = l_Lean_instInhabitedExpr;
v___x_210_ = lean_array_get(v___x_209_, v___x_187_, v___x_185_);
v___x_211_ = l_StmtKeys_isRawNat(v___x_210_);
lean_dec(v___x_210_);
if (v___x_211_ == 0)
{
lean_inc_ref(v_o_179_);
goto v___jp_188_;
}
else
{
lean_object* v___x_212_; lean_object* v___x_213_; lean_object* v___x_214_; lean_object* v_fst_215_; lean_object* v_snd_216_; uint64_t v___x_217_; uint64_t v___x_218_; uint64_t v___x_219_; 
lean_dec_ref(v___x_181_);
v___x_212_ = lean_unsigned_to_nat(0u);
v___x_213_ = lean_array_get(v___x_209_, v___x_187_, v___x_212_);
lean_dec_ref(v___x_187_);
v___x_214_ = l_StmtKeys_hx(v_cx_94_, v___x_213_, v_a_96_);
v_fst_215_ = lean_ctor_get(v___x_214_, 0);
lean_inc(v_fst_215_);
v_snd_216_ = lean_ctor_get(v___x_214_, 1);
lean_inc(v_snd_216_);
lean_dec_ref(v___x_214_);
v___x_217_ = 1009ULL;
v___x_218_ = lean_unbox_uint64(v_fst_215_);
lean_dec(v_fst_215_);
v___x_219_ = lean_uint64_mix_hash(v___x_217_, v___x_218_);
v_h_115_ = v___x_219_;
v___y_116_ = v_snd_216_;
goto v___jp_114_;
}
}
}
}
v___jp_188_:
{
lean_object* v___x_189_; lean_object* v_fst_190_; lean_object* v_snd_191_; uint64_t v___x_192_; lean_object* v___x_193_; uint64_t v___x_194_; uint64_t v___x_195_; uint64_t v___x_196_; uint64_t v___x_197_; size_t v_sz_198_; size_t v___x_199_; lean_object* v___x_200_; lean_object* v_fst_201_; lean_object* v_snd_202_; uint64_t v___x_203_; 
lean_inc_ref(v_cx_94_);
v___x_189_ = l_StmtKeys_hx(v_cx_94_, v___x_181_, v_a_96_);
v_fst_190_ = lean_ctor_get(v___x_189_, 0);
lean_inc(v_fst_190_);
v_snd_191_ = lean_ctor_get(v___x_189_, 1);
lean_inc(v_snd_191_);
lean_dec_ref(v___x_189_);
v___x_192_ = 61ULL;
v___x_193_ = lean_array_get_size(v___x_187_);
v___x_194_ = lean_uint64_of_nat(v___x_193_);
v___x_195_ = lean_unbox_uint64(v_fst_190_);
lean_dec(v_fst_190_);
v___x_196_ = lean_uint64_mix_hash(v___x_195_, v___x_194_);
v___x_197_ = lean_uint64_mix_hash(v___x_192_, v___x_196_);
v_sz_198_ = lean_array_size(v___x_187_);
v___x_199_ = ((size_t)0ULL);
v___x_200_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_hx_spec__0(v_cx_94_, v_o_179_, v___x_187_, v_sz_198_, v___x_199_, v___x_197_, v_snd_191_);
lean_dec_ref(v___x_187_);
lean_dec_ref(v_o_179_);
v_fst_201_ = lean_ctor_get(v___x_200_, 0);
lean_inc(v_fst_201_);
v_snd_202_ = lean_ctor_get(v___x_200_, 1);
lean_inc(v_snd_202_);
lean_dec_ref(v___x_200_);
v___x_203_ = lean_unbox_uint64(v_fst_201_);
lean_dec(v_fst_201_);
v_h_115_ = v___x_203_;
v___y_116_ = v_snd_202_;
goto v___jp_114_;
}
}
case 6:
{
lean_object* v_binderType_220_; lean_object* v_body_221_; lean_object* v___x_222_; lean_object* v_fst_223_; lean_object* v_snd_224_; lean_object* v___x_225_; lean_object* v_fst_226_; lean_object* v_snd_227_; uint64_t v___x_228_; uint64_t v___x_229_; uint64_t v___x_230_; uint64_t v___x_231_; uint64_t v___x_232_; 
v_binderType_220_ = lean_ctor_get(v_e_95_, 1);
v_body_221_ = lean_ctor_get(v_e_95_, 2);
lean_inc_ref(v_binderType_220_);
lean_inc_ref(v_cx_94_);
v___x_222_ = l_StmtKeys_hx(v_cx_94_, v_binderType_220_, v_a_96_);
v_fst_223_ = lean_ctor_get(v___x_222_, 0);
lean_inc(v_fst_223_);
v_snd_224_ = lean_ctor_get(v___x_222_, 1);
lean_inc(v_snd_224_);
lean_dec_ref(v___x_222_);
lean_inc_ref(v_body_221_);
v___x_225_ = l_StmtKeys_hx(v_cx_94_, v_body_221_, v_snd_224_);
v_fst_226_ = lean_ctor_get(v___x_225_, 0);
lean_inc(v_fst_226_);
v_snd_227_ = lean_ctor_get(v___x_225_, 1);
lean_inc(v_snd_227_);
lean_dec_ref(v___x_225_);
v___x_228_ = 67ULL;
v___x_229_ = lean_unbox_uint64(v_fst_223_);
lean_dec(v_fst_223_);
v___x_230_ = lean_unbox_uint64(v_fst_226_);
lean_dec(v_fst_226_);
v___x_231_ = lean_uint64_mix_hash(v___x_229_, v___x_230_);
v___x_232_ = lean_uint64_mix_hash(v___x_228_, v___x_231_);
v_h_115_ = v___x_232_;
v___y_116_ = v_snd_227_;
goto v___jp_114_;
}
case 7:
{
lean_object* v_binderType_233_; lean_object* v_body_234_; lean_object* v___x_235_; lean_object* v_fst_236_; lean_object* v_snd_237_; lean_object* v___x_238_; lean_object* v_fst_239_; lean_object* v_snd_240_; uint64_t v___x_241_; uint64_t v___x_242_; uint64_t v___x_243_; uint64_t v___x_244_; uint64_t v___x_245_; 
v_binderType_233_ = lean_ctor_get(v_e_95_, 1);
v_body_234_ = lean_ctor_get(v_e_95_, 2);
lean_inc_ref(v_binderType_233_);
lean_inc_ref(v_cx_94_);
v___x_235_ = l_StmtKeys_hx(v_cx_94_, v_binderType_233_, v_a_96_);
v_fst_236_ = lean_ctor_get(v___x_235_, 0);
lean_inc(v_fst_236_);
v_snd_237_ = lean_ctor_get(v___x_235_, 1);
lean_inc(v_snd_237_);
lean_dec_ref(v___x_235_);
lean_inc_ref(v_body_234_);
v___x_238_ = l_StmtKeys_hx(v_cx_94_, v_body_234_, v_snd_237_);
v_fst_239_ = lean_ctor_get(v___x_238_, 0);
lean_inc(v_fst_239_);
v_snd_240_ = lean_ctor_get(v___x_238_, 1);
lean_inc(v_snd_240_);
lean_dec_ref(v___x_238_);
v___x_241_ = 71ULL;
v___x_242_ = lean_unbox_uint64(v_fst_236_);
lean_dec(v_fst_236_);
v___x_243_ = lean_unbox_uint64(v_fst_239_);
lean_dec(v_fst_239_);
v___x_244_ = lean_uint64_mix_hash(v___x_242_, v___x_243_);
v___x_245_ = lean_uint64_mix_hash(v___x_241_, v___x_244_);
v_h_115_ = v___x_245_;
v___y_116_ = v_snd_240_;
goto v___jp_114_;
}
case 8:
{
lean_object* v_type_246_; lean_object* v_value_247_; lean_object* v_body_248_; lean_object* v___x_249_; lean_object* v_fst_250_; lean_object* v_snd_251_; lean_object* v___x_252_; lean_object* v_fst_253_; lean_object* v_snd_254_; lean_object* v___x_255_; lean_object* v_fst_256_; lean_object* v_snd_257_; uint64_t v___x_258_; uint64_t v___x_259_; uint64_t v___x_260_; uint64_t v___x_261_; uint64_t v___x_262_; uint64_t v___x_263_; uint64_t v___x_264_; 
v_type_246_ = lean_ctor_get(v_e_95_, 1);
v_value_247_ = lean_ctor_get(v_e_95_, 2);
v_body_248_ = lean_ctor_get(v_e_95_, 3);
lean_inc_ref(v_type_246_);
lean_inc_ref_n(v_cx_94_, 2);
v___x_249_ = l_StmtKeys_hx(v_cx_94_, v_type_246_, v_a_96_);
v_fst_250_ = lean_ctor_get(v___x_249_, 0);
lean_inc(v_fst_250_);
v_snd_251_ = lean_ctor_get(v___x_249_, 1);
lean_inc(v_snd_251_);
lean_dec_ref(v___x_249_);
lean_inc_ref(v_value_247_);
v___x_252_ = l_StmtKeys_hx(v_cx_94_, v_value_247_, v_snd_251_);
v_fst_253_ = lean_ctor_get(v___x_252_, 0);
lean_inc(v_fst_253_);
v_snd_254_ = lean_ctor_get(v___x_252_, 1);
lean_inc(v_snd_254_);
lean_dec_ref(v___x_252_);
lean_inc_ref(v_body_248_);
v___x_255_ = l_StmtKeys_hx(v_cx_94_, v_body_248_, v_snd_254_);
v_fst_256_ = lean_ctor_get(v___x_255_, 0);
lean_inc(v_fst_256_);
v_snd_257_ = lean_ctor_get(v___x_255_, 1);
lean_inc(v_snd_257_);
lean_dec_ref(v___x_255_);
v___x_258_ = 73ULL;
v___x_259_ = lean_unbox_uint64(v_fst_253_);
lean_dec(v_fst_253_);
v___x_260_ = lean_unbox_uint64(v_fst_256_);
lean_dec(v_fst_256_);
v___x_261_ = lean_uint64_mix_hash(v___x_259_, v___x_260_);
v___x_262_ = lean_unbox_uint64(v_fst_250_);
lean_dec(v_fst_250_);
v___x_263_ = lean_uint64_mix_hash(v___x_262_, v___x_261_);
v___x_264_ = lean_uint64_mix_hash(v___x_258_, v___x_263_);
v_h_115_ = v___x_264_;
v___y_116_ = v_snd_257_;
goto v___jp_114_;
}
case 11:
{
lean_object* v_typeName_265_; lean_object* v_idx_266_; lean_object* v_struct_267_; lean_object* v___x_268_; lean_object* v_fst_269_; lean_object* v_snd_270_; uint64_t v___x_271_; uint64_t v___y_273_; 
v_typeName_265_ = lean_ctor_get(v_e_95_, 0);
v_idx_266_ = lean_ctor_get(v_e_95_, 1);
v_struct_267_ = lean_ctor_get(v_e_95_, 2);
lean_inc_ref(v_struct_267_);
v___x_268_ = l_StmtKeys_hx(v_cx_94_, v_struct_267_, v_a_96_);
v_fst_269_ = lean_ctor_get(v___x_268_, 0);
lean_inc(v_fst_269_);
v_snd_270_ = lean_ctor_get(v___x_268_, 1);
lean_inc(v_snd_270_);
lean_dec_ref(v___x_268_);
v___x_271_ = 79ULL;
if (lean_obj_tag(v_typeName_265_) == 0)
{
uint64_t v___x_279_; 
v___x_279_ = 1723ULL;
v___y_273_ = v___x_279_;
goto v___jp_272_;
}
else
{
uint64_t v_hash_280_; 
v_hash_280_ = lean_ctor_get_uint64(v_typeName_265_, sizeof(void*)*2);
v___y_273_ = v_hash_280_;
goto v___jp_272_;
}
v___jp_272_:
{
uint64_t v___x_274_; uint64_t v___x_275_; uint64_t v___x_276_; uint64_t v___x_277_; uint64_t v___x_278_; 
v___x_274_ = lean_uint64_of_nat(v_idx_266_);
v___x_275_ = lean_unbox_uint64(v_fst_269_);
lean_dec(v_fst_269_);
v___x_276_ = lean_uint64_mix_hash(v___x_274_, v___x_275_);
v___x_277_ = lean_uint64_mix_hash(v___y_273_, v___x_276_);
v___x_278_ = lean_uint64_mix_hash(v___x_271_, v___x_277_);
v_h_115_ = v___x_278_;
v___y_116_ = v_snd_270_;
goto v___jp_114_;
}
}
default: 
{
uint64_t v___x_281_; 
lean_inc_ref(v_fv_175_);
lean_inc_ref(v_order_174_);
lean_inc_ref(v_ren_173_);
lean_inc_ref(v_memo_172_);
lean_dec_ref(v_a_96_);
lean_dec_ref(v_cx_94_);
v___x_281_ = 0ULL;
v_h_104_ = v___x_281_;
v_memo_105_ = v_memo_172_;
v_ren_106_ = v_ren_173_;
v_order_107_ = v_order_174_;
v_fv_108_ = v_fv_175_;
goto v___jp_103_;
}
}
}
}
}
v___jp_97_:
{
uint64_t v___x_100_; lean_object* v___x_101_; lean_object* v___x_102_; 
v___x_100_ = lean_uint64_mix_hash(v___y_98_, v___y_99_);
v___x_101_ = lean_box_uint64(v___x_100_);
v___x_102_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_102_, 0, v___x_101_);
lean_ctor_set(v___x_102_, 1, v_a_96_);
return v___x_102_;
}
v___jp_103_:
{
lean_object* v___x_109_; lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; lean_object* v___x_113_; 
v___x_109_ = lean_box_uint64(v_h_104_);
v___x_110_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Meta_ForEachExpr_0__Lean_Meta_forEachExpr_x27_visit___at___00Lean_Meta_forEachExpr_x27___at___00__private_Lean_Linter_Extra_UnusedDecidableInType_0__Lean_Linter_Extra_UnusedDecidableInType_collectFVarsOutsideOfProofs_spec__0_spec__0_spec__2___redArg(v_memo_105_, v_e_95_, v___x_109_);
v___x_111_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_111_, 0, v___x_110_);
lean_ctor_set(v___x_111_, 1, v_ren_106_);
lean_ctor_set(v___x_111_, 2, v_order_107_);
lean_ctor_set(v___x_111_, 3, v_fv_108_);
v___x_112_ = lean_box_uint64(v_h_104_);
v___x_113_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_113_, 0, v___x_112_);
lean_ctor_set(v___x_113_, 1, v___x_111_);
return v___x_113_;
}
v___jp_114_:
{
lean_object* v_memo_117_; lean_object* v_ren_118_; lean_object* v_order_119_; lean_object* v_fv_120_; 
v_memo_117_ = lean_ctor_get(v___y_116_, 0);
lean_inc_ref(v_memo_117_);
v_ren_118_ = lean_ctor_get(v___y_116_, 1);
lean_inc_ref(v_ren_118_);
v_order_119_ = lean_ctor_get(v___y_116_, 2);
lean_inc_ref(v_order_119_);
v_fv_120_ = lean_ctor_get(v___y_116_, 3);
lean_inc_ref(v_fv_120_);
lean_dec_ref(v___y_116_);
v_h_104_ = v_h_115_;
v_memo_105_ = v_memo_117_;
v_ren_106_ = v_ren_118_;
v_order_107_ = v_order_119_;
v_fv_108_ = v_fv_120_;
goto v___jp_103_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_hx_spec__0(lean_object* v_cx_282_, lean_object* v___x_283_, lean_object* v_as_284_, size_t v_sz_285_, size_t v_i_286_, uint64_t v_b_287_, lean_object* v___y_288_){
_start:
{
uint64_t v_ha_290_; lean_object* v___y_291_; uint64_t v___y_297_; uint64_t v___y_298_; uint8_t v___x_300_; 
v___x_300_ = lean_usize_dec_lt(v_i_286_, v_sz_285_);
if (v___x_300_ == 0)
{
lean_object* v___x_301_; lean_object* v___x_302_; 
lean_dec_ref(v_cx_282_);
v___x_301_ = lean_box_uint64(v_b_287_);
v___x_302_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_302_, 0, v___x_301_);
lean_ctor_set(v___x_302_, 1, v___y_288_);
return v___x_302_;
}
else
{
lean_object* v_a_303_; lean_object* v___x_304_; 
v_a_303_ = lean_array_uget_borrowed(v_as_284_, v_i_286_);
v___x_304_ = l_Lean_Expr_consumeMData(v_a_303_);
if (lean_obj_tag(v___x_304_) == 4)
{
lean_object* v_declName_305_; uint8_t v_leaves_315_; 
v_declName_305_ = lean_ctor_get(v___x_304_, 0);
lean_inc(v_declName_305_);
lean_dec_ref_known(v___x_304_, 2);
v_leaves_315_ = lean_ctor_get_uint8(v___x_283_, 1);
if (v_leaves_315_ == 0)
{
uint8_t v_proj_316_; 
v_proj_316_ = lean_ctor_get_uint8(v___x_283_, 2);
if (v_proj_316_ == 0)
{
goto v___jp_306_;
}
else
{
lean_object* v_isProj_317_; lean_object* v___x_318_; uint8_t v___x_319_; 
v_isProj_317_ = lean_ctor_get(v_cx_282_, 1);
lean_inc_ref(v_isProj_317_);
lean_inc(v_declName_305_);
v___x_318_ = lean_apply_1(v_isProj_317_, v_declName_305_);
v___x_319_ = lean_unbox(v___x_318_);
if (v___x_319_ == 0)
{
goto v___jp_306_;
}
else
{
goto v___jp_310_;
}
}
}
else
{
goto v___jp_310_;
}
v___jp_306_:
{
uint64_t v___x_307_; 
v___x_307_ = 47ULL;
if (lean_obj_tag(v_declName_305_) == 0)
{
uint64_t v___x_308_; 
v___x_308_ = 1723ULL;
v___y_297_ = v___x_307_;
v___y_298_ = v___x_308_;
goto v___jp_296_;
}
else
{
uint64_t v_hash_309_; 
v_hash_309_ = lean_ctor_get_uint64(v_declName_305_, sizeof(void*)*2);
lean_dec(v_declName_305_);
v___y_297_ = v___x_307_;
v___y_298_ = v_hash_309_;
goto v___jp_296_;
}
}
v___jp_310_:
{
lean_object* v___x_311_; lean_object* v_fst_312_; lean_object* v_snd_313_; uint64_t v___x_314_; 
lean_inc_ref(v_cx_282_);
v___x_311_ = l_StmtKeys_renameConst(v_cx_282_, v_declName_305_, v___y_288_);
v_fst_312_ = lean_ctor_get(v___x_311_, 0);
lean_inc(v_fst_312_);
v_snd_313_ = lean_ctor_get(v___x_311_, 1);
lean_inc(v_snd_313_);
lean_dec_ref(v___x_311_);
v___x_314_ = lean_unbox_uint64(v_fst_312_);
lean_dec(v_fst_312_);
v_ha_290_ = v___x_314_;
v___y_291_ = v_snd_313_;
goto v___jp_289_;
}
}
else
{
lean_object* v___x_320_; lean_object* v_fst_321_; lean_object* v_snd_322_; uint64_t v___x_323_; 
lean_inc_ref(v_cx_282_);
v___x_320_ = l_StmtKeys_hx(v_cx_282_, v___x_304_, v___y_288_);
v_fst_321_ = lean_ctor_get(v___x_320_, 0);
lean_inc(v_fst_321_);
v_snd_322_ = lean_ctor_get(v___x_320_, 1);
lean_inc(v_snd_322_);
lean_dec_ref(v___x_320_);
v___x_323_ = lean_unbox_uint64(v_fst_321_);
lean_dec(v_fst_321_);
v_ha_290_ = v___x_323_;
v___y_291_ = v_snd_322_;
goto v___jp_289_;
}
}
v___jp_289_:
{
uint64_t v___x_292_; size_t v___x_293_; size_t v___x_294_; 
v___x_292_ = lean_uint64_mix_hash(v_b_287_, v_ha_290_);
v___x_293_ = ((size_t)1ULL);
v___x_294_ = lean_usize_add(v_i_286_, v___x_293_);
v_i_286_ = v___x_294_;
v_b_287_ = v___x_292_;
v___y_288_ = v___y_291_;
goto _start;
}
v___jp_296_:
{
uint64_t v___x_299_; 
v___x_299_ = lean_uint64_mix_hash(v___y_297_, v___y_298_);
v_ha_290_ = v___x_299_;
v___y_291_ = v___y_288_;
goto v___jp_289_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_hx_spec__0___boxed(lean_object* v_cx_324_, lean_object* v___x_325_, lean_object* v_as_326_, lean_object* v_sz_327_, lean_object* v_i_328_, lean_object* v_b_329_, lean_object* v___y_330_){
_start:
{
size_t v_sz_boxed_331_; size_t v_i_boxed_332_; uint64_t v_b_boxed_333_; lean_object* v_res_334_; 
v_sz_boxed_331_ = lean_unbox_usize(v_sz_327_);
lean_dec(v_sz_327_);
v_i_boxed_332_ = lean_unbox_usize(v_i_328_);
lean_dec(v_i_328_);
v_b_boxed_333_ = lean_unbox_uint64(v_b_329_);
lean_dec_ref(v_b_329_);
v_res_334_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_hx_spec__0(v_cx_324_, v___x_325_, v_as_326_, v_sz_boxed_331_, v_i_boxed_332_, v_b_boxed_333_, v___y_330_);
lean_dec_ref(v_as_326_);
lean_dec_ref(v___x_325_);
return v_res_334_;
}
}
LEAN_EXPORT uint64_t l_StmtKeys_plainKey___lam__0(lean_object* v_x_335_){
_start:
{
uint64_t v___x_336_; 
v___x_336_ = 0ULL;
return v___x_336_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_plainKey___lam__0___boxed(lean_object* v_x_337_){
_start:
{
uint64_t v_res_338_; lean_object* v_r_339_; 
v_res_338_ = l_StmtKeys_plainKey___lam__0(v_x_337_);
lean_dec(v_x_337_);
v_r_339_ = lean_box_uint64(v_res_338_);
return v_r_339_;
}
}
static lean_object* _init_l_StmtKeys_plainKey___closed__1(void){
_start:
{
lean_object* v___x_341_; lean_object* v___x_342_; lean_object* v___x_343_; 
v___x_341_ = lean_box(0);
v___x_342_ = lean_unsigned_to_nat(16u);
v___x_343_ = lean_mk_array(v___x_342_, v___x_341_);
return v___x_343_;
}
}
static lean_object* _init_l_StmtKeys_plainKey___closed__2(void){
_start:
{
lean_object* v___x_344_; lean_object* v___x_345_; lean_object* v___x_346_; 
v___x_344_ = lean_obj_once(&l_StmtKeys_plainKey___closed__1, &l_StmtKeys_plainKey___closed__1_once, _init_l_StmtKeys_plainKey___closed__1);
v___x_345_ = lean_unsigned_to_nat(0u);
v___x_346_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_346_, 0, v___x_345_);
lean_ctor_set(v___x_346_, 1, v___x_344_);
return v___x_346_;
}
}
static lean_object* _init_l_StmtKeys_plainKey___closed__4(void){
_start:
{
lean_object* v___x_349_; lean_object* v___x_350_; lean_object* v___x_351_; 
v___x_349_ = ((lean_object*)(l_StmtKeys_plainKey___closed__3));
v___x_350_ = lean_obj_once(&l_StmtKeys_plainKey___closed__2, &l_StmtKeys_plainKey___closed__2_once, _init_l_StmtKeys_plainKey___closed__2);
v___x_351_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_351_, 0, v___x_350_);
lean_ctor_set(v___x_351_, 1, v___x_350_);
lean_ctor_set(v___x_351_, 2, v___x_349_);
lean_ctor_set(v___x_351_, 3, v___x_350_);
return v___x_351_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_plainKey(lean_object* v_o_352_, lean_object* v_isProj_353_, lean_object* v_e_354_){
_start:
{
lean_object* v___f_355_; uint8_t v___x_356_; lean_object* v___x_357_; lean_object* v___x_358_; lean_object* v___x_359_; lean_object* v_snd_360_; lean_object* v_fst_361_; lean_object* v___x_363_; uint8_t v_isShared_364_; uint8_t v_isSharedCheck_369_; 
v___f_355_ = ((lean_object*)(l_StmtKeys_plainKey___closed__0));
v___x_356_ = 1;
v___x_357_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_357_, 0, v_o_352_);
lean_ctor_set(v___x_357_, 1, v_isProj_353_);
lean_ctor_set(v___x_357_, 2, v___f_355_);
lean_ctor_set_uint8(v___x_357_, sizeof(void*)*3, v___x_356_);
v___x_358_ = lean_obj_once(&l_StmtKeys_plainKey___closed__4, &l_StmtKeys_plainKey___closed__4_once, _init_l_StmtKeys_plainKey___closed__4);
v___x_359_ = l_StmtKeys_hx(v___x_357_, v_e_354_, v___x_358_);
v_snd_360_ = lean_ctor_get(v___x_359_, 1);
v_fst_361_ = lean_ctor_get(v___x_359_, 0);
v_isSharedCheck_369_ = !lean_is_exclusive(v___x_359_);
if (v_isSharedCheck_369_ == 0)
{
v___x_363_ = v___x_359_;
v_isShared_364_ = v_isSharedCheck_369_;
goto v_resetjp_362_;
}
else
{
lean_inc(v_snd_360_);
lean_inc(v_fst_361_);
lean_dec(v___x_359_);
v___x_363_ = lean_box(0);
v_isShared_364_ = v_isSharedCheck_369_;
goto v_resetjp_362_;
}
v_resetjp_362_:
{
lean_object* v_order_365_; lean_object* v___x_367_; 
v_order_365_ = lean_ctor_get(v_snd_360_, 2);
lean_inc_ref(v_order_365_);
lean_dec(v_snd_360_);
if (v_isShared_364_ == 0)
{
lean_ctor_set(v___x_363_, 1, v_order_365_);
v___x_367_ = v___x_363_;
goto v_reusejp_366_;
}
else
{
lean_object* v_reuseFailAlloc_368_; 
v_reuseFailAlloc_368_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_368_, 0, v_fst_361_);
lean_ctor_set(v_reuseFailAlloc_368_, 1, v_order_365_);
v___x_367_ = v_reuseFailAlloc_368_;
goto v_reusejp_366_;
}
v_reusejp_366_:
{
return v___x_367_;
}
}
}
}
LEAN_EXPORT lean_object* l_StmtKeys_jointKey(lean_object* v_o_370_, lean_object* v_isProj_371_, lean_object* v_annot_372_, lean_object* v_ty_373_, lean_object* v_val_374_){
_start:
{
uint8_t v___x_375_; lean_object* v_cx_376_; lean_object* v___x_377_; lean_object* v___x_378_; lean_object* v_fst_379_; lean_object* v_snd_380_; lean_object* v___x_381_; lean_object* v_snd_382_; lean_object* v_fst_383_; lean_object* v___x_385_; uint8_t v_isShared_386_; uint8_t v_isSharedCheck_395_; 
v___x_375_ = 1;
v_cx_376_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v_cx_376_, 0, v_o_370_);
lean_ctor_set(v_cx_376_, 1, v_isProj_371_);
lean_ctor_set(v_cx_376_, 2, v_annot_372_);
lean_ctor_set_uint8(v_cx_376_, sizeof(void*)*3, v___x_375_);
v___x_377_ = lean_obj_once(&l_StmtKeys_plainKey___closed__4, &l_StmtKeys_plainKey___closed__4_once, _init_l_StmtKeys_plainKey___closed__4);
lean_inc_ref(v_cx_376_);
v___x_378_ = l_StmtKeys_hx(v_cx_376_, v_ty_373_, v___x_377_);
v_fst_379_ = lean_ctor_get(v___x_378_, 0);
lean_inc(v_fst_379_);
v_snd_380_ = lean_ctor_get(v___x_378_, 1);
lean_inc(v_snd_380_);
lean_dec_ref(v___x_378_);
v___x_381_ = l_StmtKeys_hx(v_cx_376_, v_val_374_, v_snd_380_);
v_snd_382_ = lean_ctor_get(v___x_381_, 1);
v_fst_383_ = lean_ctor_get(v___x_381_, 0);
v_isSharedCheck_395_ = !lean_is_exclusive(v___x_381_);
if (v_isSharedCheck_395_ == 0)
{
v___x_385_ = v___x_381_;
v_isShared_386_ = v_isSharedCheck_395_;
goto v_resetjp_384_;
}
else
{
lean_inc(v_snd_382_);
lean_inc(v_fst_383_);
lean_dec(v___x_381_);
v___x_385_ = lean_box(0);
v_isShared_386_ = v_isSharedCheck_395_;
goto v_resetjp_384_;
}
v_resetjp_384_:
{
lean_object* v_order_387_; uint64_t v___x_388_; uint64_t v___x_389_; uint64_t v___x_390_; lean_object* v___x_391_; lean_object* v___x_393_; 
v_order_387_ = lean_ctor_get(v_snd_382_, 2);
lean_inc_ref(v_order_387_);
lean_dec(v_snd_382_);
v___x_388_ = lean_unbox_uint64(v_fst_379_);
lean_dec(v_fst_379_);
v___x_389_ = lean_unbox_uint64(v_fst_383_);
lean_dec(v_fst_383_);
v___x_390_ = lean_uint64_mix_hash(v___x_388_, v___x_389_);
v___x_391_ = lean_box_uint64(v___x_390_);
if (v_isShared_386_ == 0)
{
lean_ctor_set(v___x_385_, 1, v_order_387_);
lean_ctor_set(v___x_385_, 0, v___x_391_);
v___x_393_ = v___x_385_;
goto v_reusejp_392_;
}
else
{
lean_object* v_reuseFailAlloc_394_; 
v_reuseFailAlloc_394_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_394_, 0, v___x_391_);
lean_ctor_set(v_reuseFailAlloc_394_, 1, v_order_387_);
v___x_393_ = v_reuseFailAlloc_394_;
goto v_reusejp_392_;
}
v_reusejp_392_:
{
return v___x_393_;
}
}
}
}
LEAN_EXPORT lean_object* l_StmtKeys_fvarOrder(lean_object* v_e_396_, lean_object* v_a_397_){
_start:
{
lean_object* v_t_399_; lean_object* v_b_400_; lean_object* v___y_401_; uint8_t v___x_405_; 
v___x_405_ = l_Lean_Expr_hasFVar(v_e_396_);
if (v___x_405_ == 0)
{
lean_object* v___x_406_; lean_object* v___x_407_; 
lean_dec_ref(v_e_396_);
v___x_406_ = lean_box(0);
v___x_407_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_407_, 0, v___x_406_);
lean_ctor_set(v___x_407_, 1, v_a_397_);
return v___x_407_;
}
else
{
if (lean_obj_tag(v_e_396_) == 1)
{
lean_object* v_fvarId_408_; lean_object* v_fst_409_; lean_object* v_snd_410_; uint8_t v___x_411_; 
v_fvarId_408_ = lean_ctor_get(v_e_396_, 0);
lean_inc(v_fvarId_408_);
lean_dec_ref_known(v_e_396_, 1);
v_fst_409_ = lean_ctor_get(v_a_397_, 0);
v_snd_410_ = lean_ctor_get(v_a_397_, 1);
v___x_411_ = l_Array_contains___at___00Lean_Meta_CheckAssignment_checkMVar_spec__14(v_snd_410_, v_fvarId_408_);
if (v___x_411_ == 0)
{
lean_object* v___x_413_; uint8_t v_isShared_414_; uint8_t v_isSharedCheck_421_; 
lean_inc(v_snd_410_);
lean_inc(v_fst_409_);
v_isSharedCheck_421_ = !lean_is_exclusive(v_a_397_);
if (v_isSharedCheck_421_ == 0)
{
lean_object* v_unused_422_; lean_object* v_unused_423_; 
v_unused_422_ = lean_ctor_get(v_a_397_, 1);
lean_dec(v_unused_422_);
v_unused_423_ = lean_ctor_get(v_a_397_, 0);
lean_dec(v_unused_423_);
v___x_413_ = v_a_397_;
v_isShared_414_ = v_isSharedCheck_421_;
goto v_resetjp_412_;
}
else
{
lean_dec(v_a_397_);
v___x_413_ = lean_box(0);
v_isShared_414_ = v_isSharedCheck_421_;
goto v_resetjp_412_;
}
v_resetjp_412_:
{
lean_object* v___x_415_; lean_object* v___x_417_; 
v___x_415_ = lean_array_push(v_snd_410_, v_fvarId_408_);
if (v_isShared_414_ == 0)
{
lean_ctor_set(v___x_413_, 1, v___x_415_);
v___x_417_ = v___x_413_;
goto v_reusejp_416_;
}
else
{
lean_object* v_reuseFailAlloc_420_; 
v_reuseFailAlloc_420_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_420_, 0, v_fst_409_);
lean_ctor_set(v_reuseFailAlloc_420_, 1, v___x_415_);
v___x_417_ = v_reuseFailAlloc_420_;
goto v_reusejp_416_;
}
v_reusejp_416_:
{
lean_object* v___x_418_; lean_object* v___x_419_; 
v___x_418_ = lean_box(0);
v___x_419_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_419_, 0, v___x_418_);
lean_ctor_set(v___x_419_, 1, v___x_417_);
return v___x_419_;
}
}
}
else
{
lean_object* v___x_424_; lean_object* v___x_425_; 
lean_dec(v_fvarId_408_);
v___x_424_ = lean_box(0);
v___x_425_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_425_, 0, v___x_424_);
lean_ctor_set(v___x_425_, 1, v_a_397_);
return v___x_425_;
}
}
else
{
lean_object* v_fst_426_; lean_object* v_snd_427_; uint8_t v___x_428_; 
v_fst_426_ = lean_ctor_get(v_a_397_, 0);
v_snd_427_ = lean_ctor_get(v_a_397_, 1);
v___x_428_ = l_Std_DHashMap_Internal_Raw_u2080_contains___at___00__private_Lean_Util_OccursCheck_0__Lean_occursCheck_visit___at___00Lean_occursCheck___at___00Lean_Meta_CheckAssignment_checkMVar_spec__21_spec__24_spec__28___redArg(v_fst_426_, v_e_396_);
if (v___x_428_ == 0)
{
lean_object* v___x_430_; uint8_t v_isShared_431_; uint8_t v_isSharedCheck_459_; 
lean_inc(v_snd_427_);
lean_inc(v_fst_426_);
v_isSharedCheck_459_ = !lean_is_exclusive(v_a_397_);
if (v_isSharedCheck_459_ == 0)
{
lean_object* v_unused_460_; lean_object* v_unused_461_; 
v_unused_460_ = lean_ctor_get(v_a_397_, 1);
lean_dec(v_unused_460_);
v_unused_461_ = lean_ctor_get(v_a_397_, 0);
lean_dec(v_unused_461_);
v___x_430_ = v_a_397_;
v_isShared_431_ = v_isSharedCheck_459_;
goto v_resetjp_429_;
}
else
{
lean_dec(v_a_397_);
v___x_430_ = lean_box(0);
v_isShared_431_ = v_isSharedCheck_459_;
goto v_resetjp_429_;
}
v_resetjp_429_:
{
lean_object* v___x_432_; lean_object* v___x_433_; lean_object* v___x_435_; 
v___x_432_ = lean_box(0);
lean_inc_ref(v_e_396_);
v___x_433_ = l_Std_DHashMap_Internal_Raw_u2080_insertIfNew___at___00__private_Lean_Util_OccursCheck_0__Lean_occursCheck_visit___at___00Lean_occursCheck___at___00Lean_Meta_CheckAssignment_checkMVar_spec__21_spec__24_spec__29___redArg(v_fst_426_, v_e_396_, v___x_432_);
if (v_isShared_431_ == 0)
{
lean_ctor_set(v___x_430_, 0, v___x_433_);
v___x_435_ = v___x_430_;
goto v_reusejp_434_;
}
else
{
lean_object* v_reuseFailAlloc_458_; 
v_reuseFailAlloc_458_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_458_, 0, v___x_433_);
lean_ctor_set(v_reuseFailAlloc_458_, 1, v_snd_427_);
v___x_435_ = v_reuseFailAlloc_458_;
goto v_reusejp_434_;
}
v_reusejp_434_:
{
switch(lean_obj_tag(v_e_396_))
{
case 5:
{
lean_object* v_fn_436_; lean_object* v_arg_437_; lean_object* v___x_438_; lean_object* v_snd_439_; 
v_fn_436_ = lean_ctor_get(v_e_396_, 0);
lean_inc_ref(v_fn_436_);
v_arg_437_ = lean_ctor_get(v_e_396_, 1);
lean_inc_ref(v_arg_437_);
lean_dec_ref_known(v_e_396_, 2);
v___x_438_ = l_StmtKeys_fvarOrder(v_fn_436_, v___x_435_);
v_snd_439_ = lean_ctor_get(v___x_438_, 1);
lean_inc(v_snd_439_);
lean_dec_ref(v___x_438_);
v_e_396_ = v_arg_437_;
v_a_397_ = v_snd_439_;
goto _start;
}
case 6:
{
lean_object* v_binderType_441_; lean_object* v_body_442_; 
v_binderType_441_ = lean_ctor_get(v_e_396_, 1);
lean_inc_ref(v_binderType_441_);
v_body_442_ = lean_ctor_get(v_e_396_, 2);
lean_inc_ref(v_body_442_);
lean_dec_ref_known(v_e_396_, 3);
v_t_399_ = v_binderType_441_;
v_b_400_ = v_body_442_;
v___y_401_ = v___x_435_;
goto v___jp_398_;
}
case 7:
{
lean_object* v_binderType_443_; lean_object* v_body_444_; 
v_binderType_443_ = lean_ctor_get(v_e_396_, 1);
lean_inc_ref(v_binderType_443_);
v_body_444_ = lean_ctor_get(v_e_396_, 2);
lean_inc_ref(v_body_444_);
lean_dec_ref_known(v_e_396_, 3);
v_t_399_ = v_binderType_443_;
v_b_400_ = v_body_444_;
v___y_401_ = v___x_435_;
goto v___jp_398_;
}
case 8:
{
lean_object* v_type_445_; lean_object* v_value_446_; lean_object* v_body_447_; lean_object* v___x_448_; lean_object* v_snd_449_; lean_object* v___x_450_; lean_object* v_snd_451_; 
v_type_445_ = lean_ctor_get(v_e_396_, 1);
lean_inc_ref(v_type_445_);
v_value_446_ = lean_ctor_get(v_e_396_, 2);
lean_inc_ref(v_value_446_);
v_body_447_ = lean_ctor_get(v_e_396_, 3);
lean_inc_ref(v_body_447_);
lean_dec_ref_known(v_e_396_, 4);
v___x_448_ = l_StmtKeys_fvarOrder(v_type_445_, v___x_435_);
v_snd_449_ = lean_ctor_get(v___x_448_, 1);
lean_inc(v_snd_449_);
lean_dec_ref(v___x_448_);
v___x_450_ = l_StmtKeys_fvarOrder(v_value_446_, v_snd_449_);
v_snd_451_ = lean_ctor_get(v___x_450_, 1);
lean_inc(v_snd_451_);
lean_dec_ref(v___x_450_);
v_e_396_ = v_body_447_;
v_a_397_ = v_snd_451_;
goto _start;
}
case 10:
{
lean_object* v_expr_453_; 
v_expr_453_ = lean_ctor_get(v_e_396_, 1);
lean_inc_ref(v_expr_453_);
lean_dec_ref_known(v_e_396_, 2);
v_e_396_ = v_expr_453_;
v_a_397_ = v___x_435_;
goto _start;
}
case 11:
{
lean_object* v_struct_455_; 
v_struct_455_ = lean_ctor_get(v_e_396_, 2);
lean_inc_ref(v_struct_455_);
lean_dec_ref_known(v_e_396_, 3);
v_e_396_ = v_struct_455_;
v_a_397_ = v___x_435_;
goto _start;
}
default: 
{
lean_object* v___x_457_; 
lean_dec_ref(v_e_396_);
v___x_457_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_457_, 0, v___x_432_);
lean_ctor_set(v___x_457_, 1, v___x_435_);
return v___x_457_;
}
}
}
}
}
else
{
lean_object* v___x_462_; lean_object* v___x_463_; 
lean_dec_ref(v_e_396_);
v___x_462_ = lean_box(0);
v___x_463_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_463_, 0, v___x_462_);
lean_ctor_set(v___x_463_, 1, v_a_397_);
return v___x_463_;
}
}
}
v___jp_398_:
{
lean_object* v___x_402_; lean_object* v_snd_403_; 
v___x_402_ = l_StmtKeys_fvarOrder(v_t_399_, v___y_401_);
v_snd_403_ = lean_ctor_get(v___x_402_, 1);
lean_inc(v_snd_403_);
lean_dec_ref(v___x_402_);
v_e_396_ = v_b_400_;
v_a_397_ = v_snd_403_;
goto _start;
}
}
}
static lean_object* _init_l_StmtKeys_fvarsOf___closed__0(void){
_start:
{
lean_object* v___x_464_; lean_object* v___x_465_; lean_object* v___x_466_; 
v___x_464_ = ((lean_object*)(l_StmtKeys_plainKey___closed__3));
v___x_465_ = lean_obj_once(&l_StmtKeys_plainKey___closed__2, &l_StmtKeys_plainKey___closed__2_once, _init_l_StmtKeys_plainKey___closed__2);
v___x_466_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_466_, 0, v___x_465_);
lean_ctor_set(v___x_466_, 1, v___x_464_);
return v___x_466_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_fvarsOf(lean_object* v_e_467_){
_start:
{
lean_object* v___x_468_; lean_object* v___x_469_; lean_object* v_snd_470_; lean_object* v_snd_471_; 
v___x_468_ = lean_obj_once(&l_StmtKeys_fvarsOf___closed__0, &l_StmtKeys_fvarsOf___closed__0_once, _init_l_StmtKeys_fvarsOf___closed__0);
v___x_469_ = l_StmtKeys_fvarOrder(v_e_467_, v___x_468_);
v_snd_470_ = lean_ctor_get(v___x_469_, 1);
lean_inc(v_snd_470_);
lean_dec_ref(v___x_469_);
v_snd_471_ = lean_ctor_get(v_snd_470_, 1);
lean_inc(v_snd_471_);
lean_dec(v_snd_470_);
return v_snd_471_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg(lean_object* v_ord_475_, lean_object* v_range_476_, lean_object* v_b_477_, lean_object* v_i_478_){
_start:
{
lean_object* v_stop_479_; lean_object* v_step_480_; uint8_t v___x_481_; 
v_stop_479_ = lean_ctor_get(v_range_476_, 1);
v_step_480_ = lean_ctor_get(v_range_476_, 2);
v___x_481_ = lean_nat_dec_lt(v_i_478_, v_stop_479_);
if (v___x_481_ == 0)
{
lean_dec(v_i_478_);
return v_b_477_;
}
else
{
lean_object* v___x_482_; lean_object* v___x_483_; lean_object* v___x_484_; lean_object* v___x_485_; lean_object* v___x_486_; lean_object* v___x_487_; 
v___x_482_ = lean_unsigned_to_nat(0u);
v___x_483_ = ((lean_object*)(l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__1));
v___x_484_ = lean_array_get_borrowed(v___x_482_, v_ord_475_, v_i_478_);
lean_inc(v___x_484_);
v___x_485_ = l_Lean_Name_num___override(v___x_483_, v___x_484_);
lean_inc(v_i_478_);
v___x_486_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00Lean_Elab_Command_elabOmit_spec__3___redArg(v_b_477_, v___x_485_, v_i_478_);
v___x_487_ = lean_nat_add(v_i_478_, v_step_480_);
lean_dec(v_i_478_);
v_b_477_ = v___x_486_;
v_i_478_ = v___x_487_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___boxed(lean_object* v_ord_489_, lean_object* v_range_490_, lean_object* v_b_491_, lean_object* v_i_492_){
_start:
{
lean_object* v_res_493_; 
v_res_493_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg(v_ord_489_, v_range_490_, v_b_491_, v_i_492_);
lean_dec_ref(v_range_490_);
lean_dec_ref(v_ord_489_);
return v_res_493_;
}
}
static lean_object* _init_l_StmtKeys_permKey___lam__1___closed__0(void){
_start:
{
lean_object* v___x_494_; lean_object* v___x_495_; lean_object* v___x_496_; 
v___x_494_ = lean_box(0);
v___x_495_ = lean_unsigned_to_nat(16u);
v___x_496_ = lean_mk_array(v___x_495_, v___x_494_);
return v___x_496_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_permKey___lam__1(lean_object* v___x_497_, lean_object* v___x_498_, lean_object* v_ord_499_){
_start:
{
lean_object* v___x_500_; lean_object* v___x_501_; lean_object* v___x_502_; lean_object* v___x_503_; lean_object* v___x_504_; 
v___x_500_ = lean_obj_once(&l_StmtKeys_permKey___lam__1___closed__0, &l_StmtKeys_permKey___lam__1___closed__0_once, _init_l_StmtKeys_permKey___lam__1___closed__0);
lean_inc_n(v___x_497_, 2);
v___x_501_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_501_, 0, v___x_497_);
lean_ctor_set(v___x_501_, 1, v___x_500_);
v___x_502_ = lean_array_get_size(v_ord_499_);
v___x_503_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_503_, 0, v___x_497_);
lean_ctor_set(v___x_503_, 1, v___x_502_);
lean_ctor_set(v___x_503_, 2, v___x_498_);
v___x_504_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg(v_ord_499_, v___x_503_, v___x_501_, v___x_497_);
lean_dec_ref_known(v___x_503_, 3);
return v___x_504_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_permKey___lam__1___boxed(lean_object* v___x_505_, lean_object* v___x_506_, lean_object* v_ord_507_){
_start:
{
lean_object* v_res_508_; 
v_res_508_ = l_StmtKeys_permKey___lam__1(v___x_505_, v___x_506_, v_ord_507_);
lean_dec_ref(v_ord_507_);
return v_res_508_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2_spec__2(lean_object* v_as_509_, size_t v_sz_510_, size_t v_i_511_, lean_object* v_b_512_){
_start:
{
lean_object* v_a_514_; uint8_t v___x_518_; 
v___x_518_ = lean_usize_dec_lt(v_i_511_, v_sz_510_);
if (v___x_518_ == 0)
{
return v_b_512_;
}
else
{
lean_object* v_fst_519_; lean_object* v_snd_520_; lean_object* v___x_522_; uint8_t v_isShared_523_; uint8_t v_isSharedCheck_542_; 
v_fst_519_ = lean_ctor_get(v_b_512_, 0);
v_snd_520_ = lean_ctor_get(v_b_512_, 1);
v_isSharedCheck_542_ = !lean_is_exclusive(v_b_512_);
if (v_isSharedCheck_542_ == 0)
{
v___x_522_ = v_b_512_;
v_isShared_523_ = v_isSharedCheck_542_;
goto v_resetjp_521_;
}
else
{
lean_inc(v_snd_520_);
lean_inc(v_fst_519_);
lean_dec(v_b_512_);
v___x_522_ = lean_box(0);
v_isShared_523_ = v_isSharedCheck_542_;
goto v_resetjp_521_;
}
v_resetjp_521_:
{
uint8_t v___x_524_; lean_object* v___y_526_; lean_object* v_a_539_; 
v___x_524_ = 0;
v_a_539_ = lean_array_uget_borrowed(v_as_509_, v_i_511_);
if (lean_obj_tag(v_a_539_) == 2)
{
lean_object* v_i_540_; 
v_i_540_ = lean_ctor_get(v_a_539_, 1);
lean_inc(v_i_540_);
v___y_526_ = v_i_540_;
goto v___jp_525_;
}
else
{
lean_object* v_i_541_; 
v_i_541_ = lean_unsigned_to_nat(0u);
v___y_526_ = v_i_541_;
goto v___jp_525_;
}
v___jp_525_:
{
lean_object* v___x_527_; lean_object* v___x_528_; uint8_t v___x_529_; 
v___x_527_ = lean_box(v___x_524_);
v___x_528_ = lean_array_get(v___x_527_, v_snd_520_, v___y_526_);
lean_dec(v___x_527_);
v___x_529_ = lean_unbox(v___x_528_);
lean_dec(v___x_528_);
if (v___x_529_ == 0)
{
lean_object* v___x_530_; lean_object* v___x_531_; lean_object* v___x_532_; lean_object* v___x_534_; 
v___x_530_ = lean_box(v___x_518_);
v___x_531_ = lean_array_set(v_snd_520_, v___y_526_, v___x_530_);
v___x_532_ = lean_array_push(v_fst_519_, v___y_526_);
if (v_isShared_523_ == 0)
{
lean_ctor_set(v___x_522_, 1, v___x_531_);
lean_ctor_set(v___x_522_, 0, v___x_532_);
v___x_534_ = v___x_522_;
goto v_reusejp_533_;
}
else
{
lean_object* v_reuseFailAlloc_535_; 
v_reuseFailAlloc_535_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_535_, 0, v___x_532_);
lean_ctor_set(v_reuseFailAlloc_535_, 1, v___x_531_);
v___x_534_ = v_reuseFailAlloc_535_;
goto v_reusejp_533_;
}
v_reusejp_533_:
{
v_a_514_ = v___x_534_;
goto v___jp_513_;
}
}
else
{
lean_object* v___x_537_; 
lean_dec(v___y_526_);
if (v_isShared_523_ == 0)
{
v___x_537_ = v___x_522_;
goto v_reusejp_536_;
}
else
{
lean_object* v_reuseFailAlloc_538_; 
v_reuseFailAlloc_538_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_538_, 0, v_fst_519_);
lean_ctor_set(v_reuseFailAlloc_538_, 1, v_snd_520_);
v___x_537_ = v_reuseFailAlloc_538_;
goto v_reusejp_536_;
}
v_reusejp_536_:
{
v_a_514_ = v___x_537_;
goto v___jp_513_;
}
}
}
}
}
v___jp_513_:
{
size_t v___x_515_; size_t v___x_516_; 
v___x_515_ = ((size_t)1ULL);
v___x_516_ = lean_usize_add(v_i_511_, v___x_515_);
v_i_511_ = v___x_516_;
v_b_512_ = v_a_514_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2_spec__2___boxed(lean_object* v_as_543_, lean_object* v_sz_544_, lean_object* v_i_545_, lean_object* v_b_546_){
_start:
{
size_t v_sz_boxed_547_; size_t v_i_boxed_548_; lean_object* v_res_549_; 
v_sz_boxed_547_ = lean_unbox_usize(v_sz_544_);
lean_dec(v_sz_544_);
v_i_boxed_548_ = lean_unbox_usize(v_i_545_);
lean_dec(v_i_545_);
v_res_549_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2_spec__2(v_as_543_, v_sz_boxed_547_, v_i_boxed_548_, v_b_546_);
lean_dec_ref(v_as_543_);
return v_res_549_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2(lean_object* v_as_550_, size_t v_sz_551_, size_t v_i_552_, lean_object* v_b_553_){
_start:
{
lean_object* v_a_555_; uint8_t v___x_559_; 
v___x_559_ = lean_usize_dec_lt(v_i_552_, v_sz_551_);
if (v___x_559_ == 0)
{
return v_b_553_;
}
else
{
lean_object* v_fst_560_; lean_object* v_snd_561_; lean_object* v___x_563_; uint8_t v_isShared_564_; uint8_t v_isSharedCheck_583_; 
v_fst_560_ = lean_ctor_get(v_b_553_, 0);
v_snd_561_ = lean_ctor_get(v_b_553_, 1);
v_isSharedCheck_583_ = !lean_is_exclusive(v_b_553_);
if (v_isSharedCheck_583_ == 0)
{
v___x_563_ = v_b_553_;
v_isShared_564_ = v_isSharedCheck_583_;
goto v_resetjp_562_;
}
else
{
lean_inc(v_snd_561_);
lean_inc(v_fst_560_);
lean_dec(v_b_553_);
v___x_563_ = lean_box(0);
v_isShared_564_ = v_isSharedCheck_583_;
goto v_resetjp_562_;
}
v_resetjp_562_:
{
uint8_t v___x_565_; lean_object* v___y_567_; lean_object* v_a_580_; 
v___x_565_ = 0;
v_a_580_ = lean_array_uget_borrowed(v_as_550_, v_i_552_);
if (lean_obj_tag(v_a_580_) == 2)
{
lean_object* v_i_581_; 
v_i_581_ = lean_ctor_get(v_a_580_, 1);
lean_inc(v_i_581_);
v___y_567_ = v_i_581_;
goto v___jp_566_;
}
else
{
lean_object* v_i_582_; 
v_i_582_ = lean_unsigned_to_nat(0u);
v___y_567_ = v_i_582_;
goto v___jp_566_;
}
v___jp_566_:
{
lean_object* v___x_568_; lean_object* v___x_569_; uint8_t v___x_570_; 
v___x_568_ = lean_box(v___x_565_);
v___x_569_ = lean_array_get(v___x_568_, v_snd_561_, v___y_567_);
lean_dec(v___x_568_);
v___x_570_ = lean_unbox(v___x_569_);
lean_dec(v___x_569_);
if (v___x_570_ == 0)
{
lean_object* v___x_571_; lean_object* v___x_572_; lean_object* v___x_573_; lean_object* v___x_575_; 
v___x_571_ = lean_box(v___x_559_);
v___x_572_ = lean_array_set(v_snd_561_, v___y_567_, v___x_571_);
v___x_573_ = lean_array_push(v_fst_560_, v___y_567_);
if (v_isShared_564_ == 0)
{
lean_ctor_set(v___x_563_, 1, v___x_572_);
lean_ctor_set(v___x_563_, 0, v___x_573_);
v___x_575_ = v___x_563_;
goto v_reusejp_574_;
}
else
{
lean_object* v_reuseFailAlloc_576_; 
v_reuseFailAlloc_576_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_576_, 0, v___x_573_);
lean_ctor_set(v_reuseFailAlloc_576_, 1, v___x_572_);
v___x_575_ = v_reuseFailAlloc_576_;
goto v_reusejp_574_;
}
v_reusejp_574_:
{
v_a_555_ = v___x_575_;
goto v___jp_554_;
}
}
else
{
lean_object* v___x_578_; 
lean_dec(v___y_567_);
if (v_isShared_564_ == 0)
{
v___x_578_ = v___x_563_;
goto v_reusejp_577_;
}
else
{
lean_object* v_reuseFailAlloc_579_; 
v_reuseFailAlloc_579_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_579_, 0, v_fst_560_);
lean_ctor_set(v_reuseFailAlloc_579_, 1, v_snd_561_);
v___x_578_ = v_reuseFailAlloc_579_;
goto v_reusejp_577_;
}
v_reusejp_577_:
{
v_a_555_ = v___x_578_;
goto v___jp_554_;
}
}
}
}
}
v___jp_554_:
{
size_t v___x_556_; size_t v___x_557_; lean_object* v___x_558_; 
v___x_556_ = ((size_t)1ULL);
v___x_557_ = lean_usize_add(v_i_552_, v___x_556_);
v___x_558_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2_spec__2(v_as_550_, v_sz_551_, v___x_557_, v_a_555_);
return v___x_558_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2___boxed(lean_object* v_as_584_, lean_object* v_sz_585_, lean_object* v_i_586_, lean_object* v_b_587_){
_start:
{
size_t v_sz_boxed_588_; size_t v_i_boxed_589_; lean_object* v_res_590_; 
v_sz_boxed_588_ = lean_unbox_usize(v_sz_585_);
lean_dec(v_sz_585_);
v_i_boxed_589_ = lean_unbox_usize(v_i_586_);
lean_dec(v_i_586_);
v_res_590_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2(v_as_584_, v_sz_boxed_588_, v_i_boxed_589_, v_b_587_);
lean_dec_ref(v_as_584_);
return v_res_590_;
}
}
static lean_object* _init_l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0(void){
_start:
{
lean_object* v___x_591_; 
v___x_591_ = l_Array_instInhabited(lean_box(0));
return v___x_591_;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg(lean_object* v___x_592_, lean_object* v_a_593_){
_start:
{
lean_object* v_snd_594_; lean_object* v_fst_595_; lean_object* v___x_597_; uint8_t v_isShared_598_; uint8_t v_isSharedCheck_638_; 
v_snd_594_ = lean_ctor_get(v_a_593_, 1);
v_fst_595_ = lean_ctor_get(v_a_593_, 0);
v_isSharedCheck_638_ = !lean_is_exclusive(v_a_593_);
if (v_isSharedCheck_638_ == 0)
{
v___x_597_ = v_a_593_;
v_isShared_598_ = v_isSharedCheck_638_;
goto v_resetjp_596_;
}
else
{
lean_inc(v_snd_594_);
lean_inc(v_fst_595_);
lean_dec(v_a_593_);
v___x_597_ = lean_box(0);
v_isShared_598_ = v_isSharedCheck_638_;
goto v_resetjp_596_;
}
v_resetjp_596_:
{
lean_object* v_fst_599_; lean_object* v_snd_600_; lean_object* v___x_602_; uint8_t v_isShared_603_; uint8_t v_isSharedCheck_637_; 
v_fst_599_ = lean_ctor_get(v_snd_594_, 0);
v_snd_600_ = lean_ctor_get(v_snd_594_, 1);
v_isSharedCheck_637_ = !lean_is_exclusive(v_snd_594_);
if (v_isSharedCheck_637_ == 0)
{
v___x_602_ = v_snd_594_;
v_isShared_603_ = v_isSharedCheck_637_;
goto v_resetjp_601_;
}
else
{
lean_inc(v_snd_600_);
lean_inc(v_fst_599_);
lean_dec(v_snd_594_);
v___x_602_ = lean_box(0);
v_isShared_603_ = v_isSharedCheck_637_;
goto v_resetjp_601_;
}
v_resetjp_601_:
{
lean_object* v___x_604_; uint8_t v___x_605_; 
v___x_604_ = lean_array_get_size(v_fst_595_);
v___x_605_ = lean_nat_dec_lt(v_snd_600_, v___x_604_);
if (v___x_605_ == 0)
{
lean_object* v___x_607_; 
if (v_isShared_603_ == 0)
{
v___x_607_ = v___x_602_;
goto v_reusejp_606_;
}
else
{
lean_object* v_reuseFailAlloc_611_; 
v_reuseFailAlloc_611_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_611_, 0, v_fst_599_);
lean_ctor_set(v_reuseFailAlloc_611_, 1, v_snd_600_);
v___x_607_ = v_reuseFailAlloc_611_;
goto v_reusejp_606_;
}
v_reusejp_606_:
{
lean_object* v___x_609_; 
if (v_isShared_598_ == 0)
{
lean_ctor_set(v___x_597_, 1, v___x_607_);
v___x_609_ = v___x_597_;
goto v_reusejp_608_;
}
else
{
lean_object* v_reuseFailAlloc_610_; 
v_reuseFailAlloc_610_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_610_, 0, v_fst_595_);
lean_ctor_set(v_reuseFailAlloc_610_, 1, v___x_607_);
v___x_609_ = v_reuseFailAlloc_610_;
goto v_reusejp_608_;
}
v_reusejp_608_:
{
return v___x_609_;
}
}
}
else
{
lean_object* v___x_612_; lean_object* v___x_613_; lean_object* v___x_614_; lean_object* v___x_615_; lean_object* v___x_617_; 
v___x_612_ = lean_unsigned_to_nat(0u);
v___x_613_ = lean_obj_once(&l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0, &l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0_once, _init_l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0);
v___x_614_ = lean_array_get_borrowed(v___x_612_, v_fst_595_, v_snd_600_);
v___x_615_ = lean_array_get_borrowed(v___x_613_, v___x_592_, v___x_614_);
if (v_isShared_603_ == 0)
{
lean_ctor_set(v___x_602_, 1, v_fst_599_);
lean_ctor_set(v___x_602_, 0, v_fst_595_);
v___x_617_ = v___x_602_;
goto v_reusejp_616_;
}
else
{
lean_object* v_reuseFailAlloc_636_; 
v_reuseFailAlloc_636_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_636_, 0, v_fst_595_);
lean_ctor_set(v_reuseFailAlloc_636_, 1, v_fst_599_);
v___x_617_ = v_reuseFailAlloc_636_;
goto v_reusejp_616_;
}
v_reusejp_616_:
{
size_t v_sz_618_; size_t v___x_619_; lean_object* v___x_620_; lean_object* v_fst_621_; lean_object* v_snd_622_; lean_object* v___x_624_; uint8_t v_isShared_625_; uint8_t v_isSharedCheck_635_; 
v_sz_618_ = lean_array_size(v___x_615_);
v___x_619_ = ((size_t)0ULL);
v___x_620_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2(v___x_615_, v_sz_618_, v___x_619_, v___x_617_);
v_fst_621_ = lean_ctor_get(v___x_620_, 0);
v_snd_622_ = lean_ctor_get(v___x_620_, 1);
v_isSharedCheck_635_ = !lean_is_exclusive(v___x_620_);
if (v_isSharedCheck_635_ == 0)
{
v___x_624_ = v___x_620_;
v_isShared_625_ = v_isSharedCheck_635_;
goto v_resetjp_623_;
}
else
{
lean_inc(v_snd_622_);
lean_inc(v_fst_621_);
lean_dec(v___x_620_);
v___x_624_ = lean_box(0);
v_isShared_625_ = v_isSharedCheck_635_;
goto v_resetjp_623_;
}
v_resetjp_623_:
{
lean_object* v___x_626_; lean_object* v___x_627_; lean_object* v___x_629_; 
v___x_626_ = lean_unsigned_to_nat(1u);
v___x_627_ = lean_nat_add(v_snd_600_, v___x_626_);
lean_dec(v_snd_600_);
if (v_isShared_625_ == 0)
{
lean_ctor_set(v___x_624_, 1, v___x_627_);
lean_ctor_set(v___x_624_, 0, v_snd_622_);
v___x_629_ = v___x_624_;
goto v_reusejp_628_;
}
else
{
lean_object* v_reuseFailAlloc_634_; 
v_reuseFailAlloc_634_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_634_, 0, v_snd_622_);
lean_ctor_set(v_reuseFailAlloc_634_, 1, v___x_627_);
v___x_629_ = v_reuseFailAlloc_634_;
goto v_reusejp_628_;
}
v_reusejp_628_:
{
lean_object* v___x_631_; 
if (v_isShared_598_ == 0)
{
lean_ctor_set(v___x_597_, 1, v___x_629_);
lean_ctor_set(v___x_597_, 0, v_fst_621_);
v___x_631_ = v___x_597_;
goto v_reusejp_630_;
}
else
{
lean_object* v_reuseFailAlloc_633_; 
v_reuseFailAlloc_633_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_633_, 0, v_fst_621_);
lean_ctor_set(v_reuseFailAlloc_633_, 1, v___x_629_);
v___x_631_ = v_reuseFailAlloc_633_;
goto v_reusejp_630_;
}
v_reusejp_630_:
{
v_a_593_ = v___x_631_;
goto _start;
}
}
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___boxed(lean_object* v___x_639_, lean_object* v_a_640_){
_start:
{
lean_object* v_res_641_; 
v_res_641_ = l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg(v___x_639_, v_a_640_);
lean_dec_ref(v___x_639_);
return v_res_641_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__7(lean_object* v_as_642_, size_t v_sz_643_, size_t v_i_644_, lean_object* v_b_645_){
_start:
{
lean_object* v_a_647_; uint8_t v___x_651_; 
v___x_651_ = lean_usize_dec_lt(v_i_644_, v_sz_643_);
if (v___x_651_ == 0)
{
return v_b_645_;
}
else
{
lean_object* v_fst_652_; lean_object* v_snd_653_; lean_object* v___x_655_; uint8_t v_isShared_656_; uint8_t v_isSharedCheck_675_; 
v_fst_652_ = lean_ctor_get(v_b_645_, 0);
v_snd_653_ = lean_ctor_get(v_b_645_, 1);
v_isSharedCheck_675_ = !lean_is_exclusive(v_b_645_);
if (v_isSharedCheck_675_ == 0)
{
v___x_655_ = v_b_645_;
v_isShared_656_ = v_isSharedCheck_675_;
goto v_resetjp_654_;
}
else
{
lean_inc(v_snd_653_);
lean_inc(v_fst_652_);
lean_dec(v_b_645_);
v___x_655_ = lean_box(0);
v_isShared_656_ = v_isSharedCheck_675_;
goto v_resetjp_654_;
}
v_resetjp_654_:
{
uint8_t v___x_657_; lean_object* v___y_659_; lean_object* v_a_672_; 
v___x_657_ = 0;
v_a_672_ = lean_array_uget_borrowed(v_as_642_, v_i_644_);
if (lean_obj_tag(v_a_672_) == 2)
{
lean_object* v_i_673_; 
v_i_673_ = lean_ctor_get(v_a_672_, 1);
lean_inc(v_i_673_);
v___y_659_ = v_i_673_;
goto v___jp_658_;
}
else
{
lean_object* v_i_674_; 
v_i_674_ = lean_unsigned_to_nat(0u);
v___y_659_ = v_i_674_;
goto v___jp_658_;
}
v___jp_658_:
{
lean_object* v___x_660_; lean_object* v___x_661_; uint8_t v___x_662_; 
v___x_660_ = lean_box(v___x_657_);
v___x_661_ = lean_array_get(v___x_660_, v_snd_653_, v___y_659_);
lean_dec(v___x_660_);
v___x_662_ = lean_unbox(v___x_661_);
lean_dec(v___x_661_);
if (v___x_662_ == 0)
{
lean_object* v___x_663_; lean_object* v___x_664_; lean_object* v___x_665_; lean_object* v___x_667_; 
v___x_663_ = lean_box(v___x_651_);
v___x_664_ = lean_array_set(v_snd_653_, v___y_659_, v___x_663_);
v___x_665_ = lean_array_push(v_fst_652_, v___y_659_);
if (v_isShared_656_ == 0)
{
lean_ctor_set(v___x_655_, 1, v___x_664_);
lean_ctor_set(v___x_655_, 0, v___x_665_);
v___x_667_ = v___x_655_;
goto v_reusejp_666_;
}
else
{
lean_object* v_reuseFailAlloc_668_; 
v_reuseFailAlloc_668_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_668_, 0, v___x_665_);
lean_ctor_set(v_reuseFailAlloc_668_, 1, v___x_664_);
v___x_667_ = v_reuseFailAlloc_668_;
goto v_reusejp_666_;
}
v_reusejp_666_:
{
v_a_647_ = v___x_667_;
goto v___jp_646_;
}
}
else
{
lean_object* v___x_670_; 
lean_dec(v___y_659_);
if (v_isShared_656_ == 0)
{
v___x_670_ = v___x_655_;
goto v_reusejp_669_;
}
else
{
lean_object* v_reuseFailAlloc_671_; 
v_reuseFailAlloc_671_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_671_, 0, v_fst_652_);
lean_ctor_set(v_reuseFailAlloc_671_, 1, v_snd_653_);
v___x_670_ = v_reuseFailAlloc_671_;
goto v_reusejp_669_;
}
v_reusejp_669_:
{
v_a_647_ = v___x_670_;
goto v___jp_646_;
}
}
}
}
}
v___jp_646_:
{
size_t v___x_648_; size_t v___x_649_; lean_object* v___x_650_; 
v___x_648_ = ((size_t)1ULL);
v___x_649_ = lean_usize_add(v_i_644_, v___x_648_);
v___x_650_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2_spec__2(v_as_642_, v_sz_643_, v___x_649_, v_a_647_);
return v___x_650_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__7___boxed(lean_object* v_as_676_, lean_object* v_sz_677_, lean_object* v_i_678_, lean_object* v_b_679_){
_start:
{
size_t v_sz_boxed_680_; size_t v_i_boxed_681_; lean_object* v_res_682_; 
v_sz_boxed_680_ = lean_unbox_usize(v_sz_677_);
lean_dec(v_sz_677_);
v_i_boxed_681_ = lean_unbox_usize(v_i_678_);
lean_dec(v_i_678_);
v_res_682_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__7(v_as_676_, v_sz_boxed_680_, v_i_boxed_681_, v_b_679_);
lean_dec_ref(v_as_676_);
return v_res_682_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__11(lean_object* v___x_683_, lean_object* v___x_684_, lean_object* v_as_685_, size_t v_sz_686_, size_t v_i_687_, lean_object* v_b_688_){
_start:
{
uint8_t v___x_689_; 
v___x_689_ = lean_usize_dec_lt(v_i_687_, v_sz_686_);
if (v___x_689_ == 0)
{
lean_dec_ref(v___x_684_);
return v_b_688_;
}
else
{
lean_object* v_fst_690_; lean_object* v_snd_691_; lean_object* v___x_692_; lean_object* v_a_693_; lean_object* v___x_694_; lean_object* v___x_695_; lean_object* v_fst_696_; lean_object* v_snd_697_; lean_object* v___x_699_; uint8_t v_isShared_700_; uint8_t v_isSharedCheck_711_; 
v_fst_690_ = lean_ctor_get(v_b_688_, 0);
lean_inc(v_fst_690_);
v_snd_691_ = lean_ctor_get(v_b_688_, 1);
lean_inc(v_snd_691_);
lean_dec_ref(v_b_688_);
v___x_692_ = l_Lean_instInhabitedExpr;
v_a_693_ = lean_array_uget_borrowed(v_as_685_, v_i_687_);
v___x_694_ = lean_array_get_borrowed(v___x_692_, v___x_683_, v_a_693_);
lean_inc(v___x_694_);
lean_inc_ref(v___x_684_);
v___x_695_ = l_StmtKeys_hx(v___x_684_, v___x_694_, v_fst_690_);
v_fst_696_ = lean_ctor_get(v___x_695_, 0);
v_snd_697_ = lean_ctor_get(v___x_695_, 1);
v_isSharedCheck_711_ = !lean_is_exclusive(v___x_695_);
if (v_isSharedCheck_711_ == 0)
{
v___x_699_ = v___x_695_;
v_isShared_700_ = v_isSharedCheck_711_;
goto v_resetjp_698_;
}
else
{
lean_inc(v_snd_697_);
lean_inc(v_fst_696_);
lean_dec(v___x_695_);
v___x_699_ = lean_box(0);
v_isShared_700_ = v_isSharedCheck_711_;
goto v_resetjp_698_;
}
v_resetjp_698_:
{
uint64_t v___x_701_; uint64_t v___x_702_; uint64_t v___x_703_; lean_object* v___x_704_; lean_object* v___x_706_; 
v___x_701_ = lean_unbox_uint64(v_snd_691_);
lean_dec(v_snd_691_);
v___x_702_ = lean_unbox_uint64(v_fst_696_);
lean_dec(v_fst_696_);
v___x_703_ = lean_uint64_mix_hash(v___x_701_, v___x_702_);
v___x_704_ = lean_box_uint64(v___x_703_);
if (v_isShared_700_ == 0)
{
lean_ctor_set(v___x_699_, 1, v___x_704_);
lean_ctor_set(v___x_699_, 0, v_snd_697_);
v___x_706_ = v___x_699_;
goto v_reusejp_705_;
}
else
{
lean_object* v_reuseFailAlloc_710_; 
v_reuseFailAlloc_710_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_710_, 0, v_snd_697_);
lean_ctor_set(v_reuseFailAlloc_710_, 1, v___x_704_);
v___x_706_ = v_reuseFailAlloc_710_;
goto v_reusejp_705_;
}
v_reusejp_705_:
{
size_t v___x_707_; size_t v___x_708_; 
v___x_707_ = ((size_t)1ULL);
v___x_708_ = lean_usize_add(v_i_687_, v___x_707_);
v_i_687_ = v___x_708_;
v_b_688_ = v___x_706_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__11___boxed(lean_object* v___x_712_, lean_object* v___x_713_, lean_object* v_as_714_, lean_object* v_sz_715_, lean_object* v_i_716_, lean_object* v_b_717_){
_start:
{
size_t v_sz_boxed_718_; size_t v_i_boxed_719_; lean_object* v_res_720_; 
v_sz_boxed_718_ = lean_unbox_usize(v_sz_715_);
lean_dec(v_sz_715_);
v_i_boxed_719_ = lean_unbox_usize(v_i_716_);
lean_dec(v_i_716_);
v_res_720_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__11(v___x_712_, v___x_713_, v_as_714_, v_sz_boxed_718_, v_i_boxed_719_, v_b_717_);
lean_dec_ref(v_as_714_);
lean_dec_ref(v___x_712_);
return v_res_720_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___redArg(lean_object* v_hi_721_, lean_object* v_pivot_722_, lean_object* v_as_723_, lean_object* v_i_724_, lean_object* v_k_725_){
_start:
{
uint8_t v___y_731_; uint8_t v___x_737_; 
v___x_737_ = lean_nat_dec_lt(v_k_725_, v_hi_721_);
if (v___x_737_ == 0)
{
lean_object* v___x_738_; lean_object* v___x_739_; 
lean_dec(v_k_725_);
v___x_738_ = lean_array_fswap(v_as_723_, v_i_724_, v_hi_721_);
v___x_739_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_739_, 0, v_i_724_);
lean_ctor_set(v___x_739_, 1, v___x_738_);
return v___x_739_;
}
else
{
lean_object* v___x_740_; lean_object* v_fst_741_; lean_object* v_snd_742_; lean_object* v_fst_743_; lean_object* v_snd_744_; uint64_t v___x_745_; uint64_t v___x_746_; uint8_t v___x_747_; 
v___x_740_ = lean_array_fget_borrowed(v_as_723_, v_k_725_);
v_fst_741_ = lean_ctor_get(v___x_740_, 0);
v_snd_742_ = lean_ctor_get(v___x_740_, 1);
v_fst_743_ = lean_ctor_get(v_pivot_722_, 0);
v_snd_744_ = lean_ctor_get(v_pivot_722_, 1);
v___x_745_ = lean_unbox_uint64(v_fst_741_);
v___x_746_ = lean_unbox_uint64(v_fst_743_);
v___x_747_ = lean_uint64_dec_lt(v___x_745_, v___x_746_);
if (v___x_747_ == 0)
{
uint64_t v___x_748_; uint64_t v___x_749_; uint8_t v___x_750_; 
v___x_748_ = lean_unbox_uint64(v_fst_741_);
v___x_749_ = lean_unbox_uint64(v_fst_743_);
v___x_750_ = lean_uint64_dec_eq(v___x_748_, v___x_749_);
if (v___x_750_ == 0)
{
goto v___jp_726_;
}
else
{
uint8_t v___x_751_; 
v___x_751_ = lean_nat_dec_lt(v_snd_742_, v_snd_744_);
v___y_731_ = v___x_751_;
goto v___jp_730_;
}
}
else
{
v___y_731_ = v___x_747_;
goto v___jp_730_;
}
}
v___jp_726_:
{
lean_object* v___x_727_; lean_object* v___x_728_; 
v___x_727_ = lean_unsigned_to_nat(1u);
v___x_728_ = lean_nat_add(v_k_725_, v___x_727_);
lean_dec(v_k_725_);
v_k_725_ = v___x_728_;
goto _start;
}
v___jp_730_:
{
if (v___y_731_ == 0)
{
goto v___jp_726_;
}
else
{
lean_object* v___x_732_; lean_object* v___x_733_; lean_object* v___x_734_; lean_object* v___x_735_; 
v___x_732_ = lean_array_fswap(v_as_723_, v_i_724_, v_k_725_);
v___x_733_ = lean_unsigned_to_nat(1u);
v___x_734_ = lean_nat_add(v_i_724_, v___x_733_);
lean_dec(v_i_724_);
v___x_735_ = lean_nat_add(v_k_725_, v___x_733_);
lean_dec(v_k_725_);
v_as_723_ = v___x_732_;
v_i_724_ = v___x_734_;
v_k_725_ = v___x_735_;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___redArg___boxed(lean_object* v_hi_752_, lean_object* v_pivot_753_, lean_object* v_as_754_, lean_object* v_i_755_, lean_object* v_k_756_){
_start:
{
lean_object* v_res_757_; 
v_res_757_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___redArg(v_hi_752_, v_pivot_753_, v_as_754_, v_i_755_, v_k_756_);
lean_dec_ref(v_pivot_753_);
lean_dec(v_hi_752_);
return v_res_757_;
}
}
LEAN_EXPORT uint8_t l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0(uint8_t v___x_758_, lean_object* v_a_759_, lean_object* v_b_760_){
_start:
{
lean_object* v_fst_761_; lean_object* v_snd_762_; lean_object* v_fst_763_; lean_object* v_snd_764_; uint64_t v___x_765_; uint64_t v___x_766_; uint8_t v___x_767_; 
v_fst_761_ = lean_ctor_get(v_a_759_, 0);
v_snd_762_ = lean_ctor_get(v_a_759_, 1);
v_fst_763_ = lean_ctor_get(v_b_760_, 0);
v_snd_764_ = lean_ctor_get(v_b_760_, 1);
v___x_765_ = lean_unbox_uint64(v_fst_761_);
v___x_766_ = lean_unbox_uint64(v_fst_763_);
v___x_767_ = lean_uint64_dec_lt(v___x_765_, v___x_766_);
if (v___x_767_ == 0)
{
uint64_t v___x_768_; uint64_t v___x_769_; uint8_t v___x_770_; 
v___x_768_ = lean_unbox_uint64(v_fst_761_);
v___x_769_ = lean_unbox_uint64(v_fst_763_);
v___x_770_ = lean_uint64_dec_eq(v___x_768_, v___x_769_);
if (v___x_770_ == 0)
{
return v___x_758_;
}
else
{
uint8_t v___x_771_; 
v___x_771_ = lean_nat_dec_lt(v_snd_762_, v_snd_764_);
return v___x_771_;
}
}
else
{
return v___x_767_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0___boxed(lean_object* v___x_772_, lean_object* v_a_773_, lean_object* v_b_774_){
_start:
{
uint8_t v___x_9134__boxed_775_; uint8_t v_res_776_; lean_object* v_r_777_; 
v___x_9134__boxed_775_ = lean_unbox(v___x_772_);
v_res_776_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0(v___x_9134__boxed_775_, v_a_773_, v_b_774_);
lean_dec_ref(v_b_774_);
lean_dec_ref(v_a_773_);
v_r_777_ = lean_box(v_res_776_);
return v_r_777_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg(lean_object* v_n_778_, lean_object* v_as_779_, lean_object* v_lo_780_, lean_object* v_hi_781_){
_start:
{
lean_object* v___y_783_; uint8_t v___x_793_; 
v___x_793_ = lean_nat_dec_lt(v_lo_780_, v_hi_781_);
if (v___x_793_ == 0)
{
lean_dec(v_lo_780_);
return v_as_779_;
}
else
{
uint8_t v___x_794_; lean_object* v___x_795_; lean_object* v___x_796_; lean_object* v_mid_797_; lean_object* v___y_799_; lean_object* v___y_805_; lean_object* v___x_810_; lean_object* v___x_811_; uint8_t v___x_812_; 
v___x_794_ = 0;
v___x_795_ = lean_nat_add(v_lo_780_, v_hi_781_);
v___x_796_ = lean_unsigned_to_nat(1u);
v_mid_797_ = lean_nat_shiftr(v___x_795_, v___x_796_);
lean_dec(v___x_795_);
v___x_810_ = lean_array_fget_borrowed(v_as_779_, v_mid_797_);
v___x_811_ = lean_array_fget_borrowed(v_as_779_, v_lo_780_);
v___x_812_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0(v___x_794_, v___x_810_, v___x_811_);
if (v___x_812_ == 0)
{
v___y_805_ = v_as_779_;
goto v___jp_804_;
}
else
{
lean_object* v___x_813_; 
v___x_813_ = lean_array_fswap(v_as_779_, v_lo_780_, v_mid_797_);
v___y_805_ = v___x_813_;
goto v___jp_804_;
}
v___jp_798_:
{
lean_object* v___x_800_; lean_object* v___x_801_; uint8_t v___x_802_; 
v___x_800_ = lean_array_fget_borrowed(v___y_799_, v_mid_797_);
v___x_801_ = lean_array_fget_borrowed(v___y_799_, v_hi_781_);
v___x_802_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0(v___x_794_, v___x_800_, v___x_801_);
if (v___x_802_ == 0)
{
lean_dec(v_mid_797_);
v___y_783_ = v___y_799_;
goto v___jp_782_;
}
else
{
lean_object* v___x_803_; 
v___x_803_ = lean_array_fswap(v___y_799_, v_mid_797_, v_hi_781_);
lean_dec(v_mid_797_);
v___y_783_ = v___x_803_;
goto v___jp_782_;
}
}
v___jp_804_:
{
lean_object* v___x_806_; lean_object* v___x_807_; uint8_t v___x_808_; 
v___x_806_ = lean_array_fget_borrowed(v___y_805_, v_hi_781_);
v___x_807_ = lean_array_fget_borrowed(v___y_805_, v_lo_780_);
v___x_808_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___lam__0(v___x_794_, v___x_806_, v___x_807_);
if (v___x_808_ == 0)
{
v___y_799_ = v___y_805_;
goto v___jp_798_;
}
else
{
lean_object* v___x_809_; 
v___x_809_ = lean_array_fswap(v___y_805_, v_lo_780_, v_hi_781_);
v___y_799_ = v___x_809_;
goto v___jp_798_;
}
}
}
v___jp_782_:
{
lean_object* v_pivot_784_; lean_object* v___x_785_; lean_object* v_fst_786_; lean_object* v_snd_787_; uint8_t v___x_788_; 
v_pivot_784_ = lean_array_fget(v___y_783_, v_hi_781_);
lean_inc_n(v_lo_780_, 2);
v___x_785_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___redArg(v_hi_781_, v_pivot_784_, v___y_783_, v_lo_780_, v_lo_780_);
lean_dec(v_pivot_784_);
v_fst_786_ = lean_ctor_get(v___x_785_, 0);
lean_inc(v_fst_786_);
v_snd_787_ = lean_ctor_get(v___x_785_, 1);
lean_inc(v_snd_787_);
lean_dec_ref(v___x_785_);
v___x_788_ = lean_nat_dec_le(v_hi_781_, v_fst_786_);
if (v___x_788_ == 0)
{
lean_object* v___x_789_; lean_object* v___x_790_; lean_object* v___x_791_; 
v___x_789_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg(v_n_778_, v_snd_787_, v_lo_780_, v_fst_786_);
v___x_790_ = lean_unsigned_to_nat(1u);
v___x_791_ = lean_nat_add(v_fst_786_, v___x_790_);
lean_dec(v_fst_786_);
v_as_779_ = v___x_789_;
v_lo_780_ = v___x_791_;
goto _start;
}
else
{
lean_dec(v_fst_786_);
lean_dec(v_lo_780_);
return v_snd_787_;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg___boxed(lean_object* v_n_814_, lean_object* v_as_815_, lean_object* v_lo_816_, lean_object* v_hi_817_){
_start:
{
lean_object* v_res_818_; 
v_res_818_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg(v_n_814_, v_as_815_, v_lo_816_, v_hi_817_);
lean_dec(v_hi_817_);
lean_dec(v_n_814_);
return v_res_818_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3_spec__4(lean_object* v_as_819_, size_t v_sz_820_, size_t v_i_821_, lean_object* v_b_822_){
_start:
{
uint8_t v___x_823_; lean_object* v___y_825_; 
v___x_823_ = lean_usize_dec_lt(v_i_821_, v_sz_820_);
if (v___x_823_ == 0)
{
return v_b_822_;
}
else
{
lean_object* v_a_831_; 
v_a_831_ = lean_array_uget_borrowed(v_as_819_, v_i_821_);
if (lean_obj_tag(v_a_831_) == 2)
{
lean_object* v_i_832_; 
v_i_832_ = lean_ctor_get(v_a_831_, 1);
v___y_825_ = v_i_832_;
goto v___jp_824_;
}
else
{
lean_object* v_i_833_; 
v_i_833_ = lean_unsigned_to_nat(0u);
v___y_825_ = v_i_833_;
goto v___jp_824_;
}
}
v___jp_824_:
{
lean_object* v___x_826_; lean_object* v___x_827_; size_t v___x_828_; size_t v___x_829_; 
v___x_826_ = lean_box(v___x_823_);
v___x_827_ = lean_array_set(v_b_822_, v___y_825_, v___x_826_);
v___x_828_ = ((size_t)1ULL);
v___x_829_ = lean_usize_add(v_i_821_, v___x_828_);
v_i_821_ = v___x_829_;
v_b_822_ = v___x_827_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3_spec__4___boxed(lean_object* v_as_834_, lean_object* v_sz_835_, lean_object* v_i_836_, lean_object* v_b_837_){
_start:
{
size_t v_sz_boxed_838_; size_t v_i_boxed_839_; lean_object* v_res_840_; 
v_sz_boxed_838_ = lean_unbox_usize(v_sz_835_);
lean_dec(v_sz_835_);
v_i_boxed_839_ = lean_unbox_usize(v_i_836_);
lean_dec(v_i_836_);
v_res_840_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3_spec__4(v_as_834_, v_sz_boxed_838_, v_i_boxed_839_, v_b_837_);
lean_dec_ref(v_as_834_);
return v_res_840_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3(lean_object* v_as_841_, size_t v_sz_842_, size_t v_i_843_, lean_object* v_b_844_){
_start:
{
uint8_t v___x_845_; lean_object* v___y_847_; 
v___x_845_ = lean_usize_dec_lt(v_i_843_, v_sz_842_);
if (v___x_845_ == 0)
{
return v_b_844_;
}
else
{
lean_object* v_a_853_; 
v_a_853_ = lean_array_uget_borrowed(v_as_841_, v_i_843_);
if (lean_obj_tag(v_a_853_) == 2)
{
lean_object* v_i_854_; 
v_i_854_ = lean_ctor_get(v_a_853_, 1);
v___y_847_ = v_i_854_;
goto v___jp_846_;
}
else
{
lean_object* v_i_855_; 
v_i_855_ = lean_unsigned_to_nat(0u);
v___y_847_ = v_i_855_;
goto v___jp_846_;
}
}
v___jp_846_:
{
lean_object* v___x_848_; lean_object* v___x_849_; size_t v___x_850_; size_t v___x_851_; lean_object* v___x_852_; 
v___x_848_ = lean_box(v___x_845_);
v___x_849_ = lean_array_set(v_b_844_, v___y_847_, v___x_848_);
v___x_850_ = ((size_t)1ULL);
v___x_851_ = lean_usize_add(v_i_843_, v___x_850_);
v___x_852_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00__private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3_spec__4(v_as_841_, v_sz_842_, v___x_851_, v___x_849_);
return v___x_852_;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3___boxed(lean_object* v_as_856_, lean_object* v_sz_857_, lean_object* v_i_858_, lean_object* v_b_859_){
_start:
{
size_t v_sz_boxed_860_; size_t v_i_boxed_861_; lean_object* v_res_862_; 
v_sz_boxed_860_ = lean_unbox_usize(v_sz_857_);
lean_dec(v_sz_857_);
v_i_boxed_861_ = lean_unbox_usize(v_i_858_);
lean_dec(v_i_858_);
v_res_862_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3(v_as_856_, v_sz_boxed_860_, v_i_boxed_861_, v_b_859_);
lean_dec_ref(v_as_856_);
return v_res_862_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___redArg(lean_object* v___x_863_, lean_object* v_range_864_, lean_object* v_b_865_, lean_object* v_i_866_){
_start:
{
lean_object* v_stop_867_; lean_object* v_step_868_; uint8_t v___x_869_; 
v_stop_867_ = lean_ctor_get(v_range_864_, 1);
v_step_868_ = lean_ctor_get(v_range_864_, 2);
v___x_869_ = lean_nat_dec_lt(v_i_866_, v_stop_867_);
if (v___x_869_ == 0)
{
lean_dec(v_i_866_);
return v_b_865_;
}
else
{
lean_object* v___x_870_; lean_object* v___x_871_; size_t v_sz_872_; size_t v___x_873_; lean_object* v___x_874_; lean_object* v___x_875_; 
v___x_870_ = lean_obj_once(&l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0, &l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0_once, _init_l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0);
v___x_871_ = lean_array_get_borrowed(v___x_870_, v___x_863_, v_i_866_);
v_sz_872_ = lean_array_size(v___x_871_);
v___x_873_ = ((size_t)0ULL);
v___x_874_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3(v___x_871_, v_sz_872_, v___x_873_, v_b_865_);
v___x_875_ = lean_nat_add(v_i_866_, v_step_868_);
lean_dec(v_i_866_);
v_b_865_ = v___x_874_;
v_i_866_ = v___x_875_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___redArg___boxed(lean_object* v___x_877_, lean_object* v_range_878_, lean_object* v_b_879_, lean_object* v_i_880_){
_start:
{
lean_object* v_res_881_; 
v_res_881_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___redArg(v___x_877_, v_range_878_, v_b_879_, v_i_880_);
lean_dec_ref(v_range_878_);
lean_dec_ref(v___x_877_);
return v_res_881_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__13(lean_object* v___x_882_, lean_object* v___x_883_, lean_object* v_as_884_, size_t v_sz_885_, size_t v_i_886_, lean_object* v_b_887_){
_start:
{
uint8_t v___x_888_; 
v___x_888_ = lean_usize_dec_lt(v_i_886_, v_sz_885_);
if (v___x_888_ == 0)
{
lean_dec_ref(v___x_883_);
return v_b_887_;
}
else
{
lean_object* v_a_889_; lean_object* v_snd_890_; lean_object* v_fst_891_; lean_object* v_snd_892_; lean_object* v___x_893_; lean_object* v___x_894_; lean_object* v___x_895_; lean_object* v_fst_896_; lean_object* v_snd_897_; lean_object* v___x_899_; uint8_t v_isShared_900_; uint8_t v_isSharedCheck_908_; 
v_a_889_ = lean_array_uget_borrowed(v_as_884_, v_i_886_);
v_snd_890_ = lean_ctor_get(v_a_889_, 1);
v_fst_891_ = lean_ctor_get(v_b_887_, 0);
lean_inc(v_fst_891_);
v_snd_892_ = lean_ctor_get(v_b_887_, 1);
lean_inc(v_snd_892_);
lean_dec_ref(v_b_887_);
v___x_893_ = l_Lean_instInhabitedExpr;
v___x_894_ = lean_array_get_borrowed(v___x_893_, v___x_882_, v_snd_890_);
lean_inc(v___x_894_);
lean_inc_ref(v___x_883_);
v___x_895_ = l_StmtKeys_hx(v___x_883_, v___x_894_, v_fst_891_);
v_fst_896_ = lean_ctor_get(v___x_895_, 0);
v_snd_897_ = lean_ctor_get(v___x_895_, 1);
v_isSharedCheck_908_ = !lean_is_exclusive(v___x_895_);
if (v_isSharedCheck_908_ == 0)
{
v___x_899_ = v___x_895_;
v_isShared_900_ = v_isSharedCheck_908_;
goto v_resetjp_898_;
}
else
{
lean_inc(v_snd_897_);
lean_inc(v_fst_896_);
lean_dec(v___x_895_);
v___x_899_ = lean_box(0);
v_isShared_900_ = v_isSharedCheck_908_;
goto v_resetjp_898_;
}
v_resetjp_898_:
{
lean_object* v___x_901_; lean_object* v___x_903_; 
v___x_901_ = lean_array_push(v_snd_892_, v_fst_896_);
if (v_isShared_900_ == 0)
{
lean_ctor_set(v___x_899_, 1, v___x_901_);
lean_ctor_set(v___x_899_, 0, v_snd_897_);
v___x_903_ = v___x_899_;
goto v_reusejp_902_;
}
else
{
lean_object* v_reuseFailAlloc_907_; 
v_reuseFailAlloc_907_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_907_, 0, v_snd_897_);
lean_ctor_set(v_reuseFailAlloc_907_, 1, v___x_901_);
v___x_903_ = v_reuseFailAlloc_907_;
goto v_reusejp_902_;
}
v_reusejp_902_:
{
size_t v___x_904_; size_t v___x_905_; 
v___x_904_ = ((size_t)1ULL);
v___x_905_ = lean_usize_add(v_i_886_, v___x_904_);
v_i_886_ = v___x_905_;
v_b_887_ = v___x_903_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__13___boxed(lean_object* v___x_909_, lean_object* v___x_910_, lean_object* v_as_911_, lean_object* v_sz_912_, lean_object* v_i_913_, lean_object* v_b_914_){
_start:
{
size_t v_sz_boxed_915_; size_t v_i_boxed_916_; lean_object* v_res_917_; 
v_sz_boxed_915_ = lean_unbox_usize(v_sz_912_);
lean_dec(v_sz_912_);
v_i_boxed_916_ = lean_unbox_usize(v_i_913_);
lean_dec(v_i_913_);
v_res_917_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__13(v___x_909_, v___x_910_, v_as_911_, v_sz_boxed_915_, v_i_boxed_916_, v_b_914_);
lean_dec_ref(v_as_911_);
lean_dec_ref(v___x_909_);
return v_res_917_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___redArg(lean_object* v___x_918_, lean_object* v_range_919_, lean_object* v_b_920_, lean_object* v_i_921_){
_start:
{
lean_object* v_stop_922_; lean_object* v_step_923_; lean_object* v_a_925_; uint8_t v___x_928_; 
v_stop_922_ = lean_ctor_get(v_range_919_, 1);
v_step_923_ = lean_ctor_get(v_range_919_, 2);
v___x_928_ = lean_nat_dec_lt(v_i_921_, v_stop_922_);
if (v___x_928_ == 0)
{
lean_dec(v_i_921_);
return v_b_920_;
}
else
{
lean_object* v_fst_929_; lean_object* v_snd_930_; lean_object* v___x_932_; uint8_t v_isShared_933_; uint8_t v_isSharedCheck_949_; 
v_fst_929_ = lean_ctor_get(v_b_920_, 0);
v_snd_930_ = lean_ctor_get(v_b_920_, 1);
v_isSharedCheck_949_ = !lean_is_exclusive(v_b_920_);
if (v_isSharedCheck_949_ == 0)
{
v___x_932_ = v_b_920_;
v_isShared_933_ = v_isSharedCheck_949_;
goto v_resetjp_931_;
}
else
{
lean_inc(v_snd_930_);
lean_inc(v_fst_929_);
lean_dec(v_b_920_);
v___x_932_ = lean_box(0);
v_isShared_933_ = v_isSharedCheck_949_;
goto v_resetjp_931_;
}
v_resetjp_931_:
{
uint8_t v___x_938_; lean_object* v___x_939_; lean_object* v___x_940_; uint8_t v___x_941_; 
v___x_938_ = 0;
v___x_939_ = lean_box(v___x_938_);
v___x_940_ = lean_array_get(v___x_939_, v___x_918_, v_i_921_);
lean_dec(v___x_939_);
v___x_941_ = lean_unbox(v___x_940_);
if (v___x_941_ == 0)
{
lean_dec(v___x_940_);
goto v___jp_934_;
}
else
{
lean_object* v___x_942_; lean_object* v___x_943_; uint8_t v___x_944_; 
v___x_942_ = lean_box(v___x_938_);
v___x_943_ = lean_array_get(v___x_942_, v_snd_930_, v_i_921_);
lean_dec(v___x_942_);
v___x_944_ = lean_unbox(v___x_943_);
lean_dec(v___x_943_);
if (v___x_944_ == 0)
{
uint8_t v___x_945_; 
v___x_945_ = lean_unbox(v___x_940_);
if (v___x_945_ == 0)
{
lean_dec(v___x_940_);
goto v___jp_934_;
}
else
{
lean_object* v___x_946_; lean_object* v___x_947_; lean_object* v___x_948_; 
lean_del_object(v___x_932_);
v___x_946_ = lean_array_set(v_snd_930_, v_i_921_, v___x_940_);
lean_inc(v_i_921_);
v___x_947_ = lean_array_push(v_fst_929_, v_i_921_);
v___x_948_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_948_, 0, v___x_947_);
lean_ctor_set(v___x_948_, 1, v___x_946_);
v_a_925_ = v___x_948_;
goto v___jp_924_;
}
}
else
{
lean_dec(v___x_940_);
goto v___jp_934_;
}
}
v___jp_934_:
{
lean_object* v___x_936_; 
if (v_isShared_933_ == 0)
{
v___x_936_ = v___x_932_;
goto v_reusejp_935_;
}
else
{
lean_object* v_reuseFailAlloc_937_; 
v_reuseFailAlloc_937_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_937_, 0, v_fst_929_);
lean_ctor_set(v_reuseFailAlloc_937_, 1, v_snd_930_);
v___x_936_ = v_reuseFailAlloc_937_;
goto v_reusejp_935_;
}
v_reusejp_935_:
{
v_a_925_ = v___x_936_;
goto v___jp_924_;
}
}
}
}
v___jp_924_:
{
lean_object* v___x_926_; 
v___x_926_ = lean_nat_add(v_i_921_, v_step_923_);
lean_dec(v_i_921_);
v_b_920_ = v_a_925_;
v_i_921_ = v___x_926_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___redArg___boxed(lean_object* v___x_950_, lean_object* v_range_951_, lean_object* v_b_952_, lean_object* v_i_953_){
_start:
{
lean_object* v_res_954_; 
v_res_954_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___redArg(v___x_950_, v_range_951_, v_b_952_, v_i_953_);
lean_dec_ref(v_range_951_);
lean_dec_ref(v___x_950_);
return v_res_954_;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__0___redArg(lean_object* v_a_955_){
_start:
{
lean_object* v_snd_956_; lean_object* v_snd_957_; lean_object* v_fst_958_; 
v_snd_956_ = lean_ctor_get(v_a_955_, 1);
lean_inc(v_snd_956_);
v_snd_957_ = lean_ctor_get(v_snd_956_, 1);
lean_inc(v_snd_957_);
v_fst_958_ = lean_ctor_get(v_snd_957_, 0);
lean_inc(v_fst_958_);
switch(lean_obj_tag(v_fst_958_))
{
case 10:
{
lean_object* v_fst_959_; lean_object* v___x_961_; uint8_t v_isShared_962_; uint8_t v_isSharedCheck_986_; 
v_fst_959_ = lean_ctor_get(v_a_955_, 0);
v_isSharedCheck_986_ = !lean_is_exclusive(v_a_955_);
if (v_isSharedCheck_986_ == 0)
{
lean_object* v_unused_987_; 
v_unused_987_ = lean_ctor_get(v_a_955_, 1);
lean_dec(v_unused_987_);
v___x_961_ = v_a_955_;
v_isShared_962_ = v_isSharedCheck_986_;
goto v_resetjp_960_;
}
else
{
lean_inc(v_fst_959_);
lean_dec(v_a_955_);
v___x_961_ = lean_box(0);
v_isShared_962_ = v_isSharedCheck_986_;
goto v_resetjp_960_;
}
v_resetjp_960_:
{
lean_object* v_fst_963_; lean_object* v___x_965_; uint8_t v_isShared_966_; uint8_t v_isSharedCheck_984_; 
v_fst_963_ = lean_ctor_get(v_snd_956_, 0);
v_isSharedCheck_984_ = !lean_is_exclusive(v_snd_956_);
if (v_isSharedCheck_984_ == 0)
{
lean_object* v_unused_985_; 
v_unused_985_ = lean_ctor_get(v_snd_956_, 1);
lean_dec(v_unused_985_);
v___x_965_ = v_snd_956_;
v_isShared_966_ = v_isSharedCheck_984_;
goto v_resetjp_964_;
}
else
{
lean_inc(v_fst_963_);
lean_dec(v_snd_956_);
v___x_965_ = lean_box(0);
v_isShared_966_ = v_isSharedCheck_984_;
goto v_resetjp_964_;
}
v_resetjp_964_:
{
lean_object* v_snd_967_; lean_object* v___x_969_; uint8_t v_isShared_970_; uint8_t v_isSharedCheck_982_; 
v_snd_967_ = lean_ctor_get(v_snd_957_, 1);
v_isSharedCheck_982_ = !lean_is_exclusive(v_snd_957_);
if (v_isSharedCheck_982_ == 0)
{
lean_object* v_unused_983_; 
v_unused_983_ = lean_ctor_get(v_snd_957_, 0);
lean_dec(v_unused_983_);
v___x_969_ = v_snd_957_;
v_isShared_970_ = v_isSharedCheck_982_;
goto v_resetjp_968_;
}
else
{
lean_inc(v_snd_967_);
lean_dec(v_snd_957_);
v___x_969_ = lean_box(0);
v_isShared_970_ = v_isSharedCheck_982_;
goto v_resetjp_968_;
}
v_resetjp_968_:
{
lean_object* v_expr_971_; lean_object* v___x_973_; 
v_expr_971_ = lean_ctor_get(v_fst_958_, 1);
lean_inc_ref(v_expr_971_);
lean_dec_ref_known(v_fst_958_, 2);
if (v_isShared_970_ == 0)
{
lean_ctor_set(v___x_969_, 0, v_expr_971_);
v___x_973_ = v___x_969_;
goto v_reusejp_972_;
}
else
{
lean_object* v_reuseFailAlloc_981_; 
v_reuseFailAlloc_981_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_981_, 0, v_expr_971_);
lean_ctor_set(v_reuseFailAlloc_981_, 1, v_snd_967_);
v___x_973_ = v_reuseFailAlloc_981_;
goto v_reusejp_972_;
}
v_reusejp_972_:
{
lean_object* v___x_975_; 
if (v_isShared_966_ == 0)
{
lean_ctor_set(v___x_965_, 1, v___x_973_);
v___x_975_ = v___x_965_;
goto v_reusejp_974_;
}
else
{
lean_object* v_reuseFailAlloc_980_; 
v_reuseFailAlloc_980_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_980_, 0, v_fst_963_);
lean_ctor_set(v_reuseFailAlloc_980_, 1, v___x_973_);
v___x_975_ = v_reuseFailAlloc_980_;
goto v_reusejp_974_;
}
v_reusejp_974_:
{
lean_object* v___x_977_; 
if (v_isShared_962_ == 0)
{
lean_ctor_set(v___x_961_, 1, v___x_975_);
v___x_977_ = v___x_961_;
goto v_reusejp_976_;
}
else
{
lean_object* v_reuseFailAlloc_979_; 
v_reuseFailAlloc_979_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_979_, 0, v_fst_959_);
lean_ctor_set(v_reuseFailAlloc_979_, 1, v___x_975_);
v___x_977_ = v_reuseFailAlloc_979_;
goto v_reusejp_976_;
}
v_reusejp_976_:
{
v_a_955_ = v___x_977_;
goto _start;
}
}
}
}
}
}
}
case 7:
{
lean_object* v_fst_988_; lean_object* v___x_990_; uint8_t v_isShared_991_; uint8_t v_isSharedCheck_1024_; 
v_fst_988_ = lean_ctor_get(v_a_955_, 0);
v_isSharedCheck_1024_ = !lean_is_exclusive(v_a_955_);
if (v_isSharedCheck_1024_ == 0)
{
lean_object* v_unused_1025_; 
v_unused_1025_ = lean_ctor_get(v_a_955_, 1);
lean_dec(v_unused_1025_);
v___x_990_ = v_a_955_;
v_isShared_991_ = v_isSharedCheck_1024_;
goto v_resetjp_989_;
}
else
{
lean_inc(v_fst_988_);
lean_dec(v_a_955_);
v___x_990_ = lean_box(0);
v_isShared_991_ = v_isSharedCheck_1024_;
goto v_resetjp_989_;
}
v_resetjp_989_:
{
lean_object* v_fst_992_; lean_object* v___x_994_; uint8_t v_isShared_995_; uint8_t v_isSharedCheck_1022_; 
v_fst_992_ = lean_ctor_get(v_snd_956_, 0);
v_isSharedCheck_1022_ = !lean_is_exclusive(v_snd_956_);
if (v_isSharedCheck_1022_ == 0)
{
lean_object* v_unused_1023_; 
v_unused_1023_ = lean_ctor_get(v_snd_956_, 1);
lean_dec(v_unused_1023_);
v___x_994_ = v_snd_956_;
v_isShared_995_ = v_isSharedCheck_1022_;
goto v_resetjp_993_;
}
else
{
lean_inc(v_fst_992_);
lean_dec(v_snd_956_);
v___x_994_ = lean_box(0);
v_isShared_995_ = v_isSharedCheck_1022_;
goto v_resetjp_993_;
}
v_resetjp_993_:
{
lean_object* v_snd_996_; lean_object* v___x_998_; uint8_t v_isShared_999_; uint8_t v_isSharedCheck_1020_; 
v_snd_996_ = lean_ctor_get(v_snd_957_, 1);
v_isSharedCheck_1020_ = !lean_is_exclusive(v_snd_957_);
if (v_isSharedCheck_1020_ == 0)
{
lean_object* v_unused_1021_; 
v_unused_1021_ = lean_ctor_get(v_snd_957_, 0);
lean_dec(v_unused_1021_);
v___x_998_ = v_snd_957_;
v_isShared_999_ = v_isSharedCheck_1020_;
goto v_resetjp_997_;
}
else
{
lean_inc(v_snd_996_);
lean_dec(v_snd_957_);
v___x_998_ = lean_box(0);
v_isShared_999_ = v_isSharedCheck_1020_;
goto v_resetjp_997_;
}
v_resetjp_997_:
{
lean_object* v_binderType_1000_; lean_object* v_body_1001_; lean_object* v___x_1002_; lean_object* v___x_1003_; lean_object* v___x_1004_; lean_object* v___x_1005_; lean_object* v___x_1006_; lean_object* v___x_1007_; lean_object* v___x_1008_; lean_object* v___x_1009_; lean_object* v___x_1011_; 
v_binderType_1000_ = lean_ctor_get(v_fst_958_, 1);
lean_inc_ref(v_binderType_1000_);
v_body_1001_ = lean_ctor_get(v_fst_958_, 2);
lean_inc_ref(v_body_1001_);
lean_dec_ref_known(v_fst_958_, 3);
v___x_1002_ = lean_expr_instantiate_rev(v_binderType_1000_, v_fst_992_);
lean_dec_ref(v_binderType_1000_);
v___x_1003_ = lean_array_push(v_fst_988_, v___x_1002_);
v___x_1004_ = ((lean_object*)(l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg___closed__1));
lean_inc(v_snd_996_);
v___x_1005_ = l_Lean_Name_num___override(v___x_1004_, v_snd_996_);
v___x_1006_ = l_Lean_Expr_fvar___override(v___x_1005_);
v___x_1007_ = lean_array_push(v_fst_992_, v___x_1006_);
v___x_1008_ = lean_unsigned_to_nat(1u);
v___x_1009_ = lean_nat_add(v_snd_996_, v___x_1008_);
lean_dec(v_snd_996_);
if (v_isShared_999_ == 0)
{
lean_ctor_set(v___x_998_, 1, v___x_1009_);
lean_ctor_set(v___x_998_, 0, v_body_1001_);
v___x_1011_ = v___x_998_;
goto v_reusejp_1010_;
}
else
{
lean_object* v_reuseFailAlloc_1019_; 
v_reuseFailAlloc_1019_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1019_, 0, v_body_1001_);
lean_ctor_set(v_reuseFailAlloc_1019_, 1, v___x_1009_);
v___x_1011_ = v_reuseFailAlloc_1019_;
goto v_reusejp_1010_;
}
v_reusejp_1010_:
{
lean_object* v___x_1013_; 
if (v_isShared_995_ == 0)
{
lean_ctor_set(v___x_994_, 1, v___x_1011_);
lean_ctor_set(v___x_994_, 0, v___x_1007_);
v___x_1013_ = v___x_994_;
goto v_reusejp_1012_;
}
else
{
lean_object* v_reuseFailAlloc_1018_; 
v_reuseFailAlloc_1018_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1018_, 0, v___x_1007_);
lean_ctor_set(v_reuseFailAlloc_1018_, 1, v___x_1011_);
v___x_1013_ = v_reuseFailAlloc_1018_;
goto v_reusejp_1012_;
}
v_reusejp_1012_:
{
lean_object* v___x_1015_; 
if (v_isShared_991_ == 0)
{
lean_ctor_set(v___x_990_, 1, v___x_1013_);
lean_ctor_set(v___x_990_, 0, v___x_1003_);
v___x_1015_ = v___x_990_;
goto v_reusejp_1014_;
}
else
{
lean_object* v_reuseFailAlloc_1017_; 
v_reuseFailAlloc_1017_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1017_, 0, v___x_1003_);
lean_ctor_set(v_reuseFailAlloc_1017_, 1, v___x_1013_);
v___x_1015_ = v_reuseFailAlloc_1017_;
goto v_reusejp_1014_;
}
v_reusejp_1014_:
{
v_a_955_ = v___x_1015_;
goto _start;
}
}
}
}
}
}
}
default: 
{
lean_object* v_fst_1026_; lean_object* v___x_1028_; uint8_t v_isShared_1029_; uint8_t v_isSharedCheck_1051_; 
v_fst_1026_ = lean_ctor_get(v_a_955_, 0);
v_isSharedCheck_1051_ = !lean_is_exclusive(v_a_955_);
if (v_isSharedCheck_1051_ == 0)
{
lean_object* v_unused_1052_; 
v_unused_1052_ = lean_ctor_get(v_a_955_, 1);
lean_dec(v_unused_1052_);
v___x_1028_ = v_a_955_;
v_isShared_1029_ = v_isSharedCheck_1051_;
goto v_resetjp_1027_;
}
else
{
lean_inc(v_fst_1026_);
lean_dec(v_a_955_);
v___x_1028_ = lean_box(0);
v_isShared_1029_ = v_isSharedCheck_1051_;
goto v_resetjp_1027_;
}
v_resetjp_1027_:
{
lean_object* v_fst_1030_; lean_object* v___x_1032_; uint8_t v_isShared_1033_; uint8_t v_isSharedCheck_1049_; 
v_fst_1030_ = lean_ctor_get(v_snd_956_, 0);
v_isSharedCheck_1049_ = !lean_is_exclusive(v_snd_956_);
if (v_isSharedCheck_1049_ == 0)
{
lean_object* v_unused_1050_; 
v_unused_1050_ = lean_ctor_get(v_snd_956_, 1);
lean_dec(v_unused_1050_);
v___x_1032_ = v_snd_956_;
v_isShared_1033_ = v_isSharedCheck_1049_;
goto v_resetjp_1031_;
}
else
{
lean_inc(v_fst_1030_);
lean_dec(v_snd_956_);
v___x_1032_ = lean_box(0);
v_isShared_1033_ = v_isSharedCheck_1049_;
goto v_resetjp_1031_;
}
v_resetjp_1031_:
{
lean_object* v_snd_1034_; lean_object* v___x_1036_; uint8_t v_isShared_1037_; uint8_t v_isSharedCheck_1047_; 
v_snd_1034_ = lean_ctor_get(v_snd_957_, 1);
v_isSharedCheck_1047_ = !lean_is_exclusive(v_snd_957_);
if (v_isSharedCheck_1047_ == 0)
{
lean_object* v_unused_1048_; 
v_unused_1048_ = lean_ctor_get(v_snd_957_, 0);
lean_dec(v_unused_1048_);
v___x_1036_ = v_snd_957_;
v_isShared_1037_ = v_isSharedCheck_1047_;
goto v_resetjp_1035_;
}
else
{
lean_inc(v_snd_1034_);
lean_dec(v_snd_957_);
v___x_1036_ = lean_box(0);
v_isShared_1037_ = v_isSharedCheck_1047_;
goto v_resetjp_1035_;
}
v_resetjp_1035_:
{
lean_object* v___x_1039_; 
if (v_isShared_1037_ == 0)
{
v___x_1039_ = v___x_1036_;
goto v_reusejp_1038_;
}
else
{
lean_object* v_reuseFailAlloc_1046_; 
v_reuseFailAlloc_1046_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1046_, 0, v_fst_958_);
lean_ctor_set(v_reuseFailAlloc_1046_, 1, v_snd_1034_);
v___x_1039_ = v_reuseFailAlloc_1046_;
goto v_reusejp_1038_;
}
v_reusejp_1038_:
{
lean_object* v___x_1041_; 
if (v_isShared_1033_ == 0)
{
lean_ctor_set(v___x_1032_, 1, v___x_1039_);
v___x_1041_ = v___x_1032_;
goto v_reusejp_1040_;
}
else
{
lean_object* v_reuseFailAlloc_1045_; 
v_reuseFailAlloc_1045_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1045_, 0, v_fst_1030_);
lean_ctor_set(v_reuseFailAlloc_1045_, 1, v___x_1039_);
v___x_1041_ = v_reuseFailAlloc_1045_;
goto v_reusejp_1040_;
}
v_reusejp_1040_:
{
lean_object* v___x_1043_; 
if (v_isShared_1029_ == 0)
{
lean_ctor_set(v___x_1028_, 1, v___x_1041_);
v___x_1043_ = v___x_1028_;
goto v_reusejp_1042_;
}
else
{
lean_object* v_reuseFailAlloc_1044_; 
v_reuseFailAlloc_1044_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1044_, 0, v_fst_1026_);
lean_ctor_set(v_reuseFailAlloc_1044_, 1, v___x_1041_);
v___x_1043_ = v_reuseFailAlloc_1044_;
goto v_reusejp_1042_;
}
v_reusejp_1042_:
{
return v___x_1043_;
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
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___redArg(lean_object* v___x_1053_, lean_object* v___x_1054_, lean_object* v_as_x27_1055_, lean_object* v_b_1056_){
_start:
{
if (lean_obj_tag(v_as_x27_1055_) == 0)
{
lean_dec_ref(v___x_1054_);
return v_b_1056_;
}
else
{
lean_object* v_head_1057_; lean_object* v_tail_1058_; lean_object* v_fst_1059_; lean_object* v_snd_1060_; lean_object* v___x_1062_; uint8_t v_isShared_1063_; uint8_t v_isSharedCheck_1081_; 
v_head_1057_ = lean_ctor_get(v_as_x27_1055_, 0);
v_tail_1058_ = lean_ctor_get(v_as_x27_1055_, 1);
v_fst_1059_ = lean_ctor_get(v_b_1056_, 0);
v_snd_1060_ = lean_ctor_get(v_b_1056_, 1);
v_isSharedCheck_1081_ = !lean_is_exclusive(v_b_1056_);
if (v_isSharedCheck_1081_ == 0)
{
v___x_1062_ = v_b_1056_;
v_isShared_1063_ = v_isSharedCheck_1081_;
goto v_resetjp_1061_;
}
else
{
lean_inc(v_snd_1060_);
lean_inc(v_fst_1059_);
lean_dec(v_b_1056_);
v___x_1062_ = lean_box(0);
v_isShared_1063_ = v_isSharedCheck_1081_;
goto v_resetjp_1061_;
}
v_resetjp_1061_:
{
lean_object* v___x_1064_; lean_object* v___x_1065_; lean_object* v___x_1066_; lean_object* v_fst_1067_; lean_object* v_snd_1068_; lean_object* v___x_1070_; uint8_t v_isShared_1071_; uint8_t v_isSharedCheck_1080_; 
v___x_1064_ = l_Lean_instInhabitedExpr;
v___x_1065_ = lean_array_get_borrowed(v___x_1064_, v___x_1053_, v_head_1057_);
lean_inc(v___x_1065_);
lean_inc_ref(v___x_1054_);
v___x_1066_ = l_StmtKeys_hx(v___x_1054_, v___x_1065_, v_snd_1060_);
v_fst_1067_ = lean_ctor_get(v___x_1066_, 0);
v_snd_1068_ = lean_ctor_get(v___x_1066_, 1);
v_isSharedCheck_1080_ = !lean_is_exclusive(v___x_1066_);
if (v_isSharedCheck_1080_ == 0)
{
v___x_1070_ = v___x_1066_;
v_isShared_1071_ = v_isSharedCheck_1080_;
goto v_resetjp_1069_;
}
else
{
lean_inc(v_snd_1068_);
lean_inc(v_fst_1067_);
lean_dec(v___x_1066_);
v___x_1070_ = lean_box(0);
v_isShared_1071_ = v_isSharedCheck_1080_;
goto v_resetjp_1069_;
}
v_resetjp_1069_:
{
lean_object* v___x_1073_; 
lean_inc(v_head_1057_);
if (v_isShared_1071_ == 0)
{
lean_ctor_set(v___x_1070_, 1, v_head_1057_);
v___x_1073_ = v___x_1070_;
goto v_reusejp_1072_;
}
else
{
lean_object* v_reuseFailAlloc_1079_; 
v_reuseFailAlloc_1079_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1079_, 0, v_fst_1067_);
lean_ctor_set(v_reuseFailAlloc_1079_, 1, v_head_1057_);
v___x_1073_ = v_reuseFailAlloc_1079_;
goto v_reusejp_1072_;
}
v_reusejp_1072_:
{
lean_object* v___x_1074_; lean_object* v___x_1076_; 
v___x_1074_ = lean_array_push(v_fst_1059_, v___x_1073_);
if (v_isShared_1063_ == 0)
{
lean_ctor_set(v___x_1062_, 1, v_snd_1068_);
lean_ctor_set(v___x_1062_, 0, v___x_1074_);
v___x_1076_ = v___x_1062_;
goto v_reusejp_1075_;
}
else
{
lean_object* v_reuseFailAlloc_1078_; 
v_reuseFailAlloc_1078_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1078_, 0, v___x_1074_);
lean_ctor_set(v_reuseFailAlloc_1078_, 1, v_snd_1068_);
v___x_1076_ = v_reuseFailAlloc_1078_;
goto v_reusejp_1075_;
}
v_reusejp_1075_:
{
v_as_x27_1055_ = v_tail_1058_;
v_b_1056_ = v___x_1076_;
goto _start;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___redArg___boxed(lean_object* v___x_1082_, lean_object* v___x_1083_, lean_object* v_as_x27_1084_, lean_object* v_b_1085_){
_start:
{
lean_object* v_res_1086_; 
v_res_1086_ = l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___redArg(v___x_1082_, v___x_1083_, v_as_x27_1084_, v_b_1085_);
lean_dec(v_as_x27_1084_);
lean_dec_ref(v___x_1082_);
return v_res_1086_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___redArg(lean_object* v_hi_1087_, uint64_t v_pivot_1088_, lean_object* v_as_1089_, lean_object* v_i_1090_, lean_object* v_k_1091_){
_start:
{
uint8_t v___x_1092_; 
v___x_1092_ = lean_nat_dec_lt(v_k_1091_, v_hi_1087_);
if (v___x_1092_ == 0)
{
lean_object* v___x_1093_; lean_object* v___x_1094_; 
lean_dec(v_k_1091_);
v___x_1093_ = lean_array_fswap(v_as_1089_, v_i_1090_, v_hi_1087_);
v___x_1094_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1094_, 0, v_i_1090_);
lean_ctor_set(v___x_1094_, 1, v___x_1093_);
return v___x_1094_;
}
else
{
lean_object* v___x_1095_; uint64_t v___x_1096_; uint8_t v___x_1097_; 
v___x_1095_ = lean_array_fget_borrowed(v_as_1089_, v_k_1091_);
v___x_1096_ = lean_unbox_uint64(v___x_1095_);
v___x_1097_ = lean_uint64_dec_lt(v___x_1096_, v_pivot_1088_);
if (v___x_1097_ == 0)
{
lean_object* v___x_1098_; lean_object* v___x_1099_; 
v___x_1098_ = lean_unsigned_to_nat(1u);
v___x_1099_ = lean_nat_add(v_k_1091_, v___x_1098_);
lean_dec(v_k_1091_);
v_k_1091_ = v___x_1099_;
goto _start;
}
else
{
lean_object* v___x_1101_; lean_object* v___x_1102_; lean_object* v___x_1103_; lean_object* v___x_1104_; 
v___x_1101_ = lean_array_fswap(v_as_1089_, v_i_1090_, v_k_1091_);
v___x_1102_ = lean_unsigned_to_nat(1u);
v___x_1103_ = lean_nat_add(v_i_1090_, v___x_1102_);
lean_dec(v_i_1090_);
v___x_1104_ = lean_nat_add(v_k_1091_, v___x_1102_);
lean_dec(v_k_1091_);
v_as_1089_ = v___x_1101_;
v_i_1090_ = v___x_1103_;
v_k_1091_ = v___x_1104_;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___redArg___boxed(lean_object* v_hi_1106_, lean_object* v_pivot_1107_, lean_object* v_as_1108_, lean_object* v_i_1109_, lean_object* v_k_1110_){
_start:
{
uint64_t v_pivot_boxed_1111_; lean_object* v_res_1112_; 
v_pivot_boxed_1111_ = lean_unbox_uint64(v_pivot_1107_);
lean_dec_ref(v_pivot_1107_);
v_res_1112_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___redArg(v_hi_1106_, v_pivot_boxed_1111_, v_as_1108_, v_i_1109_, v_k_1110_);
lean_dec(v_hi_1106_);
return v_res_1112_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg(lean_object* v_n_1113_, lean_object* v_as_1114_, lean_object* v_lo_1115_, lean_object* v_hi_1116_){
_start:
{
lean_object* v___y_1118_; uint8_t v___x_1129_; 
v___x_1129_ = lean_nat_dec_lt(v_lo_1115_, v_hi_1116_);
if (v___x_1129_ == 0)
{
lean_dec(v_lo_1115_);
return v_as_1114_;
}
else
{
lean_object* v___x_1130_; lean_object* v___x_1131_; lean_object* v_mid_1132_; lean_object* v___y_1134_; lean_object* v___y_1142_; lean_object* v___x_1149_; lean_object* v___x_1150_; uint64_t v___x_1151_; uint64_t v___x_1152_; uint8_t v___x_1153_; 
v___x_1130_ = lean_nat_add(v_lo_1115_, v_hi_1116_);
v___x_1131_ = lean_unsigned_to_nat(1u);
v_mid_1132_ = lean_nat_shiftr(v___x_1130_, v___x_1131_);
lean_dec(v___x_1130_);
v___x_1149_ = lean_array_fget_borrowed(v_as_1114_, v_mid_1132_);
v___x_1150_ = lean_array_fget_borrowed(v_as_1114_, v_lo_1115_);
v___x_1151_ = lean_unbox_uint64(v___x_1149_);
v___x_1152_ = lean_unbox_uint64(v___x_1150_);
v___x_1153_ = lean_uint64_dec_lt(v___x_1151_, v___x_1152_);
if (v___x_1153_ == 0)
{
v___y_1142_ = v_as_1114_;
goto v___jp_1141_;
}
else
{
lean_object* v___x_1154_; 
v___x_1154_ = lean_array_fswap(v_as_1114_, v_lo_1115_, v_mid_1132_);
v___y_1142_ = v___x_1154_;
goto v___jp_1141_;
}
v___jp_1133_:
{
lean_object* v___x_1135_; lean_object* v___x_1136_; uint64_t v___x_1137_; uint64_t v___x_1138_; uint8_t v___x_1139_; 
v___x_1135_ = lean_array_fget_borrowed(v___y_1134_, v_mid_1132_);
v___x_1136_ = lean_array_fget_borrowed(v___y_1134_, v_hi_1116_);
v___x_1137_ = lean_unbox_uint64(v___x_1135_);
v___x_1138_ = lean_unbox_uint64(v___x_1136_);
v___x_1139_ = lean_uint64_dec_lt(v___x_1137_, v___x_1138_);
if (v___x_1139_ == 0)
{
lean_dec(v_mid_1132_);
v___y_1118_ = v___y_1134_;
goto v___jp_1117_;
}
else
{
lean_object* v___x_1140_; 
v___x_1140_ = lean_array_fswap(v___y_1134_, v_mid_1132_, v_hi_1116_);
lean_dec(v_mid_1132_);
v___y_1118_ = v___x_1140_;
goto v___jp_1117_;
}
}
v___jp_1141_:
{
lean_object* v___x_1143_; lean_object* v___x_1144_; uint64_t v___x_1145_; uint64_t v___x_1146_; uint8_t v___x_1147_; 
v___x_1143_ = lean_array_fget_borrowed(v___y_1142_, v_hi_1116_);
v___x_1144_ = lean_array_fget_borrowed(v___y_1142_, v_lo_1115_);
v___x_1145_ = lean_unbox_uint64(v___x_1143_);
v___x_1146_ = lean_unbox_uint64(v___x_1144_);
v___x_1147_ = lean_uint64_dec_lt(v___x_1145_, v___x_1146_);
if (v___x_1147_ == 0)
{
v___y_1134_ = v___y_1142_;
goto v___jp_1133_;
}
else
{
lean_object* v___x_1148_; 
v___x_1148_ = lean_array_fswap(v___y_1142_, v_lo_1115_, v_hi_1116_);
v___y_1134_ = v___x_1148_;
goto v___jp_1133_;
}
}
}
v___jp_1117_:
{
lean_object* v_pivot_1119_; uint64_t v___x_1120_; lean_object* v___x_1121_; lean_object* v_fst_1122_; lean_object* v_snd_1123_; uint8_t v___x_1124_; 
v_pivot_1119_ = lean_array_fget_borrowed(v___y_1118_, v_hi_1116_);
v___x_1120_ = lean_unbox_uint64(v_pivot_1119_);
lean_inc_n(v_lo_1115_, 2);
v___x_1121_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___redArg(v_hi_1116_, v___x_1120_, v___y_1118_, v_lo_1115_, v_lo_1115_);
v_fst_1122_ = lean_ctor_get(v___x_1121_, 0);
lean_inc(v_fst_1122_);
v_snd_1123_ = lean_ctor_get(v___x_1121_, 1);
lean_inc(v_snd_1123_);
lean_dec_ref(v___x_1121_);
v___x_1124_ = lean_nat_dec_le(v_hi_1116_, v_fst_1122_);
if (v___x_1124_ == 0)
{
lean_object* v___x_1125_; lean_object* v___x_1126_; lean_object* v___x_1127_; 
v___x_1125_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg(v_n_1113_, v_snd_1123_, v_lo_1115_, v_fst_1122_);
v___x_1126_ = lean_unsigned_to_nat(1u);
v___x_1127_ = lean_nat_add(v_fst_1122_, v___x_1126_);
lean_dec(v_fst_1122_);
v_as_1114_ = v___x_1125_;
v_lo_1115_ = v___x_1127_;
goto _start;
}
else
{
lean_dec(v_fst_1122_);
lean_dec(v_lo_1115_);
return v_snd_1123_;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg___boxed(lean_object* v_n_1155_, lean_object* v_as_1156_, lean_object* v_lo_1157_, lean_object* v_hi_1158_){
_start:
{
lean_object* v_res_1159_; 
v_res_1159_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg(v_n_1155_, v_as_1156_, v_lo_1157_, v_hi_1158_);
lean_dec(v_hi_1158_);
lean_dec(v_n_1155_);
return v_res_1159_;
}
}
LEAN_EXPORT uint64_t l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__12(lean_object* v_as_1160_, size_t v_sz_1161_, size_t v_i_1162_, uint64_t v_b_1163_){
_start:
{
uint8_t v___x_1164_; 
v___x_1164_ = lean_usize_dec_lt(v_i_1162_, v_sz_1161_);
if (v___x_1164_ == 0)
{
return v_b_1163_;
}
else
{
lean_object* v_a_1165_; uint64_t v___x_1166_; uint64_t v___x_1167_; uint64_t v___x_1168_; uint64_t v___x_1169_; size_t v___x_1170_; size_t v___x_1171_; 
v_a_1165_ = lean_array_uget_borrowed(v_as_1160_, v_i_1162_);
v___x_1166_ = 103ULL;
v___x_1167_ = lean_unbox_uint64(v_a_1165_);
v___x_1168_ = lean_uint64_mix_hash(v___x_1166_, v___x_1167_);
v___x_1169_ = lean_uint64_mix_hash(v_b_1163_, v___x_1168_);
v___x_1170_ = ((size_t)1ULL);
v___x_1171_ = lean_usize_add(v_i_1162_, v___x_1170_);
v_i_1162_ = v___x_1171_;
v_b_1163_ = v___x_1169_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__12___boxed(lean_object* v_as_1173_, lean_object* v_sz_1174_, lean_object* v_i_1175_, lean_object* v_b_1176_){
_start:
{
size_t v_sz_boxed_1177_; size_t v_i_boxed_1178_; uint64_t v_b_boxed_1179_; uint64_t v_res_1180_; lean_object* v_r_1181_; 
v_sz_boxed_1177_ = lean_unbox_usize(v_sz_1174_);
lean_dec(v_sz_1174_);
v_i_boxed_1178_ = lean_unbox_usize(v_i_1175_);
lean_dec(v_i_1175_);
v_b_boxed_1179_ = lean_unbox_uint64(v_b_1176_);
lean_dec_ref(v_b_1176_);
v_res_1180_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__12(v_as_1173_, v_sz_boxed_1177_, v_i_boxed_1178_, v_b_boxed_1179_);
lean_dec_ref(v_as_1173_);
v_r_1181_ = lean_box_uint64(v_res_1180_);
return v_r_1181_;
}
}
LEAN_EXPORT lean_object* l_List_filterTR_loop___at___00StmtKeys_permKey_spec__6(lean_object* v___x_1182_, lean_object* v_a_1183_, lean_object* v_a_1184_){
_start:
{
if (lean_obj_tag(v_a_1183_) == 0)
{
lean_object* v___x_1185_; 
v___x_1185_ = l_List_reverse___redArg(v_a_1184_);
return v___x_1185_;
}
else
{
lean_object* v_head_1186_; lean_object* v_tail_1187_; lean_object* v___x_1189_; uint8_t v_isShared_1190_; uint8_t v_isSharedCheck_1200_; 
v_head_1186_ = lean_ctor_get(v_a_1183_, 0);
v_tail_1187_ = lean_ctor_get(v_a_1183_, 1);
v_isSharedCheck_1200_ = !lean_is_exclusive(v_a_1183_);
if (v_isSharedCheck_1200_ == 0)
{
v___x_1189_ = v_a_1183_;
v_isShared_1190_ = v_isSharedCheck_1200_;
goto v_resetjp_1188_;
}
else
{
lean_inc(v_tail_1187_);
lean_inc(v_head_1186_);
lean_dec(v_a_1183_);
v___x_1189_ = lean_box(0);
v_isShared_1190_ = v_isSharedCheck_1200_;
goto v_resetjp_1188_;
}
v_resetjp_1188_:
{
uint8_t v___x_1191_; lean_object* v___x_1192_; lean_object* v___x_1193_; uint8_t v___x_1194_; 
v___x_1191_ = 0;
v___x_1192_ = lean_box(v___x_1191_);
v___x_1193_ = lean_array_get(v___x_1192_, v___x_1182_, v_head_1186_);
lean_dec(v___x_1192_);
v___x_1194_ = lean_unbox(v___x_1193_);
lean_dec(v___x_1193_);
if (v___x_1194_ == 0)
{
lean_object* v___x_1196_; 
if (v_isShared_1190_ == 0)
{
lean_ctor_set(v___x_1189_, 1, v_a_1184_);
v___x_1196_ = v___x_1189_;
goto v_reusejp_1195_;
}
else
{
lean_object* v_reuseFailAlloc_1198_; 
v_reuseFailAlloc_1198_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1198_, 0, v_head_1186_);
lean_ctor_set(v_reuseFailAlloc_1198_, 1, v_a_1184_);
v___x_1196_ = v_reuseFailAlloc_1198_;
goto v_reusejp_1195_;
}
v_reusejp_1195_:
{
v_a_1183_ = v_tail_1187_;
v_a_1184_ = v___x_1196_;
goto _start;
}
}
else
{
lean_del_object(v___x_1189_);
lean_dec(v_head_1186_);
v_a_1183_ = v_tail_1187_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_filterTR_loop___at___00StmtKeys_permKey_spec__6___boxed(lean_object* v___x_1201_, lean_object* v_a_1202_, lean_object* v_a_1203_){
_start:
{
lean_object* v_res_1204_; 
v_res_1204_ = l_List_filterTR_loop___at___00StmtKeys_permKey_spec__6(v___x_1201_, v_a_1202_, v_a_1203_);
lean_dec_ref(v___x_1201_);
return v_res_1204_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__9(lean_object* v___x_1205_, lean_object* v_as_1206_, size_t v_sz_1207_, size_t v_i_1208_, lean_object* v_b_1209_){
_start:
{
uint8_t v___x_1210_; 
v___x_1210_ = lean_usize_dec_lt(v_i_1208_, v_sz_1207_);
if (v___x_1210_ == 0)
{
return v_b_1209_;
}
else
{
lean_object* v_a_1211_; lean_object* v_snd_1212_; lean_object* v_fst_1213_; lean_object* v_snd_1214_; lean_object* v___x_1216_; uint8_t v_isShared_1217_; uint8_t v_isSharedCheck_1238_; 
v_a_1211_ = lean_array_uget_borrowed(v_as_1206_, v_i_1208_);
v_snd_1212_ = lean_ctor_get(v_a_1211_, 1);
v_fst_1213_ = lean_ctor_get(v_b_1209_, 0);
v_snd_1214_ = lean_ctor_get(v_b_1209_, 1);
v_isSharedCheck_1238_ = !lean_is_exclusive(v_b_1209_);
if (v_isSharedCheck_1238_ == 0)
{
v___x_1216_ = v_b_1209_;
v_isShared_1217_ = v_isSharedCheck_1238_;
goto v_resetjp_1215_;
}
else
{
lean_inc(v_snd_1214_);
lean_inc(v_fst_1213_);
lean_dec(v_b_1209_);
v___x_1216_ = lean_box(0);
v_isShared_1217_ = v_isSharedCheck_1238_;
goto v_resetjp_1215_;
}
v_resetjp_1215_:
{
lean_object* v___x_1218_; lean_object* v___x_1219_; lean_object* v___x_1221_; 
v___x_1218_ = lean_obj_once(&l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0, &l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0_once, _init_l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg___closed__0);
v___x_1219_ = lean_array_get_borrowed(v___x_1218_, v___x_1205_, v_snd_1212_);
if (v_isShared_1217_ == 0)
{
v___x_1221_ = v___x_1216_;
goto v_reusejp_1220_;
}
else
{
lean_object* v_reuseFailAlloc_1237_; 
v_reuseFailAlloc_1237_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1237_, 0, v_fst_1213_);
lean_ctor_set(v_reuseFailAlloc_1237_, 1, v_snd_1214_);
v___x_1221_ = v_reuseFailAlloc_1237_;
goto v_reusejp_1220_;
}
v_reusejp_1220_:
{
size_t v_sz_1222_; size_t v___x_1223_; lean_object* v___x_1224_; lean_object* v_fst_1225_; lean_object* v_snd_1226_; lean_object* v___x_1228_; uint8_t v_isShared_1229_; uint8_t v_isSharedCheck_1236_; 
v_sz_1222_ = lean_array_size(v___x_1219_);
v___x_1223_ = ((size_t)0ULL);
v___x_1224_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__2(v___x_1219_, v_sz_1222_, v___x_1223_, v___x_1221_);
v_fst_1225_ = lean_ctor_get(v___x_1224_, 0);
v_snd_1226_ = lean_ctor_get(v___x_1224_, 1);
v_isSharedCheck_1236_ = !lean_is_exclusive(v___x_1224_);
if (v_isSharedCheck_1236_ == 0)
{
v___x_1228_ = v___x_1224_;
v_isShared_1229_ = v_isSharedCheck_1236_;
goto v_resetjp_1227_;
}
else
{
lean_inc(v_snd_1226_);
lean_inc(v_fst_1225_);
lean_dec(v___x_1224_);
v___x_1228_ = lean_box(0);
v_isShared_1229_ = v_isSharedCheck_1236_;
goto v_resetjp_1227_;
}
v_resetjp_1227_:
{
lean_object* v___x_1231_; 
if (v_isShared_1229_ == 0)
{
v___x_1231_ = v___x_1228_;
goto v_reusejp_1230_;
}
else
{
lean_object* v_reuseFailAlloc_1235_; 
v_reuseFailAlloc_1235_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1235_, 0, v_fst_1225_);
lean_ctor_set(v_reuseFailAlloc_1235_, 1, v_snd_1226_);
v___x_1231_ = v_reuseFailAlloc_1235_;
goto v_reusejp_1230_;
}
v_reusejp_1230_:
{
size_t v___x_1232_; size_t v___x_1233_; 
v___x_1232_ = ((size_t)1ULL);
v___x_1233_ = lean_usize_add(v_i_1208_, v___x_1232_);
v_i_1208_ = v___x_1233_;
v_b_1209_ = v___x_1231_;
goto _start;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__9___boxed(lean_object* v___x_1239_, lean_object* v_as_1240_, lean_object* v_sz_1241_, lean_object* v_i_1242_, lean_object* v_b_1243_){
_start:
{
size_t v_sz_boxed_1244_; size_t v_i_boxed_1245_; lean_object* v_res_1246_; 
v_sz_boxed_1244_ = lean_unbox_usize(v_sz_1241_);
lean_dec(v_sz_1241_);
v_i_boxed_1245_ = lean_unbox_usize(v_i_1242_);
lean_dec(v_i_1242_);
v_res_1246_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__9(v___x_1239_, v_as_1240_, v_sz_boxed_1244_, v_i_boxed_1245_, v_b_1243_);
lean_dec_ref(v_as_1240_);
lean_dec_ref(v___x_1239_);
return v_res_1246_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_permKey_spec__1(size_t v_sz_1247_, size_t v_i_1248_, lean_object* v_bs_1249_){
_start:
{
uint8_t v___x_1250_; 
v___x_1250_ = lean_usize_dec_lt(v_i_1248_, v_sz_1247_);
if (v___x_1250_ == 0)
{
return v_bs_1249_;
}
else
{
lean_object* v_v_1251_; lean_object* v___x_1252_; lean_object* v_bs_x27_1253_; lean_object* v___x_1254_; size_t v___x_1255_; size_t v___x_1256_; lean_object* v___x_1257_; 
v_v_1251_ = lean_array_uget(v_bs_1249_, v_i_1248_);
v___x_1252_ = lean_unsigned_to_nat(0u);
v_bs_x27_1253_ = lean_array_uset(v_bs_1249_, v_i_1248_, v___x_1252_);
v___x_1254_ = l_StmtKeys_fvarsOf(v_v_1251_);
v___x_1255_ = ((size_t)1ULL);
v___x_1256_ = lean_usize_add(v_i_1248_, v___x_1255_);
v___x_1257_ = lean_array_uset(v_bs_x27_1253_, v_i_1248_, v___x_1254_);
v_i_1248_ = v___x_1256_;
v_bs_1249_ = v___x_1257_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_permKey_spec__1___boxed(lean_object* v_sz_1259_, lean_object* v_i_1260_, lean_object* v_bs_1261_){
_start:
{
size_t v_sz_boxed_1262_; size_t v_i_boxed_1263_; lean_object* v_res_1264_; 
v_sz_boxed_1262_ = lean_unbox_usize(v_sz_1259_);
lean_dec(v_sz_1259_);
v_i_boxed_1263_ = lean_unbox_usize(v_i_1260_);
lean_dec(v_i_1260_);
v_res_1264_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_permKey_spec__1(v_sz_boxed_1262_, v_i_boxed_1263_, v_bs_1261_);
return v_res_1264_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_permKey(lean_object* v_o_1267_, lean_object* v_isProj_1268_, lean_object* v_ty_1269_){
_start:
{
lean_object* v___x_1270_; lean_object* v_tys_1271_; lean_object* v___x_1272_; lean_object* v___x_1273_; lean_object* v___x_1274_; lean_object* v___x_1275_; lean_object* v_snd_1276_; lean_object* v_snd_1277_; lean_object* v_fst_1278_; lean_object* v___x_1280_; uint8_t v_isShared_1281_; uint8_t v_isSharedCheck_1453_; 
v___x_1270_ = lean_unsigned_to_nat(0u);
v_tys_1271_ = ((lean_object*)(l_StmtKeys_permKey___closed__0));
v___x_1272_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1272_, 0, v_ty_1269_);
lean_ctor_set(v___x_1272_, 1, v___x_1270_);
v___x_1273_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1273_, 0, v_tys_1271_);
lean_ctor_set(v___x_1273_, 1, v___x_1272_);
v___x_1274_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1274_, 0, v_tys_1271_);
lean_ctor_set(v___x_1274_, 1, v___x_1273_);
v___x_1275_ = l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__0___redArg(v___x_1274_);
v_snd_1276_ = lean_ctor_get(v___x_1275_, 1);
lean_inc(v_snd_1276_);
v_snd_1277_ = lean_ctor_get(v_snd_1276_, 1);
lean_inc(v_snd_1277_);
v_fst_1278_ = lean_ctor_get(v___x_1275_, 0);
v_isSharedCheck_1453_ = !lean_is_exclusive(v___x_1275_);
if (v_isSharedCheck_1453_ == 0)
{
lean_object* v_unused_1454_; 
v_unused_1454_ = lean_ctor_get(v___x_1275_, 1);
lean_dec(v_unused_1454_);
v___x_1280_ = v___x_1275_;
v_isShared_1281_ = v_isSharedCheck_1453_;
goto v_resetjp_1279_;
}
else
{
lean_inc(v_fst_1278_);
lean_dec(v___x_1275_);
v___x_1280_ = lean_box(0);
v_isShared_1281_ = v_isSharedCheck_1453_;
goto v_resetjp_1279_;
}
v_resetjp_1279_:
{
lean_object* v_fst_1282_; lean_object* v___x_1284_; uint8_t v_isShared_1285_; uint8_t v_isSharedCheck_1451_; 
v_fst_1282_ = lean_ctor_get(v_snd_1276_, 0);
v_isSharedCheck_1451_ = !lean_is_exclusive(v_snd_1276_);
if (v_isSharedCheck_1451_ == 0)
{
lean_object* v_unused_1452_; 
v_unused_1452_ = lean_ctor_get(v_snd_1276_, 1);
lean_dec(v_unused_1452_);
v___x_1284_ = v_snd_1276_;
v_isShared_1285_ = v_isSharedCheck_1451_;
goto v_resetjp_1283_;
}
else
{
lean_inc(v_fst_1282_);
lean_dec(v_snd_1276_);
v___x_1284_ = lean_box(0);
v_isShared_1285_ = v_isSharedCheck_1451_;
goto v_resetjp_1283_;
}
v_resetjp_1283_:
{
lean_object* v_fst_1286_; lean_object* v___x_1288_; uint8_t v_isShared_1289_; uint8_t v_isSharedCheck_1449_; 
v_fst_1286_ = lean_ctor_get(v_snd_1277_, 0);
v_isSharedCheck_1449_ = !lean_is_exclusive(v_snd_1277_);
if (v_isSharedCheck_1449_ == 0)
{
lean_object* v_unused_1450_; 
v_unused_1450_ = lean_ctor_get(v_snd_1277_, 1);
lean_dec(v_unused_1450_);
v___x_1288_ = v_snd_1277_;
v_isShared_1289_ = v_isSharedCheck_1449_;
goto v_resetjp_1287_;
}
else
{
lean_inc(v_fst_1286_);
lean_dec(v_snd_1277_);
v___x_1288_ = lean_box(0);
v_isShared_1289_ = v_isSharedCheck_1449_;
goto v_resetjp_1287_;
}
v_resetjp_1287_:
{
lean_object* v___x_1290_; lean_object* v___x_1291_; size_t v_sz_1292_; size_t v___x_1293_; lean_object* v___x_1294_; lean_object* v___x_1295_; uint8_t v___x_1296_; lean_object* v___x_1297_; lean_object* v___x_1298_; size_t v_sz_1299_; lean_object* v___x_1300_; lean_object* v___x_1302_; 
v___x_1290_ = lean_expr_instantiate_rev(v_fst_1286_, v_fst_1282_);
lean_dec(v_fst_1282_);
lean_dec(v_fst_1286_);
v___x_1291_ = lean_array_get_size(v_fst_1278_);
v_sz_1292_ = lean_array_size(v_fst_1278_);
v___x_1293_ = ((size_t)0ULL);
lean_inc(v_fst_1278_);
v___x_1294_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_permKey_spec__1(v_sz_1292_, v___x_1293_, v_fst_1278_);
lean_inc_ref(v___x_1290_);
v___x_1295_ = l_StmtKeys_fvarsOf(v___x_1290_);
v___x_1296_ = 0;
v___x_1297_ = lean_box(v___x_1296_);
v___x_1298_ = lean_mk_array(v___x_1291_, v___x_1297_);
v_sz_1299_ = lean_array_size(v___x_1295_);
lean_inc_ref(v___x_1298_);
v___x_1300_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__3(v___x_1295_, v_sz_1299_, v___x_1293_, v___x_1298_);
if (v_isShared_1289_ == 0)
{
lean_ctor_set(v___x_1288_, 1, v___x_1298_);
lean_ctor_set(v___x_1288_, 0, v_tys_1271_);
v___x_1302_ = v___x_1288_;
goto v_reusejp_1301_;
}
else
{
lean_object* v_reuseFailAlloc_1448_; 
v_reuseFailAlloc_1448_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1448_, 0, v_tys_1271_);
lean_ctor_set(v_reuseFailAlloc_1448_, 1, v___x_1298_);
v___x_1302_ = v_reuseFailAlloc_1448_;
goto v_reusejp_1301_;
}
v_reusejp_1301_:
{
lean_object* v___x_1303_; lean_object* v_fst_1304_; lean_object* v_snd_1305_; lean_object* v___x_1307_; uint8_t v_isShared_1308_; uint8_t v_isSharedCheck_1447_; 
v___x_1303_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__7(v___x_1295_, v_sz_1299_, v___x_1293_, v___x_1302_);
lean_dec_ref(v___x_1295_);
v_fst_1304_ = lean_ctor_get(v___x_1303_, 0);
v_snd_1305_ = lean_ctor_get(v___x_1303_, 1);
v_isSharedCheck_1447_ = !lean_is_exclusive(v___x_1303_);
if (v_isSharedCheck_1447_ == 0)
{
v___x_1307_ = v___x_1303_;
v_isShared_1308_ = v_isSharedCheck_1447_;
goto v_resetjp_1306_;
}
else
{
lean_inc(v_snd_1305_);
lean_inc(v_fst_1304_);
lean_dec(v___x_1303_);
v___x_1307_ = lean_box(0);
v_isShared_1308_ = v_isSharedCheck_1447_;
goto v_resetjp_1306_;
}
v_resetjp_1306_:
{
lean_object* v___x_1309_; lean_object* v___x_1310_; lean_object* v___x_1311_; lean_object* v___x_1313_; 
v___x_1309_ = lean_unsigned_to_nat(1u);
v___x_1310_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_1310_, 0, v___x_1270_);
lean_ctor_set(v___x_1310_, 1, v___x_1291_);
lean_ctor_set(v___x_1310_, 2, v___x_1309_);
v___x_1311_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___redArg(v___x_1294_, v___x_1310_, v___x_1300_, v___x_1270_);
if (v_isShared_1308_ == 0)
{
lean_ctor_set(v___x_1307_, 1, v___x_1270_);
lean_ctor_set(v___x_1307_, 0, v_snd_1305_);
v___x_1313_ = v___x_1307_;
goto v_reusejp_1312_;
}
else
{
lean_object* v_reuseFailAlloc_1446_; 
v_reuseFailAlloc_1446_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1446_, 0, v_snd_1305_);
lean_ctor_set(v_reuseFailAlloc_1446_, 1, v___x_1270_);
v___x_1313_ = v_reuseFailAlloc_1446_;
goto v_reusejp_1312_;
}
v_reusejp_1312_:
{
lean_object* v___x_1315_; 
if (v_isShared_1285_ == 0)
{
lean_ctor_set(v___x_1284_, 1, v___x_1313_);
lean_ctor_set(v___x_1284_, 0, v_fst_1304_);
v___x_1315_ = v___x_1284_;
goto v_reusejp_1314_;
}
else
{
lean_object* v_reuseFailAlloc_1445_; 
v_reuseFailAlloc_1445_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1445_, 0, v_fst_1304_);
lean_ctor_set(v_reuseFailAlloc_1445_, 1, v___x_1313_);
v___x_1315_ = v_reuseFailAlloc_1445_;
goto v_reusejp_1314_;
}
v_reusejp_1314_:
{
lean_object* v___x_1316_; lean_object* v_snd_1317_; lean_object* v_fst_1318_; lean_object* v___x_1320_; uint8_t v_isShared_1321_; uint8_t v_isSharedCheck_1444_; 
v___x_1316_ = l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg(v___x_1294_, v___x_1315_);
v_snd_1317_ = lean_ctor_get(v___x_1316_, 1);
v_fst_1318_ = lean_ctor_get(v___x_1316_, 0);
v_isSharedCheck_1444_ = !lean_is_exclusive(v___x_1316_);
if (v_isSharedCheck_1444_ == 0)
{
v___x_1320_ = v___x_1316_;
v_isShared_1321_ = v_isSharedCheck_1444_;
goto v_resetjp_1319_;
}
else
{
lean_inc(v_snd_1317_);
lean_inc(v_fst_1318_);
lean_dec(v___x_1316_);
v___x_1320_ = lean_box(0);
v_isShared_1321_ = v_isSharedCheck_1444_;
goto v_resetjp_1319_;
}
v_resetjp_1319_:
{
lean_object* v_fst_1322_; lean_object* v_snd_1323_; lean_object* v___x_1325_; uint8_t v_isShared_1326_; uint8_t v_isSharedCheck_1443_; 
v_fst_1322_ = lean_ctor_get(v_snd_1317_, 0);
v_snd_1323_ = lean_ctor_get(v_snd_1317_, 1);
v_isSharedCheck_1443_ = !lean_is_exclusive(v_snd_1317_);
if (v_isSharedCheck_1443_ == 0)
{
v___x_1325_ = v_snd_1317_;
v_isShared_1326_ = v_isSharedCheck_1443_;
goto v_resetjp_1324_;
}
else
{
lean_inc(v_snd_1323_);
lean_inc(v_fst_1322_);
lean_dec(v_snd_1317_);
v___x_1325_ = lean_box(0);
v_isShared_1326_ = v_isSharedCheck_1443_;
goto v_resetjp_1324_;
}
v_resetjp_1324_:
{
lean_object* v___f_1327_; lean_object* v___x_1328_; lean_object* v___x_1329_; lean_object* v___x_1330_; lean_object* v___y_1332_; lean_object* v___y_1333_; lean_object* v___y_1346_; lean_object* v___y_1347_; lean_object* v___y_1348_; lean_object* v___y_1349_; lean_object* v___y_1350_; lean_object* v___y_1353_; lean_object* v___y_1354_; lean_object* v___y_1355_; lean_object* v___y_1356_; lean_object* v___y_1357_; lean_object* v___x_1359_; lean_object* v___x_1360_; lean_object* v___y_1362_; lean_object* v___x_1427_; lean_object* v___x_1428_; lean_object* v___x_1429_; lean_object* v___x_1430_; lean_object* v_fst_1431_; lean_object* v___x_1432_; lean_object* v___y_1434_; lean_object* v___y_1435_; uint8_t v___x_1437_; 
v___f_1327_ = ((lean_object*)(l_StmtKeys_plainKey___closed__0));
v___x_1328_ = l_List_range(v___x_1291_);
v___x_1329_ = lean_box(0);
v___x_1330_ = l_List_filterTR_loop___at___00StmtKeys_permKey_spec__6(v___x_1311_, v___x_1328_, v___x_1329_);
lean_inc_ref(v_isProj_1268_);
lean_inc_ref(v_o_1267_);
v___x_1359_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_1359_, 0, v_o_1267_);
lean_ctor_set(v___x_1359_, 1, v_isProj_1268_);
lean_ctor_set(v___x_1359_, 2, v___f_1327_);
lean_ctor_set_uint8(v___x_1359_, sizeof(void*)*3, v___x_1296_);
v___x_1360_ = lean_obj_once(&l_StmtKeys_plainKey___closed__2, &l_StmtKeys_plainKey___closed__2_once, _init_l_StmtKeys_plainKey___closed__2);
v___x_1427_ = l_StmtKeys_permKey___lam__1(v___x_1270_, v___x_1309_, v_fst_1318_);
v___x_1428_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_1428_, 0, v___x_1360_);
lean_ctor_set(v___x_1428_, 1, v___x_1360_);
lean_ctor_set(v___x_1428_, 2, v_tys_1271_);
lean_ctor_set(v___x_1428_, 3, v___x_1427_);
v___x_1429_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1429_, 0, v_tys_1271_);
lean_ctor_set(v___x_1429_, 1, v___x_1428_);
v___x_1430_ = l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___redArg(v_fst_1278_, v___x_1359_, v___x_1330_, v___x_1429_);
v_fst_1431_ = lean_ctor_get(v___x_1430_, 0);
lean_inc(v_fst_1431_);
lean_dec_ref(v___x_1430_);
v___x_1432_ = lean_array_get_size(v_fst_1431_);
v___x_1437_ = lean_nat_dec_eq(v___x_1432_, v___x_1270_);
if (v___x_1437_ == 0)
{
lean_object* v___x_1438_; lean_object* v___y_1440_; uint8_t v___x_1442_; 
v___x_1438_ = lean_nat_sub(v___x_1432_, v___x_1309_);
v___x_1442_ = lean_nat_dec_le(v___x_1270_, v___x_1438_);
if (v___x_1442_ == 0)
{
lean_inc(v___x_1438_);
v___y_1440_ = v___x_1438_;
goto v___jp_1439_;
}
else
{
v___y_1440_ = v___x_1270_;
goto v___jp_1439_;
}
v___jp_1439_:
{
uint8_t v___x_1441_; 
v___x_1441_ = lean_nat_dec_le(v___y_1440_, v___x_1438_);
if (v___x_1441_ == 0)
{
lean_dec(v___x_1438_);
lean_inc(v___y_1440_);
v___y_1434_ = v___y_1440_;
v___y_1435_ = v___y_1440_;
goto v___jp_1433_;
}
else
{
v___y_1434_ = v___y_1440_;
v___y_1435_ = v___x_1438_;
goto v___jp_1433_;
}
}
}
else
{
v___y_1362_ = v_fst_1431_;
goto v___jp_1361_;
}
v___jp_1331_:
{
size_t v_sz_1334_; uint64_t v___x_1335_; uint64_t v___x_1336_; lean_object* v___x_1337_; lean_object* v___x_1339_; 
v_sz_1334_ = lean_array_size(v___y_1333_);
v___x_1335_ = lean_unbox_uint64(v___y_1332_);
lean_dec(v___y_1332_);
v___x_1336_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__12(v___y_1333_, v_sz_1334_, v___x_1293_, v___x_1335_);
lean_dec_ref(v___y_1333_);
v___x_1337_ = l_List_lengthTR___redArg(v___x_1330_);
lean_dec(v___x_1330_);
if (v_isShared_1326_ == 0)
{
lean_ctor_set(v___x_1325_, 1, v___x_1337_);
lean_ctor_set(v___x_1325_, 0, v___x_1291_);
v___x_1339_ = v___x_1325_;
goto v_reusejp_1338_;
}
else
{
lean_object* v_reuseFailAlloc_1344_; 
v_reuseFailAlloc_1344_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1344_, 0, v___x_1291_);
lean_ctor_set(v_reuseFailAlloc_1344_, 1, v___x_1337_);
v___x_1339_ = v_reuseFailAlloc_1344_;
goto v_reusejp_1338_;
}
v_reusejp_1338_:
{
lean_object* v___x_1340_; lean_object* v___x_1342_; 
v___x_1340_ = lean_box_uint64(v___x_1336_);
if (v_isShared_1321_ == 0)
{
lean_ctor_set(v___x_1320_, 1, v___x_1339_);
lean_ctor_set(v___x_1320_, 0, v___x_1340_);
v___x_1342_ = v___x_1320_;
goto v_reusejp_1341_;
}
else
{
lean_object* v_reuseFailAlloc_1343_; 
v_reuseFailAlloc_1343_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1343_, 0, v___x_1340_);
lean_ctor_set(v_reuseFailAlloc_1343_, 1, v___x_1339_);
v___x_1342_ = v_reuseFailAlloc_1343_;
goto v_reusejp_1341_;
}
v_reusejp_1341_:
{
return v___x_1342_;
}
}
}
v___jp_1345_:
{
lean_object* v___x_1351_; 
v___x_1351_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg(v___y_1349_, v___y_1347_, v___y_1348_, v___y_1350_);
lean_dec(v___y_1350_);
lean_dec(v___y_1349_);
v___y_1332_ = v___y_1346_;
v___y_1333_ = v___x_1351_;
goto v___jp_1331_;
}
v___jp_1352_:
{
uint8_t v___x_1358_; 
v___x_1358_ = lean_nat_dec_le(v___y_1357_, v___y_1353_);
if (v___x_1358_ == 0)
{
lean_dec(v___y_1353_);
lean_inc(v___y_1357_);
v___y_1346_ = v___y_1355_;
v___y_1347_ = v___y_1354_;
v___y_1348_ = v___y_1357_;
v___y_1349_ = v___y_1356_;
v___y_1350_ = v___y_1357_;
goto v___jp_1345_;
}
else
{
v___y_1346_ = v___y_1355_;
v___y_1347_ = v___y_1354_;
v___y_1348_ = v___y_1357_;
v___y_1349_ = v___y_1356_;
v___y_1350_ = v___y_1353_;
goto v___jp_1345_;
}
}
v___jp_1361_:
{
lean_object* v___x_1364_; 
if (v_isShared_1281_ == 0)
{
lean_ctor_set(v___x_1280_, 1, v_fst_1322_);
lean_ctor_set(v___x_1280_, 0, v_fst_1318_);
v___x_1364_ = v___x_1280_;
goto v_reusejp_1363_;
}
else
{
lean_object* v_reuseFailAlloc_1426_; 
v_reuseFailAlloc_1426_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1426_, 0, v_fst_1318_);
lean_ctor_set(v_reuseFailAlloc_1426_, 1, v_fst_1322_);
v___x_1364_ = v_reuseFailAlloc_1426_;
goto v_reusejp_1363_;
}
v_reusejp_1363_:
{
size_t v_sz_1365_; lean_object* v___x_1366_; lean_object* v_fst_1367_; lean_object* v_snd_1368_; lean_object* v___x_1370_; uint8_t v_isShared_1371_; uint8_t v_isSharedCheck_1425_; 
v_sz_1365_ = lean_array_size(v___y_1362_);
v___x_1366_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__9(v___x_1294_, v___y_1362_, v_sz_1365_, v___x_1293_, v___x_1364_);
v_fst_1367_ = lean_ctor_get(v___x_1366_, 0);
v_snd_1368_ = lean_ctor_get(v___x_1366_, 1);
v_isSharedCheck_1425_ = !lean_is_exclusive(v___x_1366_);
if (v_isSharedCheck_1425_ == 0)
{
v___x_1370_ = v___x_1366_;
v_isShared_1371_ = v_isSharedCheck_1425_;
goto v_resetjp_1369_;
}
else
{
lean_inc(v_snd_1368_);
lean_inc(v_fst_1367_);
lean_dec(v___x_1366_);
v___x_1370_ = lean_box(0);
v_isShared_1371_ = v_isSharedCheck_1425_;
goto v_resetjp_1369_;
}
v_resetjp_1369_:
{
lean_object* v___x_1373_; 
if (v_isShared_1371_ == 0)
{
lean_ctor_set(v___x_1370_, 1, v_snd_1323_);
lean_ctor_set(v___x_1370_, 0, v_snd_1368_);
v___x_1373_ = v___x_1370_;
goto v_reusejp_1372_;
}
else
{
lean_object* v_reuseFailAlloc_1424_; 
v_reuseFailAlloc_1424_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1424_, 0, v_snd_1368_);
lean_ctor_set(v_reuseFailAlloc_1424_, 1, v_snd_1323_);
v___x_1373_ = v_reuseFailAlloc_1424_;
goto v_reusejp_1372_;
}
v_reusejp_1372_:
{
lean_object* v___x_1374_; lean_object* v___x_1375_; lean_object* v_snd_1376_; lean_object* v_fst_1377_; lean_object* v_fst_1378_; lean_object* v___x_1380_; uint8_t v_isShared_1381_; uint8_t v_isSharedCheck_1422_; 
v___x_1374_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1374_, 0, v_fst_1367_);
lean_ctor_set(v___x_1374_, 1, v___x_1373_);
v___x_1375_ = l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg(v___x_1294_, v___x_1374_);
lean_dec_ref(v___x_1294_);
v_snd_1376_ = lean_ctor_get(v___x_1375_, 1);
lean_inc(v_snd_1376_);
v_fst_1377_ = lean_ctor_get(v___x_1375_, 0);
lean_inc(v_fst_1377_);
lean_dec_ref(v___x_1375_);
v_fst_1378_ = lean_ctor_get(v_snd_1376_, 0);
v_isSharedCheck_1422_ = !lean_is_exclusive(v_snd_1376_);
if (v_isSharedCheck_1422_ == 0)
{
lean_object* v_unused_1423_; 
v_unused_1423_ = lean_ctor_get(v_snd_1376_, 1);
lean_dec(v_unused_1423_);
v___x_1380_ = v_snd_1376_;
v_isShared_1381_ = v_isSharedCheck_1422_;
goto v_resetjp_1379_;
}
else
{
lean_inc(v_fst_1378_);
lean_dec(v_snd_1376_);
v___x_1380_ = lean_box(0);
v_isShared_1381_ = v_isSharedCheck_1422_;
goto v_resetjp_1379_;
}
v_resetjp_1379_:
{
lean_object* v___x_1383_; 
if (v_isShared_1381_ == 0)
{
lean_ctor_set(v___x_1380_, 1, v_fst_1378_);
lean_ctor_set(v___x_1380_, 0, v_fst_1377_);
v___x_1383_ = v___x_1380_;
goto v_reusejp_1382_;
}
else
{
lean_object* v_reuseFailAlloc_1421_; 
v_reuseFailAlloc_1421_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1421_, 0, v_fst_1377_);
lean_ctor_set(v_reuseFailAlloc_1421_, 1, v_fst_1378_);
v___x_1383_ = v_reuseFailAlloc_1421_;
goto v_reusejp_1382_;
}
v_reusejp_1382_:
{
lean_object* v___x_1384_; lean_object* v_fst_1385_; uint8_t v___x_1386_; lean_object* v___x_1387_; lean_object* v___x_1388_; lean_object* v___x_1389_; lean_object* v___x_1390_; lean_object* v_fst_1391_; lean_object* v_snd_1392_; lean_object* v___x_1394_; uint8_t v_isShared_1395_; uint8_t v_isSharedCheck_1420_; 
v___x_1384_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___redArg(v___x_1311_, v___x_1310_, v___x_1383_, v___x_1270_);
lean_dec_ref_known(v___x_1310_, 3);
lean_dec_ref(v___x_1311_);
v_fst_1385_ = lean_ctor_get(v___x_1384_, 0);
lean_inc(v_fst_1385_);
lean_dec_ref(v___x_1384_);
v___x_1386_ = 1;
v___x_1387_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_1387_, 0, v_o_1267_);
lean_ctor_set(v___x_1387_, 1, v_isProj_1268_);
lean_ctor_set(v___x_1387_, 2, v___f_1327_);
lean_ctor_set_uint8(v___x_1387_, sizeof(void*)*3, v___x_1386_);
v___x_1388_ = l_StmtKeys_permKey___lam__1(v___x_1270_, v___x_1309_, v_fst_1385_);
v___x_1389_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_1389_, 0, v___x_1360_);
lean_ctor_set(v___x_1389_, 1, v___x_1360_);
lean_ctor_set(v___x_1389_, 2, v_tys_1271_);
lean_ctor_set(v___x_1389_, 3, v___x_1388_);
lean_inc_ref(v___x_1387_);
v___x_1390_ = l_StmtKeys_hx(v___x_1387_, v___x_1290_, v___x_1389_);
v_fst_1391_ = lean_ctor_get(v___x_1390_, 0);
v_snd_1392_ = lean_ctor_get(v___x_1390_, 1);
v_isSharedCheck_1420_ = !lean_is_exclusive(v___x_1390_);
if (v_isSharedCheck_1420_ == 0)
{
v___x_1394_ = v___x_1390_;
v_isShared_1395_ = v_isSharedCheck_1420_;
goto v_resetjp_1393_;
}
else
{
lean_inc(v_snd_1392_);
lean_inc(v_fst_1391_);
lean_dec(v___x_1390_);
v___x_1394_ = lean_box(0);
v_isShared_1395_ = v_isSharedCheck_1420_;
goto v_resetjp_1393_;
}
v_resetjp_1393_:
{
uint64_t v___x_1396_; uint64_t v___x_1397_; uint64_t v___x_1398_; lean_object* v___x_1399_; lean_object* v___x_1401_; 
v___x_1396_ = 101ULL;
v___x_1397_ = lean_unbox_uint64(v_fst_1391_);
lean_dec(v_fst_1391_);
v___x_1398_ = lean_uint64_mix_hash(v___x_1396_, v___x_1397_);
v___x_1399_ = lean_box_uint64(v___x_1398_);
if (v_isShared_1395_ == 0)
{
lean_ctor_set(v___x_1394_, 1, v___x_1399_);
lean_ctor_set(v___x_1394_, 0, v_snd_1392_);
v___x_1401_ = v___x_1394_;
goto v_reusejp_1400_;
}
else
{
lean_object* v_reuseFailAlloc_1419_; 
v_reuseFailAlloc_1419_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1419_, 0, v_snd_1392_);
lean_ctor_set(v_reuseFailAlloc_1419_, 1, v___x_1399_);
v___x_1401_ = v_reuseFailAlloc_1419_;
goto v_reusejp_1400_;
}
v_reusejp_1400_:
{
size_t v_sz_1402_; lean_object* v___x_1403_; lean_object* v_fst_1404_; lean_object* v_snd_1405_; lean_object* v___x_1407_; uint8_t v_isShared_1408_; uint8_t v_isSharedCheck_1418_; 
v_sz_1402_ = lean_array_size(v_fst_1385_);
lean_inc_ref(v___x_1387_);
v___x_1403_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__11(v_fst_1278_, v___x_1387_, v_fst_1385_, v_sz_1402_, v___x_1293_, v___x_1401_);
lean_dec(v_fst_1385_);
v_fst_1404_ = lean_ctor_get(v___x_1403_, 0);
v_snd_1405_ = lean_ctor_get(v___x_1403_, 1);
v_isSharedCheck_1418_ = !lean_is_exclusive(v___x_1403_);
if (v_isSharedCheck_1418_ == 0)
{
v___x_1407_ = v___x_1403_;
v_isShared_1408_ = v_isSharedCheck_1418_;
goto v_resetjp_1406_;
}
else
{
lean_inc(v_snd_1405_);
lean_inc(v_fst_1404_);
lean_dec(v___x_1403_);
v___x_1407_ = lean_box(0);
v_isShared_1408_ = v_isSharedCheck_1418_;
goto v_resetjp_1406_;
}
v_resetjp_1406_:
{
lean_object* v___x_1410_; 
if (v_isShared_1408_ == 0)
{
lean_ctor_set(v___x_1407_, 1, v_tys_1271_);
v___x_1410_ = v___x_1407_;
goto v_reusejp_1409_;
}
else
{
lean_object* v_reuseFailAlloc_1417_; 
v_reuseFailAlloc_1417_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1417_, 0, v_fst_1404_);
lean_ctor_set(v_reuseFailAlloc_1417_, 1, v_tys_1271_);
v___x_1410_ = v_reuseFailAlloc_1417_;
goto v_reusejp_1409_;
}
v_reusejp_1409_:
{
lean_object* v___x_1411_; lean_object* v_snd_1412_; lean_object* v___x_1413_; uint8_t v___x_1414_; 
v___x_1411_ = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00StmtKeys_permKey_spec__13(v_fst_1278_, v___x_1387_, v___y_1362_, v_sz_1365_, v___x_1293_, v___x_1410_);
lean_dec_ref(v___y_1362_);
lean_dec(v_fst_1278_);
v_snd_1412_ = lean_ctor_get(v___x_1411_, 1);
lean_inc(v_snd_1412_);
lean_dec_ref(v___x_1411_);
v___x_1413_ = lean_array_get_size(v_snd_1412_);
v___x_1414_ = lean_nat_dec_eq(v___x_1413_, v___x_1270_);
if (v___x_1414_ == 0)
{
lean_object* v___x_1415_; uint8_t v___x_1416_; 
v___x_1415_ = lean_nat_sub(v___x_1413_, v___x_1309_);
v___x_1416_ = lean_nat_dec_le(v___x_1270_, v___x_1415_);
if (v___x_1416_ == 0)
{
lean_inc(v___x_1415_);
v___y_1353_ = v___x_1415_;
v___y_1354_ = v_snd_1412_;
v___y_1355_ = v_snd_1405_;
v___y_1356_ = v___x_1413_;
v___y_1357_ = v___x_1415_;
goto v___jp_1352_;
}
else
{
v___y_1353_ = v___x_1415_;
v___y_1354_ = v_snd_1412_;
v___y_1355_ = v_snd_1405_;
v___y_1356_ = v___x_1413_;
v___y_1357_ = v___x_1270_;
goto v___jp_1352_;
}
}
else
{
v___y_1332_ = v_snd_1405_;
v___y_1333_ = v_snd_1412_;
goto v___jp_1331_;
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
v___jp_1433_:
{
lean_object* v___x_1436_; 
v___x_1436_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg(v___x_1432_, v_fst_1431_, v___y_1434_, v___y_1435_);
lean_dec(v___y_1435_);
v___y_1362_ = v___x_1436_;
goto v___jp_1361_;
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
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__0(lean_object* v_inst_1455_, lean_object* v_a_1456_){
_start:
{
lean_object* v___x_1457_; 
v___x_1457_ = l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__0___redArg(v_a_1456_);
return v___x_1457_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4(lean_object* v_ord_1458_, lean_object* v_range_1459_, lean_object* v_b_1460_, lean_object* v_i_1461_, lean_object* v_hs_1462_, lean_object* v_hl_1463_){
_start:
{
lean_object* v___x_1464_; 
v___x_1464_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___redArg(v_ord_1458_, v_range_1459_, v_b_1460_, v_i_1461_);
return v___x_1464_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4___boxed(lean_object* v_ord_1465_, lean_object* v_range_1466_, lean_object* v_b_1467_, lean_object* v_i_1468_, lean_object* v_hs_1469_, lean_object* v_hl_1470_){
_start:
{
lean_object* v_res_1471_; 
v_res_1471_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__4(v_ord_1465_, v_range_1466_, v_b_1467_, v_i_1468_, v_hs_1469_, v_hl_1470_);
lean_dec_ref(v_range_1466_);
lean_dec_ref(v_ord_1465_);
return v_res_1471_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5(lean_object* v___x_1472_, lean_object* v_range_1473_, lean_object* v_b_1474_, lean_object* v_i_1475_, lean_object* v_hs_1476_, lean_object* v_hl_1477_){
_start:
{
lean_object* v___x_1478_; 
v___x_1478_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___redArg(v___x_1472_, v_range_1473_, v_b_1474_, v_i_1475_);
return v___x_1478_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5___boxed(lean_object* v___x_1479_, lean_object* v_range_1480_, lean_object* v_b_1481_, lean_object* v_i_1482_, lean_object* v_hs_1483_, lean_object* v_hl_1484_){
_start:
{
lean_object* v_res_1485_; 
v_res_1485_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__5(v___x_1479_, v_range_1480_, v_b_1481_, v_i_1482_, v_hs_1483_, v_hl_1484_);
lean_dec_ref(v_range_1480_);
lean_dec_ref(v___x_1479_);
return v_res_1485_;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8(lean_object* v___x_1486_, lean_object* v_inst_1487_, lean_object* v_a_1488_){
_start:
{
lean_object* v___x_1489_; 
v___x_1489_ = l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___redArg(v___x_1486_, v_a_1488_);
return v___x_1489_;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8___boxed(lean_object* v___x_1490_, lean_object* v_inst_1491_, lean_object* v_a_1492_){
_start:
{
lean_object* v_res_1493_; 
v_res_1493_ = l___private_Init_While_0__repeatM_erased___at___00StmtKeys_permKey_spec__8(v___x_1490_, v_inst_1491_, v_a_1492_);
lean_dec_ref(v___x_1490_);
return v_res_1493_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10(lean_object* v___x_1494_, lean_object* v_range_1495_, lean_object* v_b_1496_, lean_object* v_i_1497_, lean_object* v_hs_1498_, lean_object* v_hl_1499_){
_start:
{
lean_object* v___x_1500_; 
v___x_1500_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___redArg(v___x_1494_, v_range_1495_, v_b_1496_, v_i_1497_);
return v___x_1500_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10___boxed(lean_object* v___x_1501_, lean_object* v_range_1502_, lean_object* v_b_1503_, lean_object* v_i_1504_, lean_object* v_hs_1505_, lean_object* v_hl_1506_){
_start:
{
lean_object* v_res_1507_; 
v_res_1507_ = l___private_Init_Data_Range_Basic_0__Std_Legacy_Range_forIn_x27_loop___at___00StmtKeys_permKey_spec__10(v___x_1501_, v_range_1502_, v_b_1503_, v_i_1504_, v_hs_1505_, v_hl_1506_);
lean_dec_ref(v_range_1502_);
lean_dec_ref(v___x_1501_);
return v_res_1507_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14(lean_object* v_n_1508_, lean_object* v_as_1509_, lean_object* v_lo_1510_, lean_object* v_hi_1511_, lean_object* v_w_1512_, lean_object* v_hlo_1513_, lean_object* v_hhi_1514_){
_start:
{
lean_object* v___x_1515_; 
v___x_1515_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___redArg(v_n_1508_, v_as_1509_, v_lo_1510_, v_hi_1511_);
return v___x_1515_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14___boxed(lean_object* v_n_1516_, lean_object* v_as_1517_, lean_object* v_lo_1518_, lean_object* v_hi_1519_, lean_object* v_w_1520_, lean_object* v_hlo_1521_, lean_object* v_hhi_1522_){
_start:
{
lean_object* v_res_1523_; 
v_res_1523_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14(v_n_1516_, v_as_1517_, v_lo_1518_, v_hi_1519_, v_w_1520_, v_hlo_1521_, v_hhi_1522_);
lean_dec(v_hi_1519_);
lean_dec(v_n_1516_);
return v_res_1523_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15(lean_object* v___x_1524_, lean_object* v___x_1525_, lean_object* v_as_1526_, lean_object* v_as_x27_1527_, lean_object* v_b_1528_, lean_object* v_a_1529_){
_start:
{
lean_object* v___x_1530_; 
v___x_1530_ = l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___redArg(v___x_1524_, v___x_1525_, v_as_x27_1527_, v_b_1528_);
return v___x_1530_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15___boxed(lean_object* v___x_1531_, lean_object* v___x_1532_, lean_object* v_as_1533_, lean_object* v_as_x27_1534_, lean_object* v_b_1535_, lean_object* v_a_1536_){
_start:
{
lean_object* v_res_1537_; 
v_res_1537_ = l_List_forIn_x27_loop___at___00StmtKeys_permKey_spec__15(v___x_1531_, v___x_1532_, v_as_1533_, v_as_x27_1534_, v_b_1535_, v_a_1536_);
lean_dec(v_as_x27_1534_);
lean_dec(v_as_1533_);
lean_dec_ref(v___x_1531_);
return v_res_1537_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16(lean_object* v_n_1538_, lean_object* v_as_1539_, lean_object* v_lo_1540_, lean_object* v_hi_1541_, lean_object* v_w_1542_, lean_object* v_hlo_1543_, lean_object* v_hhi_1544_){
_start:
{
lean_object* v___x_1545_; 
v___x_1545_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___redArg(v_n_1538_, v_as_1539_, v_lo_1540_, v_hi_1541_);
return v___x_1545_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16___boxed(lean_object* v_n_1546_, lean_object* v_as_1547_, lean_object* v_lo_1548_, lean_object* v_hi_1549_, lean_object* v_w_1550_, lean_object* v_hlo_1551_, lean_object* v_hhi_1552_){
_start:
{
lean_object* v_res_1553_; 
v_res_1553_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16(v_n_1546_, v_as_1547_, v_lo_1548_, v_hi_1549_, v_w_1550_, v_hlo_1551_, v_hhi_1552_);
lean_dec(v_hi_1549_);
lean_dec(v_n_1546_);
return v_res_1553_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16(lean_object* v_n_1554_, lean_object* v_lo_1555_, lean_object* v_hi_1556_, lean_object* v_hhi_1557_, uint64_t v_pivot_1558_, lean_object* v_as_1559_, lean_object* v_i_1560_, lean_object* v_k_1561_, lean_object* v_ilo_1562_, lean_object* v_ik_1563_, lean_object* v_w_1564_){
_start:
{
lean_object* v___x_1565_; 
v___x_1565_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___redArg(v_hi_1556_, v_pivot_1558_, v_as_1559_, v_i_1560_, v_k_1561_);
return v___x_1565_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16___boxed(lean_object* v_n_1566_, lean_object* v_lo_1567_, lean_object* v_hi_1568_, lean_object* v_hhi_1569_, lean_object* v_pivot_1570_, lean_object* v_as_1571_, lean_object* v_i_1572_, lean_object* v_k_1573_, lean_object* v_ilo_1574_, lean_object* v_ik_1575_, lean_object* v_w_1576_){
_start:
{
uint64_t v_pivot_boxed_1577_; lean_object* v_res_1578_; 
v_pivot_boxed_1577_ = lean_unbox_uint64(v_pivot_1570_);
lean_dec_ref(v_pivot_1570_);
v_res_1578_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__14_spec__16(v_n_1566_, v_lo_1567_, v_hi_1568_, v_hhi_1569_, v_pivot_boxed_1577_, v_as_1571_, v_i_1572_, v_k_1573_, v_ilo_1574_, v_ik_1575_, v_w_1576_);
lean_dec(v_hi_1568_);
lean_dec(v_lo_1567_);
lean_dec(v_n_1566_);
return v_res_1578_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19(lean_object* v_n_1579_, lean_object* v_lo_1580_, lean_object* v_hi_1581_, lean_object* v_hhi_1582_, lean_object* v_pivot_1583_, lean_object* v_as_1584_, lean_object* v_i_1585_, lean_object* v_k_1586_, lean_object* v_ilo_1587_, lean_object* v_ik_1588_, lean_object* v_w_1589_){
_start:
{
lean_object* v___x_1590_; 
v___x_1590_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___redArg(v_hi_1581_, v_pivot_1583_, v_as_1584_, v_i_1585_, v_k_1586_);
return v___x_1590_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19___boxed(lean_object* v_n_1591_, lean_object* v_lo_1592_, lean_object* v_hi_1593_, lean_object* v_hhi_1594_, lean_object* v_pivot_1595_, lean_object* v_as_1596_, lean_object* v_i_1597_, lean_object* v_k_1598_, lean_object* v_ilo_1599_, lean_object* v_ik_1600_, lean_object* v_w_1601_){
_start:
{
lean_object* v_res_1602_; 
v_res_1602_ = l___private_Init_Data_Array_QSort_Basic_0__Array_qpartition_loop___at___00__private_Init_Data_Array_QSort_Basic_0__Array_qsort_sort___at___00StmtKeys_permKey_spec__16_spec__19(v_n_1591_, v_lo_1592_, v_hi_1593_, v_hhi_1594_, v_pivot_1595_, v_as_1596_, v_i_1597_, v_k_1598_, v_ilo_1599_, v_ik_1600_, v_w_1601_);
lean_dec_ref(v_pivot_1595_);
lean_dec(v_hi_1593_);
lean_dec(v_lo_1592_);
lean_dec(v_n_1591_);
return v_res_1602_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_hex64(uint64_t v_h_1604_){
_start:
{
lean_object* v___x_1605_; lean_object* v___x_1606_; lean_object* v___x_1607_; lean_object* v_s_1608_; lean_object* v___x_1609_; lean_object* v___x_1610_; lean_object* v___x_1611_; lean_object* v___x_1612_; lean_object* v___x_1613_; 
v___x_1605_ = lean_unsigned_to_nat(16u);
v___x_1606_ = lean_uint64_to_nat(v_h_1604_);
v___x_1607_ = l_Nat_toDigits(v___x_1605_, v___x_1606_);
v_s_1608_ = lean_string_mk(v___x_1607_);
v___x_1609_ = ((lean_object*)(l_StmtKeys_hex64___closed__0));
v___x_1610_ = lean_string_length(v_s_1608_);
v___x_1611_ = lean_nat_sub(v___x_1605_, v___x_1610_);
v___x_1612_ = l___private_Init_Data_Nat_Basic_0__Nat_repeatTR_loop___at___00Std_Time_instToStringDuration_leftPad_spec__0(v___x_1611_, v___x_1609_);
v___x_1613_ = lean_string_append(v___x_1612_, v_s_1608_);
lean_dec_ref(v_s_1608_);
return v___x_1613_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_hex64___boxed(lean_object* v_h_1614_){
_start:
{
uint64_t v_h_boxed_1615_; lean_object* v_res_1616_; 
v_h_boxed_1615_ = lean_unbox_uint64(v_h_1614_);
lean_dec_ref(v_h_1614_);
v_res_1616_ = l_StmtKeys_hex64(v_h_boxed_1615_);
return v_res_1616_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__2(size_t v_sz_1617_, size_t v_i_1618_, lean_object* v_bs_1619_){
_start:
{
uint8_t v___x_1620_; 
v___x_1620_ = lean_usize_dec_lt(v_i_1618_, v_sz_1617_);
if (v___x_1620_ == 0)
{
return v_bs_1619_;
}
else
{
lean_object* v_v_1621_; lean_object* v___x_1622_; lean_object* v_bs_x27_1623_; lean_object* v___x_1624_; lean_object* v___x_1625_; uint8_t v___x_1626_; size_t v___x_1627_; size_t v___x_1628_; lean_object* v___x_1629_; lean_object* v___x_1630_; 
v_v_1621_ = lean_array_uget(v_bs_1619_, v_i_1618_);
v___x_1622_ = lean_unsigned_to_nat(0u);
v_bs_x27_1623_ = lean_array_uset(v_bs_1619_, v_i_1618_, v___x_1622_);
v___x_1624_ = ((lean_object*)(l_StmtKeys_projectRoots));
v___x_1625_ = l_Lean_Name_getRoot(v_v_1621_);
lean_dec(v_v_1621_);
v___x_1626_ = l_List_elem___at___00__private_Lean_Server_Completion_CompletionCollectors_0__Lean_Server_Completion_bestLabelForDecl_x3f_spec__0(v___x_1625_, v___x_1624_);
lean_dec(v___x_1625_);
v___x_1627_ = ((size_t)1ULL);
v___x_1628_ = lean_usize_add(v_i_1618_, v___x_1627_);
v___x_1629_ = lean_box(v___x_1626_);
v___x_1630_ = lean_array_uset(v_bs_x27_1623_, v_i_1618_, v___x_1629_);
v_i_1618_ = v___x_1628_;
v_bs_1619_ = v___x_1630_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__2___boxed(lean_object* v_sz_1632_, lean_object* v_i_1633_, lean_object* v_bs_1634_){
_start:
{
size_t v_sz_boxed_1635_; size_t v_i_boxed_1636_; lean_object* v_res_1637_; 
v_sz_boxed_1635_ = lean_unbox_usize(v_sz_1632_);
lean_dec(v_sz_1632_);
v_i_boxed_1636_ = lean_unbox_usize(v_i_1633_);
lean_dec(v_i_1633_);
v_res_1637_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__2(v_sz_boxed_1635_, v_i_boxed_1636_, v_bs_1634_);
return v_res_1637_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4(uint8_t v___x_1638_, size_t v_sz_1639_, size_t v_i_1640_, lean_object* v_bs_1641_){
_start:
{
uint8_t v___x_1642_; 
v___x_1642_ = lean_usize_dec_lt(v_i_1640_, v_sz_1639_);
if (v___x_1642_ == 0)
{
return v_bs_1641_;
}
else
{
lean_object* v_v_1643_; lean_object* v___x_1644_; lean_object* v_bs_x27_1645_; lean_object* v___x_1646_; size_t v___x_1647_; size_t v___x_1648_; lean_object* v___x_1649_; 
v_v_1643_ = lean_array_uget(v_bs_1641_, v_i_1640_);
v___x_1644_ = lean_unsigned_to_nat(0u);
v_bs_x27_1645_ = lean_array_uset(v_bs_1641_, v_i_1640_, v___x_1644_);
v___x_1646_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_v_1643_, v___x_1638_);
v___x_1647_ = ((size_t)1ULL);
v___x_1648_ = lean_usize_add(v_i_1640_, v___x_1647_);
v___x_1649_ = lean_array_uset(v_bs_x27_1645_, v_i_1640_, v___x_1646_);
v_i_1640_ = v___x_1648_;
v_bs_1641_ = v___x_1649_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4___boxed(lean_object* v___x_1651_, lean_object* v_sz_1652_, lean_object* v_i_1653_, lean_object* v_bs_1654_){
_start:
{
uint8_t v___x_10968__boxed_1655_; size_t v_sz_boxed_1656_; size_t v_i_boxed_1657_; lean_object* v_res_1658_; 
v___x_10968__boxed_1655_ = lean_unbox(v___x_1651_);
v_sz_boxed_1656_ = lean_unbox_usize(v_sz_1652_);
lean_dec(v_sz_1652_);
v_i_boxed_1657_ = lean_unbox_usize(v_i_1653_);
lean_dec(v_i_1653_);
v_res_1658_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4(v___x_10968__boxed_1655_, v_sz_boxed_1656_, v_i_boxed_1657_, v_bs_1654_);
return v_res_1658_;
}
}
LEAN_EXPORT uint64_t l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3(lean_object* v_a_1661_, lean_object* v_n_1662_){
_start:
{
lean_object* v___x_1663_; lean_object* v___x_1664_; uint64_t v___x_1665_; 
v___x_1663_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3___boxed__const__1));
v___x_1664_ = l_Std_DHashMap_Internal_Raw_u2080_Const_getD___at___00Lean_Linter_EnvLinter_sortResults_spec__2___redArg(v_a_1661_, v_n_1662_, v___x_1663_);
v___x_1665_ = lean_unbox_uint64(v___x_1664_);
lean_dec(v___x_1664_);
return v___x_1665_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3___boxed(lean_object* v_a_1666_, lean_object* v_n_1667_){
_start:
{
uint64_t v_res_1668_; lean_object* v_r_1669_; 
v_res_1668_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3(v_a_1666_, v_n_1667_);
lean_dec(v_n_1667_);
lean_dec_ref(v_a_1666_);
v_r_1669_ = lean_box_uint64(v_res_1668_);
return v_r_1669_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__5(lean_object* v_a_1670_, lean_object* v_as_1671_, size_t v_i_1672_, size_t v_stop_1673_, lean_object* v_b_1674_){
_start:
{
lean_object* v___y_1676_; uint8_t v___x_1680_; 
v___x_1680_ = lean_usize_dec_eq(v_i_1672_, v_stop_1673_);
if (v___x_1680_ == 0)
{
lean_object* v___x_1681_; lean_object* v___x_1682_; 
v___x_1681_ = lean_array_uget_borrowed(v_as_1671_, v_i_1672_);
lean_inc(v___x_1681_);
lean_inc_ref(v_a_1670_);
v___x_1682_ = l_Lean_Environment_find_x3f(v_a_1670_, v___x_1681_, v___x_1680_);
if (lean_obj_tag(v___x_1682_) == 1)
{
lean_object* v_val_1683_; 
v_val_1683_ = lean_ctor_get(v___x_1682_, 0);
lean_inc(v_val_1683_);
lean_dec_ref_known(v___x_1682_, 1);
if (lean_obj_tag(v_val_1683_) == 2)
{
lean_object* v___x_1684_; 
lean_dec_ref_known(v_val_1683_, 1);
lean_inc(v___x_1681_);
v___x_1684_ = lean_array_push(v_b_1674_, v___x_1681_);
v___y_1676_ = v___x_1684_;
goto v___jp_1675_;
}
else
{
lean_dec(v_val_1683_);
v___y_1676_ = v_b_1674_;
goto v___jp_1675_;
}
}
else
{
lean_dec(v___x_1682_);
v___y_1676_ = v_b_1674_;
goto v___jp_1675_;
}
}
else
{
lean_dec_ref(v_a_1670_);
return v_b_1674_;
}
v___jp_1675_:
{
size_t v___x_1677_; size_t v___x_1678_; 
v___x_1677_ = ((size_t)1ULL);
v___x_1678_ = lean_usize_add(v_i_1672_, v___x_1677_);
v_i_1672_ = v___x_1678_;
v_b_1674_ = v___y_1676_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__5___boxed(lean_object* v_a_1685_, lean_object* v_as_1686_, lean_object* v_i_1687_, lean_object* v_stop_1688_, lean_object* v_b_1689_){
_start:
{
size_t v_i_boxed_1690_; size_t v_stop_boxed_1691_; lean_object* v_res_1692_; 
v_i_boxed_1690_ = lean_unbox_usize(v_i_1687_);
lean_dec(v_i_1687_);
v_stop_boxed_1691_ = lean_unbox_usize(v_stop_1688_);
lean_dec(v_stop_1688_);
v_res_1692_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__5(v_a_1685_, v_as_1686_, v_i_boxed_1690_, v_stop_boxed_1691_, v_b_1689_);
lean_dec_ref(v_as_1686_);
return v_res_1692_;
}
}
LEAN_EXPORT uint8_t l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0(lean_object* v_a_1693_, uint8_t v___x_1694_, uint8_t v___x_1695_, lean_object* v___x_1696_, lean_object* v_n_1697_){
_start:
{
lean_object* v___x_1698_; 
v___x_1698_ = l_Lean_Environment_getModuleIdxFor_x3f(v_a_1693_, v_n_1697_);
if (lean_obj_tag(v___x_1698_) == 0)
{
return v___x_1694_;
}
else
{
lean_object* v_val_1699_; lean_object* v___x_1700_; lean_object* v___x_1701_; uint8_t v___x_1702_; 
v_val_1699_ = lean_ctor_get(v___x_1698_, 0);
lean_inc(v_val_1699_);
lean_dec_ref_known(v___x_1698_, 1);
v___x_1700_ = lean_box(v___x_1695_);
v___x_1701_ = lean_array_get(v___x_1700_, v___x_1696_, v_val_1699_);
lean_dec(v_val_1699_);
lean_dec(v___x_1700_);
v___x_1702_ = lean_unbox(v___x_1701_);
lean_dec(v___x_1701_);
return v___x_1702_;
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0___boxed(lean_object* v_a_1703_, lean_object* v___x_1704_, lean_object* v___x_1705_, lean_object* v___x_1706_, lean_object* v_n_1707_){
_start:
{
uint8_t v___x_11024__boxed_1708_; uint8_t v___x_11025__boxed_1709_; uint8_t v_res_1710_; lean_object* v_r_1711_; 
v___x_11024__boxed_1708_ = lean_unbox(v___x_1704_);
v___x_11025__boxed_1709_ = lean_unbox(v___x_1705_);
v_res_1710_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0(v_a_1703_, v___x_11024__boxed_1708_, v___x_11025__boxed_1709_, v___x_1706_, v_n_1707_);
lean_dec(v_n_1707_);
lean_dec_ref(v___x_1706_);
lean_dec_ref(v_a_1703_);
v_r_1711_ = lean_box(v_res_1710_);
return v_r_1711_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg(lean_object* v_a_1735_, lean_object* v___x_1736_, lean_object* v_a_1737_, lean_object* v_a_1738_, lean_object* v_as_x27_1739_, lean_object* v_b_1740_){
_start:
{
if (lean_obj_tag(v_as_x27_1739_) == 0)
{
lean_object* v___x_1742_; 
lean_dec_ref(v_a_1737_);
lean_dec_ref(v___x_1736_);
lean_dec_ref(v_a_1735_);
v___x_1742_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_1742_, 0, v_b_1740_);
return v___x_1742_;
}
else
{
lean_object* v_head_1743_; lean_object* v_snd_1744_; 
v_head_1743_ = lean_ctor_get(v_as_x27_1739_, 0);
v_snd_1744_ = lean_ctor_get(v_head_1743_, 1);
if (lean_obj_tag(v_snd_1744_) == 2)
{
lean_object* v_tail_1745_; lean_object* v_fst_1746_; lean_object* v_val_1747_; uint8_t v___x_1748_; lean_object* v___x_1749_; lean_object* v___x_1750_; lean_object* v___f_1751_; uint8_t v___x_1752_; 
v_tail_1745_ = lean_ctor_get(v_as_x27_1739_, 1);
v_fst_1746_ = lean_ctor_get(v_head_1743_, 0);
v_val_1747_ = lean_ctor_get(v_snd_1744_, 0);
v___x_1748_ = 0;
v___x_1749_ = lean_box(v___x_1748_);
v___x_1750_ = lean_box(v___x_1748_);
lean_inc_ref(v___x_1736_);
lean_inc_ref(v_a_1735_);
v___f_1751_ = lean_alloc_closure((void*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0___boxed), 5, 4);
lean_closure_set(v___f_1751_, 0, v_a_1735_);
lean_closure_set(v___f_1751_, 1, v___x_1749_);
lean_closure_set(v___f_1751_, 2, v___x_1750_);
lean_closure_set(v___f_1751_, 3, v___x_1736_);
v___x_1752_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0(v_a_1735_, v___x_1748_, v___x_1748_, v___x_1736_, v_fst_1746_);
if (v___x_1752_ == 0)
{
lean_dec_ref(v___f_1751_);
v_as_x27_1739_ = v_tail_1745_;
goto _start;
}
else
{
lean_object* v_toConstantVal_1754_; lean_object* v_value_1755_; lean_object* v_type_1756_; lean_object* v___x_1757_; lean_object* v___x_1758_; lean_object* v_fst_1759_; lean_object* v___x_1761_; uint8_t v_isShared_1762_; uint8_t v_isSharedCheck_2023_; 
v_toConstantVal_1754_ = lean_ctor_get(v_val_1747_, 0);
v_value_1755_ = lean_ctor_get(v_val_1747_, 1);
v_type_1756_ = lean_ctor_get(v_toConstantVal_1754_, 2);
v___x_1757_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__0));
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
v___x_1758_ = l_StmtKeys_plainKey(v___x_1757_, v___f_1751_, v_type_1756_);
v_fst_1759_ = lean_ctor_get(v___x_1758_, 0);
v_isSharedCheck_2023_ = !lean_is_exclusive(v___x_1758_);
if (v_isSharedCheck_2023_ == 0)
{
lean_object* v_unused_2024_; 
v_unused_2024_ = lean_ctor_get(v___x_1758_, 1);
lean_dec(v_unused_2024_);
v___x_1761_ = v___x_1758_;
v_isShared_1762_ = v_isSharedCheck_2023_;
goto v_resetjp_1760_;
}
else
{
lean_inc(v_fst_1759_);
lean_dec(v___x_1758_);
v___x_1761_ = lean_box(0);
v_isShared_1762_ = v_isSharedCheck_2023_;
goto v_resetjp_1760_;
}
v_resetjp_1760_:
{
lean_object* v___x_1763_; lean_object* v___x_1764_; lean_object* v_fst_1765_; lean_object* v___x_1767_; uint8_t v_isShared_1768_; uint8_t v_isSharedCheck_2021_; 
v___x_1763_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_1763_, 0, v___x_1752_);
lean_ctor_set_uint8(v___x_1763_, 1, v___x_1748_);
lean_ctor_set_uint8(v___x_1763_, 2, v___x_1748_);
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
lean_inc_ref(v___x_1763_);
v___x_1764_ = l_StmtKeys_plainKey(v___x_1763_, v___f_1751_, v_type_1756_);
v_fst_1765_ = lean_ctor_get(v___x_1764_, 0);
v_isSharedCheck_2021_ = !lean_is_exclusive(v___x_1764_);
if (v_isSharedCheck_2021_ == 0)
{
lean_object* v_unused_2022_; 
v_unused_2022_ = lean_ctor_get(v___x_1764_, 1);
lean_dec(v_unused_2022_);
v___x_1767_ = v___x_1764_;
v_isShared_1768_ = v_isSharedCheck_2021_;
goto v_resetjp_1766_;
}
else
{
lean_inc(v_fst_1765_);
lean_dec(v___x_1764_);
v___x_1767_ = lean_box(0);
v_isShared_1768_ = v_isSharedCheck_2021_;
goto v_resetjp_1766_;
}
v_resetjp_1766_:
{
lean_object* v___x_1769_; lean_object* v___x_1770_; lean_object* v_fst_1771_; lean_object* v_snd_1772_; lean_object* v___x_1774_; uint8_t v_isShared_1775_; uint8_t v_isSharedCheck_2020_; 
v___x_1769_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_1769_, 0, v___x_1752_);
lean_ctor_set_uint8(v___x_1769_, 1, v___x_1752_);
lean_ctor_set_uint8(v___x_1769_, 2, v___x_1748_);
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
v___x_1770_ = l_StmtKeys_plainKey(v___x_1769_, v___f_1751_, v_type_1756_);
v_fst_1771_ = lean_ctor_get(v___x_1770_, 0);
v_snd_1772_ = lean_ctor_get(v___x_1770_, 1);
v_isSharedCheck_2020_ = !lean_is_exclusive(v___x_1770_);
if (v_isSharedCheck_2020_ == 0)
{
v___x_1774_ = v___x_1770_;
v_isShared_1775_ = v_isSharedCheck_2020_;
goto v_resetjp_1773_;
}
else
{
lean_inc(v_snd_1772_);
lean_inc(v_fst_1771_);
lean_dec(v___x_1770_);
v___x_1774_ = lean_box(0);
v_isShared_1775_ = v_isSharedCheck_2020_;
goto v_resetjp_1773_;
}
v_resetjp_1773_:
{
lean_object* v___x_1776_; lean_object* v___x_1777_; lean_object* v_fst_1778_; lean_object* v_snd_1779_; lean_object* v___x_1781_; uint8_t v_isShared_1782_; uint8_t v_isSharedCheck_2019_; 
v___x_1776_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_1776_, 0, v___x_1752_);
lean_ctor_set_uint8(v___x_1776_, 1, v___x_1748_);
lean_ctor_set_uint8(v___x_1776_, 2, v___x_1752_);
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
lean_inc_ref(v___x_1776_);
v___x_1777_ = l_StmtKeys_plainKey(v___x_1776_, v___f_1751_, v_type_1756_);
v_fst_1778_ = lean_ctor_get(v___x_1777_, 0);
v_snd_1779_ = lean_ctor_get(v___x_1777_, 1);
v_isSharedCheck_2019_ = !lean_is_exclusive(v___x_1777_);
if (v_isSharedCheck_2019_ == 0)
{
v___x_1781_ = v___x_1777_;
v_isShared_1782_ = v_isSharedCheck_2019_;
goto v_resetjp_1780_;
}
else
{
lean_inc(v_snd_1779_);
lean_inc(v_fst_1778_);
lean_dec(v___x_1777_);
v___x_1781_ = lean_box(0);
v_isShared_1782_ = v_isSharedCheck_2019_;
goto v_resetjp_1780_;
}
v_resetjp_1780_:
{
lean_object* v___x_1783_; lean_object* v___x_1784_; lean_object* v_fst_1785_; lean_object* v___x_1787_; uint8_t v_isShared_1788_; uint8_t v_isSharedCheck_2017_; 
v___x_1783_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_1783_, 0, v___x_1752_);
lean_ctor_set_uint8(v___x_1783_, 1, v___x_1752_);
lean_ctor_set_uint8(v___x_1783_, 2, v___x_1752_);
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
lean_inc_ref(v___x_1783_);
v___x_1784_ = l_StmtKeys_plainKey(v___x_1783_, v___f_1751_, v_type_1756_);
v_fst_1785_ = lean_ctor_get(v___x_1784_, 0);
v_isSharedCheck_2017_ = !lean_is_exclusive(v___x_1784_);
if (v_isSharedCheck_2017_ == 0)
{
lean_object* v_unused_2018_; 
v_unused_2018_ = lean_ctor_get(v___x_1784_, 1);
lean_dec(v_unused_2018_);
v___x_1787_ = v___x_1784_;
v_isShared_1788_ = v_isSharedCheck_2017_;
goto v_resetjp_1786_;
}
else
{
lean_inc(v_fst_1785_);
lean_dec(v___x_1784_);
v___x_1787_ = lean_box(0);
v_isShared_1788_ = v_isSharedCheck_2017_;
goto v_resetjp_1786_;
}
v_resetjp_1786_:
{
lean_object* v___x_1789_; lean_object* v_snd_1790_; lean_object* v_fst_1791_; lean_object* v___x_1793_; uint8_t v_isShared_1794_; uint8_t v_isSharedCheck_2016_; 
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
v___x_1789_ = l_StmtKeys_permKey(v___x_1757_, v___f_1751_, v_type_1756_);
v_snd_1790_ = lean_ctor_get(v___x_1789_, 1);
v_fst_1791_ = lean_ctor_get(v___x_1789_, 0);
v_isSharedCheck_2016_ = !lean_is_exclusive(v___x_1789_);
if (v_isSharedCheck_2016_ == 0)
{
v___x_1793_ = v___x_1789_;
v_isShared_1794_ = v_isSharedCheck_2016_;
goto v_resetjp_1792_;
}
else
{
lean_inc(v_snd_1790_);
lean_inc(v_fst_1791_);
lean_dec(v___x_1789_);
v___x_1793_ = lean_box(0);
v_isShared_1794_ = v_isSharedCheck_2016_;
goto v_resetjp_1792_;
}
v_resetjp_1792_:
{
lean_object* v_fst_1795_; lean_object* v_snd_1796_; lean_object* v___x_1798_; uint8_t v_isShared_1799_; uint8_t v_isSharedCheck_2015_; 
v_fst_1795_ = lean_ctor_get(v_snd_1790_, 0);
v_snd_1796_ = lean_ctor_get(v_snd_1790_, 1);
v_isSharedCheck_2015_ = !lean_is_exclusive(v_snd_1790_);
if (v_isSharedCheck_2015_ == 0)
{
v___x_1798_ = v_snd_1790_;
v_isShared_1799_ = v_isSharedCheck_2015_;
goto v_resetjp_1797_;
}
else
{
lean_inc(v_snd_1796_);
lean_inc(v_fst_1795_);
lean_dec(v_snd_1790_);
v___x_1798_ = lean_box(0);
v_isShared_1799_ = v_isSharedCheck_2015_;
goto v_resetjp_1797_;
}
v_resetjp_1797_:
{
lean_object* v___x_1800_; lean_object* v_fst_1801_; lean_object* v___x_1803_; uint8_t v_isShared_1804_; uint8_t v_isSharedCheck_2013_; 
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
lean_inc_ref(v___x_1763_);
v___x_1800_ = l_StmtKeys_permKey(v___x_1763_, v___f_1751_, v_type_1756_);
v_fst_1801_ = lean_ctor_get(v___x_1800_, 0);
v_isSharedCheck_2013_ = !lean_is_exclusive(v___x_1800_);
if (v_isSharedCheck_2013_ == 0)
{
lean_object* v_unused_2014_; 
v_unused_2014_ = lean_ctor_get(v___x_1800_, 1);
lean_dec(v_unused_2014_);
v___x_1803_ = v___x_1800_;
v_isShared_1804_ = v_isSharedCheck_2013_;
goto v_resetjp_1802_;
}
else
{
lean_inc(v_fst_1801_);
lean_dec(v___x_1800_);
v___x_1803_ = lean_box(0);
v_isShared_1804_ = v_isSharedCheck_2013_;
goto v_resetjp_1802_;
}
v_resetjp_1802_:
{
lean_object* v___x_1805_; lean_object* v_fst_1806_; lean_object* v___x_1808_; uint8_t v_isShared_1809_; uint8_t v_isSharedCheck_2011_; 
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
v___x_1805_ = l_StmtKeys_permKey(v___x_1783_, v___f_1751_, v_type_1756_);
v_fst_1806_ = lean_ctor_get(v___x_1805_, 0);
v_isSharedCheck_2011_ = !lean_is_exclusive(v___x_1805_);
if (v_isSharedCheck_2011_ == 0)
{
lean_object* v_unused_2012_; 
v_unused_2012_ = lean_ctor_get(v___x_1805_, 1);
lean_dec(v_unused_2012_);
v___x_1808_ = v___x_1805_;
v_isShared_1809_ = v_isSharedCheck_2011_;
goto v_resetjp_1807_;
}
else
{
lean_inc(v_fst_1806_);
lean_dec(v___x_1805_);
v___x_1808_ = lean_box(0);
v_isShared_1809_ = v_isSharedCheck_2011_;
goto v_resetjp_1807_;
}
v_resetjp_1807_:
{
lean_object* v___f_1810_; lean_object* v___x_1811_; lean_object* v_fst_1812_; lean_object* v___x_1814_; uint8_t v_isShared_1815_; uint8_t v_isSharedCheck_2009_; 
v___f_1810_ = ((lean_object*)(l_StmtKeys_plainKey___closed__0));
lean_inc_ref(v_value_1755_);
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
v___x_1811_ = l_StmtKeys_jointKey(v___x_1757_, v___f_1751_, v___f_1810_, v_type_1756_, v_value_1755_);
v_fst_1812_ = lean_ctor_get(v___x_1811_, 0);
v_isSharedCheck_2009_ = !lean_is_exclusive(v___x_1811_);
if (v_isSharedCheck_2009_ == 0)
{
lean_object* v_unused_2010_; 
v_unused_2010_ = lean_ctor_get(v___x_1811_, 1);
lean_dec(v_unused_2010_);
v___x_1814_ = v___x_1811_;
v_isShared_1815_ = v_isSharedCheck_2009_;
goto v_resetjp_1813_;
}
else
{
lean_inc(v_fst_1812_);
lean_dec(v___x_1811_);
v___x_1814_ = lean_box(0);
v_isShared_1815_ = v_isSharedCheck_2009_;
goto v_resetjp_1813_;
}
v_resetjp_1813_:
{
lean_object* v___x_1816_; lean_object* v_fst_1817_; lean_object* v___x_1819_; uint8_t v_isShared_1820_; uint8_t v_isSharedCheck_2007_; 
lean_inc_ref(v_value_1755_);
lean_inc_ref(v_type_1756_);
lean_inc_ref(v___f_1751_);
v___x_1816_ = l_StmtKeys_jointKey(v___x_1763_, v___f_1751_, v___f_1810_, v_type_1756_, v_value_1755_);
v_fst_1817_ = lean_ctor_get(v___x_1816_, 0);
v_isSharedCheck_2007_ = !lean_is_exclusive(v___x_1816_);
if (v_isSharedCheck_2007_ == 0)
{
lean_object* v_unused_2008_; 
v_unused_2008_ = lean_ctor_get(v___x_1816_, 1);
lean_dec(v_unused_2008_);
v___x_1819_ = v___x_1816_;
v_isShared_1820_ = v_isSharedCheck_2007_;
goto v_resetjp_1818_;
}
else
{
lean_inc(v_fst_1817_);
lean_dec(v___x_1816_);
v___x_1819_ = lean_box(0);
v_isShared_1820_ = v_isSharedCheck_2007_;
goto v_resetjp_1818_;
}
v_resetjp_1818_:
{
lean_object* v___f_1821_; lean_object* v___x_1822_; lean_object* v_fst_1823_; lean_object* v_snd_1824_; lean_object* v___x_1826_; uint8_t v_isShared_1827_; uint8_t v_isSharedCheck_2006_; 
lean_inc_ref(v_a_1737_);
v___f_1821_ = lean_alloc_closure((void*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___lam__3___boxed), 2, 1);
lean_closure_set(v___f_1821_, 0, v_a_1737_);
lean_inc_ref(v_value_1755_);
lean_inc_ref(v_type_1756_);
v___x_1822_ = l_StmtKeys_jointKey(v___x_1776_, v___f_1751_, v___f_1821_, v_type_1756_, v_value_1755_);
v_fst_1823_ = lean_ctor_get(v___x_1822_, 0);
v_snd_1824_ = lean_ctor_get(v___x_1822_, 1);
v_isSharedCheck_2006_ = !lean_is_exclusive(v___x_1822_);
if (v_isSharedCheck_2006_ == 0)
{
v___x_1826_ = v___x_1822_;
v_isShared_1827_ = v_isSharedCheck_2006_;
goto v_resetjp_1825_;
}
else
{
lean_inc(v_snd_1824_);
lean_inc(v_fst_1823_);
lean_dec(v___x_1822_);
v___x_1826_ = lean_box(0);
v_isShared_1827_ = v_isSharedCheck_2006_;
goto v_resetjp_1825_;
}
v_resetjp_1825_:
{
lean_object* v___x_1828_; lean_object* v___x_1829_; uint64_t v___x_1830_; lean_object* v___x_1831_; lean_object* v___x_1832_; lean_object* v___x_1834_; 
v___x_1828_ = lean_unsigned_to_nat(0u);
v___x_1829_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__1));
v___x_1830_ = lean_unbox_uint64(v_fst_1812_);
lean_dec(v_fst_1812_);
v___x_1831_ = l_StmtKeys_hex64(v___x_1830_);
v___x_1832_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1832_, 0, v___x_1831_);
if (v_isShared_1827_ == 0)
{
lean_ctor_set(v___x_1826_, 1, v___x_1832_);
lean_ctor_set(v___x_1826_, 0, v___x_1829_);
v___x_1834_ = v___x_1826_;
goto v_reusejp_1833_;
}
else
{
lean_object* v_reuseFailAlloc_2005_; 
v_reuseFailAlloc_2005_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2005_, 0, v___x_1829_);
lean_ctor_set(v_reuseFailAlloc_2005_, 1, v___x_1832_);
v___x_1834_ = v_reuseFailAlloc_2005_;
goto v_reusejp_1833_;
}
v_reusejp_1833_:
{
lean_object* v___x_1835_; uint64_t v___x_1836_; lean_object* v___x_1837_; lean_object* v___x_1838_; lean_object* v___x_1840_; 
v___x_1835_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__2));
v___x_1836_ = lean_unbox_uint64(v_fst_1817_);
lean_dec(v_fst_1817_);
v___x_1837_ = l_StmtKeys_hex64(v___x_1836_);
v___x_1838_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1838_, 0, v___x_1837_);
if (v_isShared_1820_ == 0)
{
lean_ctor_set(v___x_1819_, 1, v___x_1838_);
lean_ctor_set(v___x_1819_, 0, v___x_1835_);
v___x_1840_ = v___x_1819_;
goto v_reusejp_1839_;
}
else
{
lean_object* v_reuseFailAlloc_2004_; 
v_reuseFailAlloc_2004_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2004_, 0, v___x_1835_);
lean_ctor_set(v_reuseFailAlloc_2004_, 1, v___x_1838_);
v___x_1840_ = v_reuseFailAlloc_2004_;
goto v_reusejp_1839_;
}
v_reusejp_1839_:
{
lean_object* v___x_1841_; uint64_t v___x_1842_; lean_object* v___x_1843_; lean_object* v___x_1844_; lean_object* v___x_1846_; 
v___x_1841_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__3));
v___x_1842_ = lean_unbox_uint64(v_fst_1823_);
lean_dec(v_fst_1823_);
v___x_1843_ = l_StmtKeys_hex64(v___x_1842_);
v___x_1844_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1844_, 0, v___x_1843_);
if (v_isShared_1815_ == 0)
{
lean_ctor_set(v___x_1814_, 1, v___x_1844_);
lean_ctor_set(v___x_1814_, 0, v___x_1841_);
v___x_1846_ = v___x_1814_;
goto v_reusejp_1845_;
}
else
{
lean_object* v_reuseFailAlloc_2003_; 
v_reuseFailAlloc_2003_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2003_, 0, v___x_1841_);
lean_ctor_set(v_reuseFailAlloc_2003_, 1, v___x_1844_);
v___x_1846_ = v_reuseFailAlloc_2003_;
goto v_reusejp_1845_;
}
v_reusejp_1845_:
{
lean_object* v___x_1847_; lean_object* v___x_1848_; lean_object* v___x_1849_; size_t v_sz_1850_; size_t v___x_1851_; lean_object* v___x_1852_; lean_object* v___x_1853_; lean_object* v___x_1855_; 
v___x_1847_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__4));
v___x_1848_ = lean_unsigned_to_nat(40u);
v___x_1849_ = l_Array_extract___redArg(v_snd_1824_, v___x_1828_, v___x_1848_);
v_sz_1850_ = lean_array_size(v___x_1849_);
v___x_1851_ = ((size_t)0ULL);
v___x_1852_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4(v___x_1752_, v_sz_1850_, v___x_1851_, v___x_1849_);
v___x_1853_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_1852_);
if (v_isShared_1809_ == 0)
{
lean_ctor_set(v___x_1808_, 1, v___x_1853_);
lean_ctor_set(v___x_1808_, 0, v___x_1847_);
v___x_1855_ = v___x_1808_;
goto v_reusejp_1854_;
}
else
{
lean_object* v_reuseFailAlloc_2002_; 
v_reuseFailAlloc_2002_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2002_, 0, v___x_1847_);
lean_ctor_set(v_reuseFailAlloc_2002_, 1, v___x_1853_);
v___x_1855_ = v_reuseFailAlloc_2002_;
goto v_reusejp_1854_;
}
v_reusejp_1854_:
{
lean_object* v___x_1856_; lean_object* v___x_1857_; lean_object* v___x_1858_; lean_object* v___x_1859_; lean_object* v___x_1861_; 
v___x_1856_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__5));
v___x_1857_ = lean_array_get_size(v_snd_1824_);
v___x_1858_ = l_Lean_JsonNumber_fromNat(v___x_1857_);
v___x_1859_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_1859_, 0, v___x_1858_);
if (v_isShared_1804_ == 0)
{
lean_ctor_set(v___x_1803_, 1, v___x_1859_);
lean_ctor_set(v___x_1803_, 0, v___x_1856_);
v___x_1861_ = v___x_1803_;
goto v_reusejp_1860_;
}
else
{
lean_object* v_reuseFailAlloc_2001_; 
v_reuseFailAlloc_2001_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_2001_, 0, v___x_1856_);
lean_ctor_set(v_reuseFailAlloc_2001_, 1, v___x_1859_);
v___x_1861_ = v_reuseFailAlloc_2001_;
goto v_reusejp_1860_;
}
v_reusejp_1860_:
{
lean_object* v___x_1862_; lean_object* v___y_1864_; lean_object* v___x_1994_; uint8_t v___x_1995_; 
v___x_1862_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__6));
v___x_1994_ = ((lean_object*)(l_StmtKeys_plainKey___closed__3));
v___x_1995_ = lean_nat_dec_lt(v___x_1828_, v___x_1857_);
if (v___x_1995_ == 0)
{
lean_dec(v_snd_1824_);
v___y_1864_ = v___x_1994_;
goto v___jp_1863_;
}
else
{
uint8_t v___x_1996_; 
v___x_1996_ = lean_nat_dec_le(v___x_1857_, v___x_1857_);
if (v___x_1996_ == 0)
{
if (v___x_1995_ == 0)
{
lean_dec(v_snd_1824_);
v___y_1864_ = v___x_1994_;
goto v___jp_1863_;
}
else
{
size_t v___x_1997_; lean_object* v___x_1998_; 
v___x_1997_ = lean_usize_of_nat(v___x_1857_);
lean_inc_ref(v_a_1735_);
v___x_1998_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__5(v_a_1735_, v_snd_1824_, v___x_1851_, v___x_1997_, v___x_1994_);
lean_dec(v_snd_1824_);
v___y_1864_ = v___x_1998_;
goto v___jp_1863_;
}
}
else
{
size_t v___x_1999_; lean_object* v___x_2000_; 
v___x_1999_ = lean_usize_of_nat(v___x_1857_);
lean_inc_ref(v_a_1735_);
v___x_2000_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__5(v_a_1735_, v_snd_1824_, v___x_1851_, v___x_1999_, v___x_1994_);
lean_dec(v_snd_1824_);
v___y_1864_ = v___x_2000_;
goto v___jp_1863_;
}
}
v___jp_1863_:
{
lean_object* v___x_1865_; lean_object* v___x_1866_; lean_object* v___x_1867_; lean_object* v___x_1869_; 
v___x_1865_ = lean_array_get_size(v___y_1864_);
lean_dec_ref(v___y_1864_);
v___x_1866_ = l_Lean_JsonNumber_fromNat(v___x_1865_);
v___x_1867_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_1867_, 0, v___x_1866_);
if (v_isShared_1799_ == 0)
{
lean_ctor_set(v___x_1798_, 1, v___x_1867_);
lean_ctor_set(v___x_1798_, 0, v___x_1862_);
v___x_1869_ = v___x_1798_;
goto v_reusejp_1868_;
}
else
{
lean_object* v_reuseFailAlloc_1993_; 
v_reuseFailAlloc_1993_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1993_, 0, v___x_1862_);
lean_ctor_set(v_reuseFailAlloc_1993_, 1, v___x_1867_);
v___x_1869_ = v_reuseFailAlloc_1993_;
goto v_reusejp_1868_;
}
v_reusejp_1868_:
{
lean_object* v___x_1870_; lean_object* v___x_1871_; lean_object* v___x_1872_; lean_object* v___x_1874_; 
v___x_1870_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__7));
lean_inc(v_fst_1746_);
v___x_1871_ = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(v_fst_1746_, v___x_1752_);
v___x_1872_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1872_, 0, v___x_1871_);
if (v_isShared_1794_ == 0)
{
lean_ctor_set(v___x_1793_, 1, v___x_1872_);
lean_ctor_set(v___x_1793_, 0, v___x_1870_);
v___x_1874_ = v___x_1793_;
goto v_reusejp_1873_;
}
else
{
lean_object* v_reuseFailAlloc_1992_; 
v_reuseFailAlloc_1992_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1992_, 0, v___x_1870_);
lean_ctor_set(v_reuseFailAlloc_1992_, 1, v___x_1872_);
v___x_1874_ = v_reuseFailAlloc_1992_;
goto v_reusejp_1873_;
}
v_reusejp_1873_:
{
lean_object* v___x_1875_; uint64_t v___x_1876_; lean_object* v___x_1877_; lean_object* v___x_1878_; lean_object* v___x_1880_; 
v___x_1875_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__8));
v___x_1876_ = lean_unbox_uint64(v_fst_1759_);
lean_dec(v_fst_1759_);
v___x_1877_ = l_StmtKeys_hex64(v___x_1876_);
v___x_1878_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1878_, 0, v___x_1877_);
if (v_isShared_1788_ == 0)
{
lean_ctor_set(v___x_1787_, 1, v___x_1878_);
lean_ctor_set(v___x_1787_, 0, v___x_1875_);
v___x_1880_ = v___x_1787_;
goto v_reusejp_1879_;
}
else
{
lean_object* v_reuseFailAlloc_1991_; 
v_reuseFailAlloc_1991_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1991_, 0, v___x_1875_);
lean_ctor_set(v_reuseFailAlloc_1991_, 1, v___x_1878_);
v___x_1880_ = v_reuseFailAlloc_1991_;
goto v_reusejp_1879_;
}
v_reusejp_1879_:
{
lean_object* v___x_1881_; uint64_t v___x_1882_; lean_object* v___x_1883_; lean_object* v___x_1884_; lean_object* v___x_1886_; 
v___x_1881_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__9));
v___x_1882_ = lean_unbox_uint64(v_fst_1765_);
lean_dec(v_fst_1765_);
v___x_1883_ = l_StmtKeys_hex64(v___x_1882_);
v___x_1884_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1884_, 0, v___x_1883_);
if (v_isShared_1782_ == 0)
{
lean_ctor_set(v___x_1781_, 1, v___x_1884_);
lean_ctor_set(v___x_1781_, 0, v___x_1881_);
v___x_1886_ = v___x_1781_;
goto v_reusejp_1885_;
}
else
{
lean_object* v_reuseFailAlloc_1990_; 
v_reuseFailAlloc_1990_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1990_, 0, v___x_1881_);
lean_ctor_set(v_reuseFailAlloc_1990_, 1, v___x_1884_);
v___x_1886_ = v_reuseFailAlloc_1990_;
goto v_reusejp_1885_;
}
v_reusejp_1885_:
{
lean_object* v___x_1887_; uint64_t v___x_1888_; lean_object* v___x_1889_; lean_object* v___x_1890_; lean_object* v___x_1892_; 
v___x_1887_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__10));
v___x_1888_ = lean_unbox_uint64(v_fst_1771_);
lean_dec(v_fst_1771_);
v___x_1889_ = l_StmtKeys_hex64(v___x_1888_);
v___x_1890_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1890_, 0, v___x_1889_);
if (v_isShared_1775_ == 0)
{
lean_ctor_set(v___x_1774_, 1, v___x_1890_);
lean_ctor_set(v___x_1774_, 0, v___x_1887_);
v___x_1892_ = v___x_1774_;
goto v_reusejp_1891_;
}
else
{
lean_object* v_reuseFailAlloc_1989_; 
v_reuseFailAlloc_1989_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1989_, 0, v___x_1887_);
lean_ctor_set(v_reuseFailAlloc_1989_, 1, v___x_1890_);
v___x_1892_ = v_reuseFailAlloc_1989_;
goto v_reusejp_1891_;
}
v_reusejp_1891_:
{
lean_object* v___x_1893_; uint64_t v___x_1894_; lean_object* v___x_1895_; lean_object* v___x_1896_; lean_object* v___x_1898_; 
v___x_1893_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__11));
v___x_1894_ = lean_unbox_uint64(v_fst_1778_);
lean_dec(v_fst_1778_);
v___x_1895_ = l_StmtKeys_hex64(v___x_1894_);
v___x_1896_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1896_, 0, v___x_1895_);
if (v_isShared_1768_ == 0)
{
lean_ctor_set(v___x_1767_, 1, v___x_1896_);
lean_ctor_set(v___x_1767_, 0, v___x_1893_);
v___x_1898_ = v___x_1767_;
goto v_reusejp_1897_;
}
else
{
lean_object* v_reuseFailAlloc_1988_; 
v_reuseFailAlloc_1988_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1988_, 0, v___x_1893_);
lean_ctor_set(v_reuseFailAlloc_1988_, 1, v___x_1896_);
v___x_1898_ = v_reuseFailAlloc_1988_;
goto v_reusejp_1897_;
}
v_reusejp_1897_:
{
lean_object* v___x_1899_; uint64_t v___x_1900_; lean_object* v___x_1901_; lean_object* v___x_1902_; lean_object* v___x_1904_; 
v___x_1899_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__12));
v___x_1900_ = lean_unbox_uint64(v_fst_1785_);
lean_dec(v_fst_1785_);
v___x_1901_ = l_StmtKeys_hex64(v___x_1900_);
v___x_1902_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1902_, 0, v___x_1901_);
if (v_isShared_1762_ == 0)
{
lean_ctor_set(v___x_1761_, 1, v___x_1902_);
lean_ctor_set(v___x_1761_, 0, v___x_1899_);
v___x_1904_ = v___x_1761_;
goto v_reusejp_1903_;
}
else
{
lean_object* v_reuseFailAlloc_1987_; 
v_reuseFailAlloc_1987_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1987_, 0, v___x_1899_);
lean_ctor_set(v_reuseFailAlloc_1987_, 1, v___x_1902_);
v___x_1904_ = v_reuseFailAlloc_1987_;
goto v_reusejp_1903_;
}
v_reusejp_1903_:
{
lean_object* v___x_1905_; uint64_t v___x_1906_; lean_object* v___x_1907_; lean_object* v___x_1908_; lean_object* v___x_1909_; lean_object* v___x_1910_; uint64_t v___x_1911_; lean_object* v___x_1912_; lean_object* v___x_1913_; lean_object* v___x_1914_; lean_object* v___x_1915_; uint64_t v___x_1916_; lean_object* v___x_1917_; lean_object* v___x_1918_; lean_object* v___x_1919_; lean_object* v___x_1920_; lean_object* v___x_1921_; lean_object* v___x_1922_; lean_object* v___x_1923_; lean_object* v___x_1924_; lean_object* v___x_1925_; lean_object* v___x_1926_; lean_object* v___x_1927_; lean_object* v___x_1928_; lean_object* v___x_1929_; lean_object* v___x_1930_; size_t v_sz_1931_; lean_object* v___x_1932_; lean_object* v___x_1933_; lean_object* v___x_1934_; lean_object* v___x_1935_; lean_object* v___x_1936_; size_t v_sz_1937_; lean_object* v___x_1938_; lean_object* v___x_1939_; lean_object* v___x_1940_; lean_object* v___x_1941_; lean_object* v___x_1942_; lean_object* v___x_1943_; lean_object* v___x_1944_; lean_object* v___x_1945_; lean_object* v___x_1946_; lean_object* v___x_1947_; lean_object* v___x_1948_; lean_object* v___x_1949_; lean_object* v___x_1950_; lean_object* v___x_1951_; lean_object* v___x_1952_; lean_object* v___x_1953_; lean_object* v___x_1954_; lean_object* v___x_1955_; lean_object* v___x_1956_; lean_object* v___x_1957_; lean_object* v___x_1958_; lean_object* v___x_1959_; lean_object* v___x_1960_; lean_object* v___x_1961_; lean_object* v___x_1962_; lean_object* v___x_1963_; lean_object* v___x_1964_; lean_object* v___x_1965_; lean_object* v___x_1966_; lean_object* v___x_1967_; lean_object* v___x_1968_; lean_object* v___x_1969_; lean_object* v___x_1970_; lean_object* v___x_1971_; lean_object* v___x_1972_; lean_object* v___x_1973_; lean_object* v___x_1974_; lean_object* v___x_1975_; 
v___x_1905_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__13));
v___x_1906_ = lean_unbox_uint64(v_fst_1791_);
lean_dec(v_fst_1791_);
v___x_1907_ = l_StmtKeys_hex64(v___x_1906_);
v___x_1908_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1908_, 0, v___x_1907_);
v___x_1909_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1909_, 0, v___x_1905_);
lean_ctor_set(v___x_1909_, 1, v___x_1908_);
v___x_1910_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__14));
v___x_1911_ = lean_unbox_uint64(v_fst_1801_);
lean_dec(v_fst_1801_);
v___x_1912_ = l_StmtKeys_hex64(v___x_1911_);
v___x_1913_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1913_, 0, v___x_1912_);
v___x_1914_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1914_, 0, v___x_1910_);
lean_ctor_set(v___x_1914_, 1, v___x_1913_);
v___x_1915_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__15));
v___x_1916_ = lean_unbox_uint64(v_fst_1806_);
lean_dec(v_fst_1806_);
v___x_1917_ = l_StmtKeys_hex64(v___x_1916_);
v___x_1918_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1918_, 0, v___x_1917_);
v___x_1919_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1919_, 0, v___x_1915_);
lean_ctor_set(v___x_1919_, 1, v___x_1918_);
v___x_1920_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__16));
v___x_1921_ = l_Lean_JsonNumber_fromNat(v_fst_1795_);
v___x_1922_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_1922_, 0, v___x_1921_);
v___x_1923_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1923_, 0, v___x_1920_);
lean_ctor_set(v___x_1923_, 1, v___x_1922_);
v___x_1924_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__17));
v___x_1925_ = l_Lean_JsonNumber_fromNat(v_snd_1796_);
v___x_1926_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_1926_, 0, v___x_1925_);
v___x_1927_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1927_, 0, v___x_1924_);
lean_ctor_set(v___x_1927_, 1, v___x_1926_);
v___x_1928_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__18));
v___x_1929_ = lean_unsigned_to_nat(24u);
v___x_1930_ = l_Array_extract___redArg(v_snd_1772_, v___x_1828_, v___x_1929_);
v_sz_1931_ = lean_array_size(v___x_1930_);
v___x_1932_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4(v___x_1752_, v_sz_1931_, v___x_1851_, v___x_1930_);
v___x_1933_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_1932_);
v___x_1934_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1934_, 0, v___x_1928_);
lean_ctor_set(v___x_1934_, 1, v___x_1933_);
v___x_1935_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__19));
v___x_1936_ = l_Array_extract___redArg(v_snd_1779_, v___x_1828_, v___x_1929_);
v_sz_1937_ = lean_array_size(v___x_1936_);
v___x_1938_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__4(v___x_1752_, v_sz_1937_, v___x_1851_, v___x_1936_);
v___x_1939_ = l_Lean_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__1(v___x_1938_);
v___x_1940_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1940_, 0, v___x_1935_);
lean_ctor_set(v___x_1940_, 1, v___x_1939_);
v___x_1941_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__20));
v___x_1942_ = lean_array_get_size(v_snd_1772_);
lean_dec(v_snd_1772_);
v___x_1943_ = l_Lean_JsonNumber_fromNat(v___x_1942_);
v___x_1944_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_1944_, 0, v___x_1943_);
v___x_1945_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1945_, 0, v___x_1941_);
lean_ctor_set(v___x_1945_, 1, v___x_1944_);
v___x_1946_ = ((lean_object*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___closed__21));
v___x_1947_ = lean_array_get_size(v_snd_1779_);
lean_dec(v_snd_1779_);
v___x_1948_ = l_Lean_JsonNumber_fromNat(v___x_1947_);
v___x_1949_ = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(v___x_1949_, 0, v___x_1948_);
v___x_1950_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1950_, 0, v___x_1946_);
lean_ctor_set(v___x_1950_, 1, v___x_1949_);
v___x_1951_ = lean_box(0);
v___x_1952_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1952_, 0, v___x_1950_);
lean_ctor_set(v___x_1952_, 1, v___x_1951_);
v___x_1953_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1953_, 0, v___x_1945_);
lean_ctor_set(v___x_1953_, 1, v___x_1952_);
v___x_1954_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1954_, 0, v___x_1940_);
lean_ctor_set(v___x_1954_, 1, v___x_1953_);
v___x_1955_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1955_, 0, v___x_1934_);
lean_ctor_set(v___x_1955_, 1, v___x_1954_);
v___x_1956_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1956_, 0, v___x_1927_);
lean_ctor_set(v___x_1956_, 1, v___x_1955_);
v___x_1957_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1957_, 0, v___x_1923_);
lean_ctor_set(v___x_1957_, 1, v___x_1956_);
v___x_1958_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1958_, 0, v___x_1919_);
lean_ctor_set(v___x_1958_, 1, v___x_1957_);
v___x_1959_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1959_, 0, v___x_1914_);
lean_ctor_set(v___x_1959_, 1, v___x_1958_);
v___x_1960_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1960_, 0, v___x_1909_);
lean_ctor_set(v___x_1960_, 1, v___x_1959_);
v___x_1961_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1961_, 0, v___x_1904_);
lean_ctor_set(v___x_1961_, 1, v___x_1960_);
v___x_1962_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1962_, 0, v___x_1898_);
lean_ctor_set(v___x_1962_, 1, v___x_1961_);
v___x_1963_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1963_, 0, v___x_1892_);
lean_ctor_set(v___x_1963_, 1, v___x_1962_);
v___x_1964_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1964_, 0, v___x_1886_);
lean_ctor_set(v___x_1964_, 1, v___x_1963_);
v___x_1965_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1965_, 0, v___x_1880_);
lean_ctor_set(v___x_1965_, 1, v___x_1964_);
v___x_1966_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1966_, 0, v___x_1874_);
lean_ctor_set(v___x_1966_, 1, v___x_1965_);
v___x_1967_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1967_, 0, v___x_1869_);
lean_ctor_set(v___x_1967_, 1, v___x_1966_);
v___x_1968_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1968_, 0, v___x_1861_);
lean_ctor_set(v___x_1968_, 1, v___x_1967_);
v___x_1969_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1969_, 0, v___x_1855_);
lean_ctor_set(v___x_1969_, 1, v___x_1968_);
v___x_1970_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1970_, 0, v___x_1846_);
lean_ctor_set(v___x_1970_, 1, v___x_1969_);
v___x_1971_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1971_, 0, v___x_1840_);
lean_ctor_set(v___x_1971_, 1, v___x_1970_);
v___x_1972_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_1972_, 0, v___x_1834_);
lean_ctor_set(v___x_1972_, 1, v___x_1971_);
v___x_1973_ = l_Lean_Json_mkObj(v___x_1972_);
lean_dec_ref_known(v___x_1972_, 2);
v___x_1974_ = l_Lean_Json_compress(v___x_1973_);
v___x_1975_ = l_IO_FS_Handle_putStrLn(v_a_1738_, v___x_1974_);
if (lean_obj_tag(v___x_1975_) == 0)
{
lean_object* v___x_1976_; lean_object* v___x_1977_; 
lean_dec_ref_known(v___x_1975_, 1);
v___x_1976_ = lean_unsigned_to_nat(1u);
v___x_1977_ = lean_nat_add(v_b_1740_, v___x_1976_);
lean_dec(v_b_1740_);
v_as_x27_1739_ = v_tail_1745_;
v_b_1740_ = v___x_1977_;
goto _start;
}
else
{
lean_object* v_a_1979_; lean_object* v___x_1981_; uint8_t v_isShared_1982_; uint8_t v_isSharedCheck_1986_; 
lean_dec(v_b_1740_);
lean_dec_ref(v_a_1737_);
lean_dec_ref(v___x_1736_);
lean_dec_ref(v_a_1735_);
v_a_1979_ = lean_ctor_get(v___x_1975_, 0);
v_isSharedCheck_1986_ = !lean_is_exclusive(v___x_1975_);
if (v_isSharedCheck_1986_ == 0)
{
v___x_1981_ = v___x_1975_;
v_isShared_1982_ = v_isSharedCheck_1986_;
goto v_resetjp_1980_;
}
else
{
lean_inc(v_a_1979_);
lean_dec(v___x_1975_);
v___x_1981_ = lean_box(0);
v_isShared_1982_ = v_isSharedCheck_1986_;
goto v_resetjp_1980_;
}
v_resetjp_1980_:
{
lean_object* v___x_1984_; 
if (v_isShared_1982_ == 0)
{
v___x_1984_ = v___x_1981_;
goto v_reusejp_1983_;
}
else
{
lean_object* v_reuseFailAlloc_1985_; 
v_reuseFailAlloc_1985_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_1985_, 0, v_a_1979_);
v___x_1984_ = v_reuseFailAlloc_1985_;
goto v_reusejp_1983_;
}
v_reusejp_1983_:
{
return v___x_1984_;
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
lean_object* v_tail_2025_; 
v_tail_2025_ = lean_ctor_get(v_as_x27_1739_, 1);
v_as_x27_1739_ = v_tail_2025_;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg___boxed(lean_object* v_a_2027_, lean_object* v___x_2028_, lean_object* v_a_2029_, lean_object* v_a_2030_, lean_object* v_as_x27_2031_, lean_object* v_b_2032_, lean_object* v___y_2033_){
_start:
{
lean_object* v_res_2034_; 
v_res_2034_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg(v_a_2027_, v___x_2028_, v_a_2029_, v_a_2030_, v_as_x27_2031_, v_b_2032_);
lean_dec(v_as_x27_2031_);
lean_dec(v_a_2030_);
return v_res_2034_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__1(size_t v_sz_2035_, size_t v_i_2036_, lean_object* v_bs_2037_){
_start:
{
uint8_t v___x_2038_; 
v___x_2038_ = lean_usize_dec_lt(v_i_2036_, v_sz_2035_);
if (v___x_2038_ == 0)
{
return v_bs_2037_;
}
else
{
lean_object* v_v_2039_; lean_object* v___x_2040_; lean_object* v_bs_x27_2041_; uint8_t v___x_2042_; lean_object* v___x_2043_; size_t v___x_2044_; size_t v___x_2045_; lean_object* v___x_2046_; 
v_v_2039_ = lean_array_uget(v_bs_2037_, v_i_2036_);
v___x_2040_ = lean_unsigned_to_nat(0u);
v_bs_x27_2041_ = lean_array_uset(v_bs_2037_, v_i_2036_, v___x_2040_);
v___x_2042_ = 0;
v___x_2043_ = lean_alloc_ctor(0, 1, 3);
lean_ctor_set(v___x_2043_, 0, v_v_2039_);
lean_ctor_set_uint8(v___x_2043_, sizeof(void*)*1, v___x_2042_);
lean_ctor_set_uint8(v___x_2043_, sizeof(void*)*1 + 1, v___x_2038_);
lean_ctor_set_uint8(v___x_2043_, sizeof(void*)*1 + 2, v___x_2042_);
v___x_2044_ = ((size_t)1ULL);
v___x_2045_ = lean_usize_add(v_i_2036_, v___x_2044_);
v___x_2046_ = lean_array_uset(v_bs_x27_2041_, v_i_2036_, v___x_2043_);
v_i_2036_ = v___x_2045_;
v_bs_2037_ = v___x_2046_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__1___boxed(lean_object* v_sz_2048_, lean_object* v_i_2049_, lean_object* v_bs_2050_){
_start:
{
size_t v_sz_boxed_2051_; size_t v_i_boxed_2052_; lean_object* v_res_2053_; 
v_sz_boxed_2051_ = lean_unbox_usize(v_sz_2048_);
lean_dec(v_sz_2048_);
v_i_boxed_2052_ = lean_unbox_usize(v_i_2049_);
lean_dec(v_i_2049_);
v_res_2053_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__1(v_sz_boxed_2051_, v_i_boxed_2052_, v_bs_2050_);
return v_res_2053_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__0(size_t v_sz_2054_, size_t v_i_2055_, lean_object* v_bs_2056_){
_start:
{
uint8_t v___x_2057_; 
v___x_2057_ = lean_usize_dec_lt(v_i_2055_, v_sz_2054_);
if (v___x_2057_ == 0)
{
return v_bs_2056_;
}
else
{
lean_object* v_v_2058_; lean_object* v___x_2059_; lean_object* v_bs_x27_2060_; lean_object* v___x_2061_; size_t v___x_2062_; size_t v___x_2063_; lean_object* v___x_2064_; 
v_v_2058_ = lean_array_uget(v_bs_2056_, v_i_2055_);
v___x_2059_ = lean_unsigned_to_nat(0u);
v_bs_x27_2060_ = lean_array_uset(v_bs_2056_, v_i_2055_, v___x_2059_);
v___x_2061_ = l_String_toName(v_v_2058_);
v___x_2062_ = ((size_t)1ULL);
v___x_2063_ = lean_usize_add(v_i_2055_, v___x_2062_);
v___x_2064_ = lean_array_uset(v_bs_x27_2060_, v_i_2055_, v___x_2061_);
v_i_2055_ = v___x_2063_;
v_bs_2056_ = v___x_2064_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__0___boxed(lean_object* v_sz_2066_, lean_object* v_i_2067_, lean_object* v_bs_2068_){
_start:
{
size_t v_sz_boxed_2069_; size_t v_i_boxed_2070_; lean_object* v_res_2071_; 
v_sz_boxed_2069_ = lean_unbox_usize(v_sz_2066_);
lean_dec(v_sz_2066_);
v_i_boxed_2070_ = lean_unbox_usize(v_i_2067_);
lean_dec(v_i_2067_);
v_res_2071_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__0(v_sz_boxed_2069_, v_i_boxed_2070_, v_bs_2068_);
return v_res_2071_;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__7(lean_object* v_as_2072_, size_t v_i_2073_, size_t v_stop_2074_, lean_object* v_b_2075_){
_start:
{
lean_object* v___y_2077_; uint8_t v___x_2081_; 
v___x_2081_ = lean_usize_dec_eq(v_i_2073_, v_stop_2074_);
if (v___x_2081_ == 0)
{
lean_object* v___x_2082_; lean_object* v___x_2085_; uint8_t v___x_2086_; 
v___x_2082_ = lean_array_uget_borrowed(v_as_2072_, v_i_2073_);
v___x_2085_ = ((lean_object*)(l_StmtKeys_hex64___closed__0));
v___x_2086_ = lean_string_dec_eq(v___x_2082_, v___x_2085_);
if (v___x_2086_ == 0)
{
goto v___jp_2083_;
}
else
{
if (v___x_2081_ == 0)
{
v___y_2077_ = v_b_2075_;
goto v___jp_2076_;
}
else
{
goto v___jp_2083_;
}
}
v___jp_2083_:
{
lean_object* v___x_2084_; 
lean_inc(v___x_2082_);
v___x_2084_ = lean_array_push(v_b_2075_, v___x_2082_);
v___y_2077_ = v___x_2084_;
goto v___jp_2076_;
}
}
else
{
return v_b_2075_;
}
v___jp_2076_:
{
size_t v___x_2078_; size_t v___x_2079_; 
v___x_2078_ = ((size_t)1ULL);
v___x_2079_ = lean_usize_add(v_i_2073_, v___x_2078_);
v_i_2073_ = v___x_2079_;
v_b_2075_ = v___y_2077_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__7___boxed(lean_object* v_as_2087_, lean_object* v_i_2088_, lean_object* v_stop_2089_, lean_object* v_b_2090_){
_start:
{
size_t v_i_boxed_2091_; size_t v_stop_boxed_2092_; lean_object* v_res_2093_; 
v_i_boxed_2091_ = lean_unbox_usize(v_i_2088_);
lean_dec(v_i_2088_);
v_stop_boxed_2092_ = lean_unbox_usize(v_stop_2089_);
lean_dec(v_stop_2089_);
v_res_2093_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__7(v_as_2087_, v_i_boxed_2091_, v_stop_boxed_2092_, v_b_2090_);
lean_dec_ref(v_as_2087_);
return v_res_2093_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg(lean_object* v_a_2094_, lean_object* v___x_2095_, lean_object* v_as_x27_2096_, lean_object* v_b_2097_){
_start:
{
if (lean_obj_tag(v_as_x27_2096_) == 0)
{
lean_object* v___x_2099_; 
lean_dec_ref(v___x_2095_);
lean_dec_ref(v_a_2094_);
v___x_2099_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_2099_, 0, v_b_2097_);
return v___x_2099_;
}
else
{
lean_object* v_head_2100_; lean_object* v_tail_2101_; lean_object* v_fst_2102_; lean_object* v_snd_2103_; uint8_t v___x_2104_; lean_object* v___x_2105_; lean_object* v___x_2106_; lean_object* v___f_2107_; uint8_t v___x_2108_; 
v_head_2100_ = lean_ctor_get(v_as_x27_2096_, 0);
v_tail_2101_ = lean_ctor_get(v_as_x27_2096_, 1);
v_fst_2102_ = lean_ctor_get(v_head_2100_, 0);
v_snd_2103_ = lean_ctor_get(v_head_2100_, 1);
v___x_2104_ = 0;
v___x_2105_ = lean_box(v___x_2104_);
v___x_2106_ = lean_box(v___x_2104_);
lean_inc_ref(v___x_2095_);
lean_inc_ref(v_a_2094_);
v___f_2107_ = lean_alloc_closure((void*)(l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0___boxed), 5, 4);
lean_closure_set(v___f_2107_, 0, v_a_2094_);
lean_closure_set(v___f_2107_, 1, v___x_2105_);
lean_closure_set(v___f_2107_, 2, v___x_2106_);
lean_closure_set(v___f_2107_, 3, v___x_2095_);
v___x_2108_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___lam__0(v_a_2094_, v___x_2104_, v___x_2104_, v___x_2095_, v_fst_2102_);
if (v___x_2108_ == 0)
{
lean_dec_ref(v___f_2107_);
v_as_x27_2096_ = v_tail_2101_;
goto _start;
}
else
{
lean_object* v___f_2110_; uint64_t v___y_2112_; 
v___f_2110_ = ((lean_object*)(l_StmtKeys_plainKey___closed__0));
switch(lean_obj_tag(v_snd_2103_))
{
case 2:
{
uint64_t v___x_2124_; 
v___x_2124_ = 1ULL;
v___y_2112_ = v___x_2124_;
goto v___jp_2111_;
}
case 1:
{
uint64_t v___x_2125_; 
v___x_2125_ = 2ULL;
v___y_2112_ = v___x_2125_;
goto v___jp_2111_;
}
case 6:
{
uint64_t v___x_2126_; 
v___x_2126_ = 3ULL;
v___y_2112_ = v___x_2126_;
goto v___jp_2111_;
}
case 5:
{
uint64_t v___x_2127_; 
v___x_2127_ = 4ULL;
v___y_2112_ = v___x_2127_;
goto v___jp_2111_;
}
case 7:
{
uint64_t v___x_2128_; 
v___x_2128_ = 5ULL;
v___y_2112_ = v___x_2128_;
goto v___jp_2111_;
}
case 3:
{
uint64_t v___x_2129_; 
v___x_2129_ = 6ULL;
v___y_2112_ = v___x_2129_;
goto v___jp_2111_;
}
default: 
{
uint64_t v___x_2130_; 
v___x_2130_ = 7ULL;
v___y_2112_ = v___x_2130_;
goto v___jp_2111_;
}
}
v___jp_2111_:
{
lean_object* v___x_2113_; lean_object* v___x_2114_; lean_object* v___x_2115_; lean_object* v___x_2116_; lean_object* v___x_2117_; lean_object* v_fst_2118_; uint64_t v___x_2119_; uint64_t v___x_2120_; lean_object* v___x_2121_; lean_object* v___x_2122_; 
v___x_2113_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_2113_, 0, v___x_2108_);
lean_ctor_set_uint8(v___x_2113_, 1, v___x_2104_);
lean_ctor_set_uint8(v___x_2113_, 2, v___x_2108_);
v___x_2114_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_2114_, 0, v___x_2113_);
lean_ctor_set(v___x_2114_, 1, v___f_2107_);
lean_ctor_set(v___x_2114_, 2, v___f_2110_);
lean_ctor_set_uint8(v___x_2114_, sizeof(void*)*3, v___x_2104_);
v___x_2115_ = l_Lean_ConstantInfo_type(v_snd_2103_);
v___x_2116_ = lean_obj_once(&l_StmtKeys_plainKey___closed__4, &l_StmtKeys_plainKey___closed__4_once, _init_l_StmtKeys_plainKey___closed__4);
v___x_2117_ = l_StmtKeys_hx(v___x_2114_, v___x_2115_, v___x_2116_);
v_fst_2118_ = lean_ctor_get(v___x_2117_, 0);
lean_inc(v_fst_2118_);
lean_dec_ref(v___x_2117_);
v___x_2119_ = lean_unbox_uint64(v_fst_2118_);
lean_dec(v_fst_2118_);
v___x_2120_ = lean_uint64_mix_hash(v___y_2112_, v___x_2119_);
v___x_2121_ = lean_box_uint64(v___x_2120_);
lean_inc(v_fst_2102_);
v___x_2122_ = l_Std_DHashMap_Internal_Raw_u2080_insert___at___00__private_Lean_Compiler_LCNF_EmitC_0__Lean_Compiler_LCNF_Arg_toCString_spec__1___redArg(v_b_2097_, v_fst_2102_, v___x_2121_);
v_as_x27_2096_ = v_tail_2101_;
v_b_2097_ = v___x_2122_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg___boxed(lean_object* v_a_2131_, lean_object* v___x_2132_, lean_object* v_as_x27_2133_, lean_object* v_b_2134_, lean_object* v___y_2135_){
_start:
{
lean_object* v_res_2136_; 
v_res_2136_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg(v_a_2131_, v___x_2132_, v_as_x27_2133_, v_b_2134_);
lean_dec(v_as_x27_2133_);
return v_res_2136_;
}
}
static lean_object* _init_l_StmtKeys_main___closed__6(void){
_start:
{
lean_object* v___x_2145_; lean_object* v___x_2146_; lean_object* v___x_2147_; 
v___x_2145_ = lean_obj_once(&l_StmtKeys_permKey___lam__1___closed__0, &l_StmtKeys_permKey___lam__1___closed__0_once, _init_l_StmtKeys_permKey___lam__1___closed__0);
v___x_2146_ = lean_unsigned_to_nat(0u);
v___x_2147_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_2147_, 0, v___x_2146_);
lean_ctor_set(v___x_2147_, 1, v___x_2145_);
return v___x_2147_;
}
}
static lean_object* _init_l_StmtKeys_main___boxed__const__1(void){
_start:
{
uint32_t v___x_2150_; lean_object* v___x_2151_; 
v___x_2150_ = 0;
v___x_2151_ = lean_box_uint32(v___x_2150_);
return v___x_2151_;
}
}
LEAN_EXPORT lean_object* l_StmtKeys_main(lean_object* v_args_2152_){
_start:
{
if (lean_obj_tag(v_args_2152_) == 1)
{
lean_object* v_tail_2157_; 
v_tail_2157_ = lean_ctor_get(v_args_2152_, 1);
if (lean_obj_tag(v_tail_2157_) == 1)
{
lean_object* v_tail_2158_; 
v_tail_2158_ = lean_ctor_get(v_tail_2157_, 1);
if (lean_obj_tag(v_tail_2158_) == 0)
{
lean_object* v_head_2159_; lean_object* v_head_2160_; lean_object* v___x_2161_; lean_object* v___x_2162_; 
v_head_2159_ = lean_ctor_get(v_args_2152_, 0);
v_head_2160_ = lean_ctor_get(v_tail_2157_, 0);
v___x_2161_ = ((lean_object*)(l_StmtKeys_main___closed__2));
v___x_2162_ = l_Lean_findSysroot(v___x_2161_);
if (lean_obj_tag(v___x_2162_) == 0)
{
lean_object* v_a_2163_; lean_object* v___x_2164_; lean_object* v___x_2165_; 
v_a_2163_ = lean_ctor_get(v___x_2162_, 0);
lean_inc(v_a_2163_);
lean_dec_ref_known(v___x_2162_, 1);
v___x_2164_ = lean_box(0);
v___x_2165_ = l_Lean_initSearchPath(v_a_2163_, v___x_2164_);
if (lean_obj_tag(v___x_2165_) == 0)
{
lean_object* v___x_2166_; lean_object* v___x_2167_; 
lean_dec_ref_known(v___x_2165_, 1);
v___x_2166_ = lean_enable_initializer_execution();
v___x_2167_ = l_IO_FS_lines(v_head_2159_);
if (lean_obj_tag(v___x_2167_) == 0)
{
lean_object* v_a_2168_; lean_object* v___x_2169_; lean_object* v___y_2171_; lean_object* v___y_2172_; lean_object* v___y_2173_; lean_object* v___y_2174_; lean_object* v___y_2239_; lean_object* v___x_2273_; lean_object* v___x_2274_; uint8_t v___x_2275_; 
v_a_2168_ = lean_ctor_get(v___x_2167_, 0);
lean_inc(v_a_2168_);
lean_dec_ref_known(v___x_2167_, 1);
v___x_2169_ = lean_unsigned_to_nat(0u);
v___x_2273_ = lean_array_get_size(v_a_2168_);
v___x_2274_ = ((lean_object*)(l_StmtKeys_main___closed__7));
v___x_2275_ = lean_nat_dec_lt(v___x_2169_, v___x_2273_);
if (v___x_2275_ == 0)
{
lean_dec(v_a_2168_);
v___y_2239_ = v___x_2274_;
goto v___jp_2238_;
}
else
{
uint8_t v___x_2276_; 
v___x_2276_ = lean_nat_dec_le(v___x_2273_, v___x_2273_);
if (v___x_2276_ == 0)
{
if (v___x_2275_ == 0)
{
lean_dec(v_a_2168_);
v___y_2239_ = v___x_2274_;
goto v___jp_2238_;
}
else
{
size_t v___x_2277_; size_t v___x_2278_; lean_object* v___x_2279_; 
v___x_2277_ = ((size_t)0ULL);
v___x_2278_ = lean_usize_of_nat(v___x_2273_);
v___x_2279_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__7(v_a_2168_, v___x_2277_, v___x_2278_, v___x_2274_);
lean_dec(v_a_2168_);
v___y_2239_ = v___x_2279_;
goto v___jp_2238_;
}
}
else
{
size_t v___x_2280_; size_t v___x_2281_; lean_object* v___x_2282_; 
v___x_2280_ = ((size_t)0ULL);
v___x_2281_ = lean_usize_of_nat(v___x_2273_);
v___x_2282_ = l___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00StmtKeys_main_spec__7(v_a_2168_, v___x_2280_, v___x_2281_, v___x_2274_);
lean_dec(v_a_2168_);
v___y_2239_ = v___x_2282_;
goto v___jp_2238_;
}
}
v___jp_2170_:
{
lean_object* v___x_2175_; 
lean_inc_ref(v___y_2172_);
lean_inc_ref(v___y_2173_);
lean_inc_ref(v___y_2171_);
v___x_2175_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg(v___y_2171_, v___y_2173_, v___y_2174_, v___y_2172_);
if (lean_obj_tag(v___x_2175_) == 0)
{
lean_object* v_a_2176_; uint8_t v___x_2177_; lean_object* v___x_2178_; 
v_a_2176_ = lean_ctor_get(v___x_2175_, 0);
lean_inc(v_a_2176_);
lean_dec_ref_known(v___x_2175_, 1);
v___x_2177_ = 1;
v___x_2178_ = lean_io_prim_handle_mk(v_head_2160_, v___x_2177_);
if (lean_obj_tag(v___x_2178_) == 0)
{
lean_object* v_a_2179_; lean_object* v___x_2180_; 
v_a_2179_ = lean_ctor_get(v___x_2178_, 0);
lean_inc(v_a_2179_);
lean_dec_ref_known(v___x_2178_, 1);
v___x_2180_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg(v___y_2171_, v___y_2173_, v_a_2176_, v_a_2179_, v___y_2174_, v___x_2169_);
lean_dec(v___y_2174_);
if (lean_obj_tag(v___x_2180_) == 0)
{
lean_object* v_a_2181_; lean_object* v___x_2182_; 
v_a_2181_ = lean_ctor_get(v___x_2180_, 0);
lean_inc(v_a_2181_);
lean_dec_ref_known(v___x_2180_, 1);
v___x_2182_ = lean_io_prim_handle_flush(v_a_2179_);
lean_dec(v_a_2179_);
if (lean_obj_tag(v___x_2182_) == 0)
{
lean_object* v___x_2183_; lean_object* v___x_2184_; lean_object* v___x_2185_; lean_object* v___x_2186_; lean_object* v___x_2187_; lean_object* v___x_2188_; 
lean_dec_ref_known(v___x_2182_, 1);
v___x_2183_ = ((lean_object*)(l_StmtKeys_main___closed__3));
v___x_2184_ = l_Nat_reprFast(v_a_2181_);
v___x_2185_ = lean_string_append(v___x_2183_, v___x_2184_);
lean_dec_ref(v___x_2184_);
v___x_2186_ = ((lean_object*)(l_StmtKeys_main___closed__4));
v___x_2187_ = lean_string_append(v___x_2185_, v___x_2186_);
v___x_2188_ = l_IO_eprintln___at___00__private_Lean_Shell_0__Lean_shellMain_spec__1(v___x_2187_);
if (lean_obj_tag(v___x_2188_) == 0)
{
lean_object* v___x_2190_; uint8_t v_isShared_2191_; uint8_t v_isSharedCheck_2196_; 
v_isSharedCheck_2196_ = !lean_is_exclusive(v___x_2188_);
if (v_isSharedCheck_2196_ == 0)
{
lean_object* v_unused_2197_; 
v_unused_2197_ = lean_ctor_get(v___x_2188_, 0);
lean_dec(v_unused_2197_);
v___x_2190_ = v___x_2188_;
v_isShared_2191_ = v_isSharedCheck_2196_;
goto v_resetjp_2189_;
}
else
{
lean_dec(v___x_2188_);
v___x_2190_ = lean_box(0);
v_isShared_2191_ = v_isSharedCheck_2196_;
goto v_resetjp_2189_;
}
v_resetjp_2189_:
{
lean_object* v___x_2192_; lean_object* v___x_2194_; 
v___x_2192_ = l_StmtKeys_main___boxed__const__1;
if (v_isShared_2191_ == 0)
{
lean_ctor_set(v___x_2190_, 0, v___x_2192_);
v___x_2194_ = v___x_2190_;
goto v_reusejp_2193_;
}
else
{
lean_object* v_reuseFailAlloc_2195_; 
v_reuseFailAlloc_2195_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2195_, 0, v___x_2192_);
v___x_2194_ = v_reuseFailAlloc_2195_;
goto v_reusejp_2193_;
}
v_reusejp_2193_:
{
return v___x_2194_;
}
}
}
else
{
lean_object* v_a_2198_; lean_object* v___x_2200_; uint8_t v_isShared_2201_; uint8_t v_isSharedCheck_2205_; 
v_a_2198_ = lean_ctor_get(v___x_2188_, 0);
v_isSharedCheck_2205_ = !lean_is_exclusive(v___x_2188_);
if (v_isSharedCheck_2205_ == 0)
{
v___x_2200_ = v___x_2188_;
v_isShared_2201_ = v_isSharedCheck_2205_;
goto v_resetjp_2199_;
}
else
{
lean_inc(v_a_2198_);
lean_dec(v___x_2188_);
v___x_2200_ = lean_box(0);
v_isShared_2201_ = v_isSharedCheck_2205_;
goto v_resetjp_2199_;
}
v_resetjp_2199_:
{
lean_object* v___x_2203_; 
if (v_isShared_2201_ == 0)
{
v___x_2203_ = v___x_2200_;
goto v_reusejp_2202_;
}
else
{
lean_object* v_reuseFailAlloc_2204_; 
v_reuseFailAlloc_2204_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2204_, 0, v_a_2198_);
v___x_2203_ = v_reuseFailAlloc_2204_;
goto v_reusejp_2202_;
}
v_reusejp_2202_:
{
return v___x_2203_;
}
}
}
}
else
{
lean_object* v_a_2206_; lean_object* v___x_2208_; uint8_t v_isShared_2209_; uint8_t v_isSharedCheck_2213_; 
lean_dec(v_a_2181_);
v_a_2206_ = lean_ctor_get(v___x_2182_, 0);
v_isSharedCheck_2213_ = !lean_is_exclusive(v___x_2182_);
if (v_isSharedCheck_2213_ == 0)
{
v___x_2208_ = v___x_2182_;
v_isShared_2209_ = v_isSharedCheck_2213_;
goto v_resetjp_2207_;
}
else
{
lean_inc(v_a_2206_);
lean_dec(v___x_2182_);
v___x_2208_ = lean_box(0);
v_isShared_2209_ = v_isSharedCheck_2213_;
goto v_resetjp_2207_;
}
v_resetjp_2207_:
{
lean_object* v___x_2211_; 
if (v_isShared_2209_ == 0)
{
v___x_2211_ = v___x_2208_;
goto v_reusejp_2210_;
}
else
{
lean_object* v_reuseFailAlloc_2212_; 
v_reuseFailAlloc_2212_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2212_, 0, v_a_2206_);
v___x_2211_ = v_reuseFailAlloc_2212_;
goto v_reusejp_2210_;
}
v_reusejp_2210_:
{
return v___x_2211_;
}
}
}
}
else
{
lean_object* v_a_2214_; lean_object* v___x_2216_; uint8_t v_isShared_2217_; uint8_t v_isSharedCheck_2221_; 
lean_dec(v_a_2179_);
v_a_2214_ = lean_ctor_get(v___x_2180_, 0);
v_isSharedCheck_2221_ = !lean_is_exclusive(v___x_2180_);
if (v_isSharedCheck_2221_ == 0)
{
v___x_2216_ = v___x_2180_;
v_isShared_2217_ = v_isSharedCheck_2221_;
goto v_resetjp_2215_;
}
else
{
lean_inc(v_a_2214_);
lean_dec(v___x_2180_);
v___x_2216_ = lean_box(0);
v_isShared_2217_ = v_isSharedCheck_2221_;
goto v_resetjp_2215_;
}
v_resetjp_2215_:
{
lean_object* v___x_2219_; 
if (v_isShared_2217_ == 0)
{
v___x_2219_ = v___x_2216_;
goto v_reusejp_2218_;
}
else
{
lean_object* v_reuseFailAlloc_2220_; 
v_reuseFailAlloc_2220_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2220_, 0, v_a_2214_);
v___x_2219_ = v_reuseFailAlloc_2220_;
goto v_reusejp_2218_;
}
v_reusejp_2218_:
{
return v___x_2219_;
}
}
}
}
else
{
lean_object* v_a_2222_; lean_object* v___x_2224_; uint8_t v_isShared_2225_; uint8_t v_isSharedCheck_2229_; 
lean_dec(v_a_2176_);
lean_dec(v___y_2174_);
lean_dec_ref(v___y_2173_);
lean_dec_ref(v___y_2171_);
v_a_2222_ = lean_ctor_get(v___x_2178_, 0);
v_isSharedCheck_2229_ = !lean_is_exclusive(v___x_2178_);
if (v_isSharedCheck_2229_ == 0)
{
v___x_2224_ = v___x_2178_;
v_isShared_2225_ = v_isSharedCheck_2229_;
goto v_resetjp_2223_;
}
else
{
lean_inc(v_a_2222_);
lean_dec(v___x_2178_);
v___x_2224_ = lean_box(0);
v_isShared_2225_ = v_isSharedCheck_2229_;
goto v_resetjp_2223_;
}
v_resetjp_2223_:
{
lean_object* v___x_2227_; 
if (v_isShared_2225_ == 0)
{
v___x_2227_ = v___x_2224_;
goto v_reusejp_2226_;
}
else
{
lean_object* v_reuseFailAlloc_2228_; 
v_reuseFailAlloc_2228_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2228_, 0, v_a_2222_);
v___x_2227_ = v_reuseFailAlloc_2228_;
goto v_reusejp_2226_;
}
v_reusejp_2226_:
{
return v___x_2227_;
}
}
}
}
else
{
lean_object* v_a_2230_; lean_object* v___x_2232_; uint8_t v_isShared_2233_; uint8_t v_isSharedCheck_2237_; 
lean_dec(v___y_2174_);
lean_dec_ref(v___y_2173_);
lean_dec_ref(v___y_2171_);
v_a_2230_ = lean_ctor_get(v___x_2175_, 0);
v_isSharedCheck_2237_ = !lean_is_exclusive(v___x_2175_);
if (v_isSharedCheck_2237_ == 0)
{
v___x_2232_ = v___x_2175_;
v_isShared_2233_ = v_isSharedCheck_2237_;
goto v_resetjp_2231_;
}
else
{
lean_inc(v_a_2230_);
lean_dec(v___x_2175_);
v___x_2232_ = lean_box(0);
v_isShared_2233_ = v_isSharedCheck_2237_;
goto v_resetjp_2231_;
}
v_resetjp_2231_:
{
lean_object* v___x_2235_; 
if (v_isShared_2233_ == 0)
{
v___x_2235_ = v___x_2232_;
goto v_reusejp_2234_;
}
else
{
lean_object* v_reuseFailAlloc_2236_; 
v_reuseFailAlloc_2236_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2236_, 0, v_a_2230_);
v___x_2235_ = v_reuseFailAlloc_2236_;
goto v_reusejp_2234_;
}
v_reusejp_2234_:
{
return v___x_2235_;
}
}
}
}
v___jp_2238_:
{
size_t v_sz_2240_; size_t v___x_2241_; lean_object* v___x_2242_; size_t v_sz_2243_; lean_object* v___x_2244_; lean_object* v___x_2245_; uint32_t v___x_2246_; lean_object* v___x_2247_; uint8_t v___x_2248_; uint8_t v___x_2249_; lean_object* v___x_2250_; lean_object* v___x_2251_; 
v_sz_2240_ = lean_array_size(v___y_2239_);
v___x_2241_ = ((size_t)0ULL);
v___x_2242_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__0(v_sz_2240_, v___x_2241_, v___y_2239_);
v_sz_2243_ = lean_array_size(v___x_2242_);
v___x_2244_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__1(v_sz_2243_, v___x_2241_, v___x_2242_);
v___x_2245_ = l_Lean_Options_empty;
v___x_2246_ = 1024;
v___x_2247_ = ((lean_object*)(l_StmtKeys_main___closed__5));
v___x_2248_ = 0;
v___x_2249_ = 2;
v___x_2250_ = lean_box(1);
v___x_2251_ = l_Lean_importModules(v___x_2244_, v___x_2245_, v___x_2246_, v___x_2247_, v___x_2248_, v___x_2248_, v___x_2249_, v___x_2250_);
if (lean_obj_tag(v___x_2251_) == 0)
{
lean_object* v_a_2252_; lean_object* v___x_2253_; lean_object* v___x_2254_; lean_object* v_map_u2081_2255_; lean_object* v_buckets_2256_; lean_object* v___x_2257_; size_t v_sz_2258_; lean_object* v___x_2259_; lean_object* v___x_2260_; lean_object* v___x_2261_; uint8_t v___x_2262_; 
v_a_2252_ = lean_ctor_get(v___x_2251_, 0);
lean_inc_n(v_a_2252_, 2);
lean_dec_ref_known(v___x_2251_, 1);
v___x_2253_ = l_Lean_Environment_header(v_a_2252_);
v___x_2254_ = l_Lean_Environment_constants(v_a_2252_);
v_map_u2081_2255_ = lean_ctor_get(v___x_2254_, 0);
lean_inc_ref(v_map_u2081_2255_);
lean_dec_ref(v___x_2254_);
v_buckets_2256_ = lean_ctor_get(v_map_u2081_2255_, 1);
lean_inc_ref(v_buckets_2256_);
lean_dec_ref(v_map_u2081_2255_);
v___x_2257_ = l_Lean_EnvironmentHeader_moduleNames(v___x_2253_);
v_sz_2258_ = lean_array_size(v___x_2257_);
v___x_2259_ = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00StmtKeys_main_spec__2(v_sz_2258_, v___x_2241_, v___x_2257_);
v___x_2260_ = lean_obj_once(&l_StmtKeys_main___closed__6, &l_StmtKeys_main___closed__6_once, _init_l_StmtKeys_main___closed__6);
v___x_2261_ = lean_array_get_size(v_buckets_2256_);
v___x_2262_ = lean_nat_dec_lt(v___x_2169_, v___x_2261_);
if (v___x_2262_ == 0)
{
lean_dec_ref(v_buckets_2256_);
v___y_2171_ = v_a_2252_;
v___y_2172_ = v___x_2260_;
v___y_2173_ = v___x_2259_;
v___y_2174_ = v___x_2164_;
goto v___jp_2170_;
}
else
{
size_t v___x_2263_; lean_object* v___x_2264_; 
v___x_2263_ = lean_usize_of_nat(v___x_2261_);
v___x_2264_ = l___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00Lean_Kernel_Environment_replay_spec__2(v_buckets_2256_, v___x_2263_, v___x_2241_, v___x_2164_);
lean_dec_ref(v_buckets_2256_);
v___y_2171_ = v_a_2252_;
v___y_2172_ = v___x_2260_;
v___y_2173_ = v___x_2259_;
v___y_2174_ = v___x_2264_;
goto v___jp_2170_;
}
}
else
{
lean_object* v_a_2265_; lean_object* v___x_2267_; uint8_t v_isShared_2268_; uint8_t v_isSharedCheck_2272_; 
v_a_2265_ = lean_ctor_get(v___x_2251_, 0);
v_isSharedCheck_2272_ = !lean_is_exclusive(v___x_2251_);
if (v_isSharedCheck_2272_ == 0)
{
v___x_2267_ = v___x_2251_;
v_isShared_2268_ = v_isSharedCheck_2272_;
goto v_resetjp_2266_;
}
else
{
lean_inc(v_a_2265_);
lean_dec(v___x_2251_);
v___x_2267_ = lean_box(0);
v_isShared_2268_ = v_isSharedCheck_2272_;
goto v_resetjp_2266_;
}
v_resetjp_2266_:
{
lean_object* v___x_2270_; 
if (v_isShared_2268_ == 0)
{
v___x_2270_ = v___x_2267_;
goto v_reusejp_2269_;
}
else
{
lean_object* v_reuseFailAlloc_2271_; 
v_reuseFailAlloc_2271_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2271_, 0, v_a_2265_);
v___x_2270_ = v_reuseFailAlloc_2271_;
goto v_reusejp_2269_;
}
v_reusejp_2269_:
{
return v___x_2270_;
}
}
}
}
}
else
{
lean_object* v_a_2283_; lean_object* v___x_2285_; uint8_t v_isShared_2286_; uint8_t v_isSharedCheck_2290_; 
v_a_2283_ = lean_ctor_get(v___x_2167_, 0);
v_isSharedCheck_2290_ = !lean_is_exclusive(v___x_2167_);
if (v_isSharedCheck_2290_ == 0)
{
v___x_2285_ = v___x_2167_;
v_isShared_2286_ = v_isSharedCheck_2290_;
goto v_resetjp_2284_;
}
else
{
lean_inc(v_a_2283_);
lean_dec(v___x_2167_);
v___x_2285_ = lean_box(0);
v_isShared_2286_ = v_isSharedCheck_2290_;
goto v_resetjp_2284_;
}
v_resetjp_2284_:
{
lean_object* v___x_2288_; 
if (v_isShared_2286_ == 0)
{
v___x_2288_ = v___x_2285_;
goto v_reusejp_2287_;
}
else
{
lean_object* v_reuseFailAlloc_2289_; 
v_reuseFailAlloc_2289_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2289_, 0, v_a_2283_);
v___x_2288_ = v_reuseFailAlloc_2289_;
goto v_reusejp_2287_;
}
v_reusejp_2287_:
{
return v___x_2288_;
}
}
}
}
else
{
lean_object* v_a_2291_; lean_object* v___x_2293_; uint8_t v_isShared_2294_; uint8_t v_isSharedCheck_2298_; 
v_a_2291_ = lean_ctor_get(v___x_2165_, 0);
v_isSharedCheck_2298_ = !lean_is_exclusive(v___x_2165_);
if (v_isSharedCheck_2298_ == 0)
{
v___x_2293_ = v___x_2165_;
v_isShared_2294_ = v_isSharedCheck_2298_;
goto v_resetjp_2292_;
}
else
{
lean_inc(v_a_2291_);
lean_dec(v___x_2165_);
v___x_2293_ = lean_box(0);
v_isShared_2294_ = v_isSharedCheck_2298_;
goto v_resetjp_2292_;
}
v_resetjp_2292_:
{
lean_object* v___x_2296_; 
if (v_isShared_2294_ == 0)
{
v___x_2296_ = v___x_2293_;
goto v_reusejp_2295_;
}
else
{
lean_object* v_reuseFailAlloc_2297_; 
v_reuseFailAlloc_2297_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2297_, 0, v_a_2291_);
v___x_2296_ = v_reuseFailAlloc_2297_;
goto v_reusejp_2295_;
}
v_reusejp_2295_:
{
return v___x_2296_;
}
}
}
}
else
{
lean_object* v_a_2299_; lean_object* v___x_2301_; uint8_t v_isShared_2302_; uint8_t v_isSharedCheck_2306_; 
v_a_2299_ = lean_ctor_get(v___x_2162_, 0);
v_isSharedCheck_2306_ = !lean_is_exclusive(v___x_2162_);
if (v_isSharedCheck_2306_ == 0)
{
v___x_2301_ = v___x_2162_;
v_isShared_2302_ = v_isSharedCheck_2306_;
goto v_resetjp_2300_;
}
else
{
lean_inc(v_a_2299_);
lean_dec(v___x_2162_);
v___x_2301_ = lean_box(0);
v_isShared_2302_ = v_isSharedCheck_2306_;
goto v_resetjp_2300_;
}
v_resetjp_2300_:
{
lean_object* v___x_2304_; 
if (v_isShared_2302_ == 0)
{
v___x_2304_ = v___x_2301_;
goto v_reusejp_2303_;
}
else
{
lean_object* v_reuseFailAlloc_2305_; 
v_reuseFailAlloc_2305_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_2305_, 0, v_a_2299_);
v___x_2304_ = v_reuseFailAlloc_2305_;
goto v_reusejp_2303_;
}
v_reusejp_2303_:
{
return v___x_2304_;
}
}
}
}
else
{
goto v___jp_2154_;
}
}
else
{
goto v___jp_2154_;
}
}
else
{
goto v___jp_2154_;
}
v___jp_2154_:
{
lean_object* v___x_2155_; lean_object* v___x_2156_; 
v___x_2155_ = ((lean_object*)(l_StmtKeys_main___closed__1));
v___x_2156_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_2156_, 0, v___x_2155_);
return v___x_2156_;
}
}
}
LEAN_EXPORT lean_object* l_StmtKeys_main___boxed(lean_object* v_args_2307_, lean_object* v_a_2308_){
_start:
{
lean_object* v_res_2309_; 
v_res_2309_ = l_StmtKeys_main(v_args_2307_);
lean_dec(v_args_2307_);
return v_res_2309_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3(lean_object* v_a_2310_, lean_object* v___x_2311_, lean_object* v_as_2312_, lean_object* v_as_x27_2313_, lean_object* v_b_2314_, lean_object* v_a_2315_){
_start:
{
lean_object* v___x_2317_; 
v___x_2317_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___redArg(v_a_2310_, v___x_2311_, v_as_x27_2313_, v_b_2314_);
return v___x_2317_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3___boxed(lean_object* v_a_2318_, lean_object* v___x_2319_, lean_object* v_as_2320_, lean_object* v_as_x27_2321_, lean_object* v_b_2322_, lean_object* v_a_2323_, lean_object* v___y_2324_){
_start:
{
lean_object* v_res_2325_; 
v_res_2325_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__3(v_a_2318_, v___x_2319_, v_as_2320_, v_as_x27_2321_, v_b_2322_, v_a_2323_);
lean_dec(v_as_x27_2321_);
lean_dec(v_as_2320_);
return v_res_2325_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6(lean_object* v_a_2326_, lean_object* v___x_2327_, lean_object* v_a_2328_, lean_object* v_a_2329_, lean_object* v_as_2330_, lean_object* v_as_x27_2331_, lean_object* v_b_2332_, lean_object* v_a_2333_){
_start:
{
lean_object* v___x_2335_; 
v___x_2335_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___redArg(v_a_2326_, v___x_2327_, v_a_2328_, v_a_2329_, v_as_x27_2331_, v_b_2332_);
return v___x_2335_;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6___boxed(lean_object* v_a_2336_, lean_object* v___x_2337_, lean_object* v_a_2338_, lean_object* v_a_2339_, lean_object* v_as_2340_, lean_object* v_as_x27_2341_, lean_object* v_b_2342_, lean_object* v_a_2343_, lean_object* v___y_2344_){
_start:
{
lean_object* v_res_2345_; 
v_res_2345_ = l_List_forIn_x27_loop___at___00StmtKeys_main_spec__6(v_a_2336_, v___x_2337_, v_a_2338_, v_a_2339_, v_as_2340_, v_as_x27_2341_, v_b_2342_, v_a_2343_);
lean_dec(v_as_x27_2341_);
lean_dec(v_as_2340_);
lean_dec(v_a_2339_);
return v_res_2345_;
}
}
LEAN_EXPORT lean_object* _lean_main(lean_object* v_args_2346_){
_start:
{
lean_object* v___x_2348_; 
v___x_2348_ = l_StmtKeys_main(v_args_2346_);
lean_dec(v_args_2346_);
return v___x_2348_;
}
}
LEAN_EXPORT lean_object* l_main___boxed(lean_object* v_args_2349_, lean_object* v_a_2350_){
_start:
{
lean_object* v_res_2351_; 
v_res_2351_ = _lean_main(v_args_2349_);
return v_res_2351_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Lean(uint8_t builtin);
void lean_initialize();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_StmtKeys(uint8_t builtin) {
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
l_StmtKeys_tokNum = _init_l_StmtKeys_tokNum();
l_StmtKeys_tokLit = _init_l_StmtKeys_tokLit();
l_StmtKeys_tokHoleProv = _init_l_StmtKeys_tokHoleProv();
l_StmtKeys_tokVarProv = _init_l_StmtKeys_tokVarProv();
l_StmtKeys_main___boxed__const__1 = _init_l_StmtKeys_main___boxed__const__1();
lean_mark_persistent(l_StmtKeys_main___boxed__const__1);
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
  res = initialize_StmtKeys(1 /* builtin */);
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
