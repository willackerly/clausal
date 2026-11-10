import Euler.H5RealCylinderAlgebra
import ReuseCheck

/-!
F2. A threshold proved twice.

`Euler/GeneralCylinderAlgebra.lean` and `Euler/GeneralRealCylinderAlgebra.lean` prove nine
estimates for Sobolev order `q ≥ 6`; `Euler/H5CylinderAlgebra.lean` and
`Euler/H5RealCylinderAlgebra.lean` prove the same nine for `q ≥ 5` by copying the proofs
(the second pair of files imports the first).  The `q ≥ 5` statements are the general ones: no new
lemma has to be written, each `q ≥ 6` theorem is one line from its `q ≥ 5` twin.
-/

#follows "cyl" ["EulerGeneralCylinderAlgebra.product_tensor_term_le"] :=
  by intro period _ q n j hq; exact EulerH5CylinderAlgebra.product_tensor_term_le period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.product_word_pointwise_le"] :=
  by intro period _ q n hq; exact EulerH5CylinderAlgebra.product_word_pointwise_le period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.product_word_memLp"] :=
  by intro period _ q n hq; exact EulerH5CylinderAlgebra.product_word_memLp period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.product_word_L2_le"] :=
  by intro period _ q n hq; exact EulerH5CylinderAlgebra.product_word_L2_le period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.cylinder_Hq_algebra"] :=
  by intro period _ q hq; exact EulerH5CylinderAlgebra.cylinder_Hq_algebra period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.real_cylinder_Hq_algebra"] :=
  by intro period _ q hq; exact EulerH5CylinderAlgebra.real_cylinder_Hq_algebra period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.real_product_word_memLp"] :=
  by intro period _ q n hq; exact EulerH5CylinderAlgebra.real_product_word_memLp period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.scalar_vector_product_word_memLp"] :=
  by intro period _ q n hq; exact EulerH5CylinderAlgebra.scalar_vector_product_word_memLp period (by omega)
#follows "cyl" ["EulerGeneralCylinderAlgebra.cylinder_Hq_scalar_vector_product"] :=
  by intro period _ q hq; exact EulerH5CylinderAlgebra.cylinder_Hq_scalar_vector_product period (by omega)
