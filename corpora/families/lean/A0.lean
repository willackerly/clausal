import Euler.EulerProof
import NavierStokes.ActivationContinuation
import NavierStokes.ActualBaseResidual
import NavierStokes.ActualCandidateConstruction
import NavierStokes.ActualCarrierGeometry
import NavierStokes.ActualCarrierTransportBase
import NavierStokes.ActualCopySliceRegularity
import NavierStokes.ActualCoreSupport
import NavierStokes.ActualCurrentCarrierJets
import NavierStokes.ActualCurrentParticularBounds
import NavierStokes.ActualCurrentParticularPhysical
import NavierStokes.ActualCurrentWaveSupport
import NavierStokes.ActualCycleAssembly
import NavierStokes.ActualCycleCoherence
import NavierStokes.ActualCycleExcluded
import NavierStokes.ActualCycleParameters
import NavierStokes.ActualCyclePeriodicity
import NavierStokes.ActualCyclePreservation
import NavierStokes.ActualCycleResidualBounds
import NavierStokes.ActualInitialCoherence
import NavierStokes.ActualInitialExcluded
import NavierStokes.ActualInitialMean
import NavierStokes.ActualInitialMeanEquation
import NavierStokes.ActualInitialization
import NavierStokes.ActualIntermediateDebtBounds
import NavierStokes.ActualMeanPhysicalData
import NavierStokes.ActualMeanPotentialRealization
import NavierStokes.ActualParticularBackground
import NavierStokes.ActualParticularControl
import NavierStokes.ActualParticularCycleData
import NavierStokes.ActualParticularMeanGain
import NavierStokes.ActualParticularRealization
import NavierStokes.ActualParticularStageControls
import NavierStokes.ActualPeriodizedSignedRealization
import NavierStokes.ActualPhaseDefect
import NavierStokes.ActualPhaseJetBounds
import NavierStokes.ActualPhysicalPrefixFields
import NavierStokes.ActualPolarCoverage
import NavierStokes.ActualPrimaryBounds
import NavierStokes.ActualPrimaryCoherence
import NavierStokes.ActualPrimaryCovariance
import NavierStokes.ActualPrimaryDynamics
import NavierStokes.ActualSeedPeriodicity
import NavierStokes.ActualSignedCoherence
import NavierStokes.ActualSignedControl
import NavierStokes.ActualSignedCurrentSupport
import NavierStokes.ActualSignedDynamics
import NavierStokes.ActualSignedExterior
import NavierStokes.ActualSignedFamilySupport
import NavierStokes.ActualSignedGeometry
import NavierStokes.ActualSignedMeanBinding
import NavierStokes.ActualSignedNativeBounds
import NavierStokes.ActualSignedNativeProfiles
import NavierStokes.ActualSignedNativeRegularity
import NavierStokes.ActualSignedPhysicalBinding
import NavierStokes.ActualSignedPhysicalCoherence
import NavierStokes.ActualSignedPhysicalData
import NavierStokes.ActualSignedPhysicalZeros
import NavierStokes.ActualSignedPotentialCoherence
import NavierStokes.ActualSignedReferenceGeometry
import NavierStokes.ActualSignedStageControls
import NavierStokes.ActualSignedUnmaskedBinding
import NavierStokes.ActualSignedUnmaskedBounds
import NavierStokes.ActualSignedWaveData
import NavierStokes.ActualWaveCoefficientPeriodicity
import NavierStokes.ActualWaveRegularity
import NavierStokes.ActualWaveRegularityData
import NavierStokes.AllBandBaseJets
import NavierStokes.AngularMomentReset
import NavierStokes.AnnularEndpoint
import NavierStokes.AxisymmetricFields
import NavierStokes.BaseChartJets
import NavierStokes.BaseContextAssembly
import NavierStokes.BasePhaseGeometry
import NavierStokes.BaseRadialJets
import NavierStokes.BaseStressClasses
import NavierStokes.CartesianCopySource
import NavierStokes.CommonBaseContext
import NavierStokes.CorrectionAnalyticStep
import NavierStokes.CorrectionInitialization
import NavierStokes.CorrectionState
import NavierStokes.CorrectionStep
import NavierStokes.CrossBasedMeanComposition
import NavierStokes.CurlClassBounds
import NavierStokes.CurrentParticularLabelBounds
import NavierStokes.CurrentPhysicalChartJets
import NavierStokes.CurrentPhysicalModeGerms
import NavierStokes.CurrentSignedCurl
import NavierStokes.CycleMeanEquation
import NavierStokes.CyclePhysicalPrefixes
import NavierStokes.CycleStateCoherence
import NavierStokes.DefectIncrementBounds
import NavierStokes.DirectAngularDiagonal
import NavierStokes.EndpointCoordinates
import NavierStokes.ExtendedHeatedOutgoing
import NavierStokes.FiveProfileMoments
import NavierStokes.FiveRowRank
import NavierStokes.FourierAlias
import NavierStokes.GaugeAliasDecay
import NavierStokes.GaugeDebtIncrement
import NavierStokes.GaugeExcludedBounds
import NavierStokes.GaugeMassPreservation
import NavierStokes.GaugeMomentBalances
import NavierStokes.GaugeRadialResidualBounds
import NavierStokes.GaugeStateCoherence
import NavierStokes.GaussianErrorNaturality
import NavierStokes.GlobalSlowProfiles
import NavierStokes.GrowingMode
import NavierStokes.HeatSwitchCone
import NavierStokes.HeatedOutgoing
import NavierStokes.InitialNativeRegularity
import NavierStokes.InitialPhysicalData
import NavierStokes.JointResidualLimits
import NavierStokes.LocalRankDefect
import NavierStokes.LocalSignedRequest
import NavierStokes.MatchingDebtBounds
import NavierStokes.MeanIncrementBounds
import NavierStokes.MeanRankUpdate
import NavierStokes.MeanStageRegularity
import NavierStokes.MeanStateRegularity
import NavierStokes.ModulatedHistories
import NavierStokes.ModulatedStockBounds
import NavierStokes.MovingFrameODE
import NavierStokes.NativeBandExtension
import NavierStokes.NominalProfile
import NavierStokes.OffplaneCorrectionExtensions
import NavierStokes.OutgoingHistories
import NavierStokes.ParametricEvenDescent
import NavierStokes.ParametricModulation
import NavierStokes.ParametricRadialExtension
import NavierStokes.ParametricTorusInverse
import NavierStokes.PartitionedCovariance
import NavierStokes.PeriodicIntegration
import NavierStokes.PhaseCalculus
import NavierStokes.PhaseEstimates
import NavierStokes.PhaseJetBounds
import NavierStokes.PhysicalCoordinateBounds
import NavierStokes.PhysicalCurlCovariance
import NavierStokes.PhysicalGraphBounds
import NavierStokes.PhysicalParticularWave
import NavierStokes.PhysicalResidualBridge
import NavierStokes.PhysicalResidualJetBounds
import NavierStokes.PhysicalResidualNaturality
import NavierStokes.PhysicalResidualTZ
import NavierStokes.PhysicalSignedWave
import NavierStokes.PhysicalWaveSum
import NavierStokes.PolarCharts
import NavierStokes.PositiveOrderMoments
import NavierStokes.PositiveRepresentatives
import NavierStokes.PositiveTimeCopyFamily
import NavierStokes.PositiveTimeSignedLocalization
import NavierStokes.PressureStream
import NavierStokes.PrimaryCopyBridge
import NavierStokes.PrimaryCovarianceBounds
import NavierStokes.PrimaryFieldAssembly
import NavierStokes.PrimaryGeometryAssembly
import NavierStokes.PrimaryMaterialDefect
import NavierStokes.PrimaryODE
import NavierStokes.PrimaryPulseBounds
import NavierStokes.PrimaryRepresentatives
import NavierStokes.PrimaryTargetBounds
import NavierStokes.ProblemStatement
import NavierStokes.ProfileHistories
import NavierStokes.ProfileSpectralCone
import NavierStokes.PulseCovariance
import NavierStokes.R3.ProblemStatement
import NavierStokes.RadialModulation
import NavierStokes.RankStateBounds
import NavierStokes.RepairConeBounds
import NavierStokes.ScaledActualParticularControl
import NavierStokes.ScaledParticularFrameJets
import NavierStokes.SignedCopyBounds
import NavierStokes.SignedCovariance
import NavierStokes.SignedMeanGain
import NavierStokes.SignedWaveUpdate
import NavierStokes.SimilarityHomogeneity
import NavierStokes.SimilarityProfile
import NavierStokes.SlotColoring
import NavierStokes.SlotGeometry
import NavierStokes.SlowBorelBase
import NavierStokes.SlowFirstOrderEdge
import NavierStokes.SlowStressSupport
import NavierStokes.SmoothCovariance
import NavierStokes.SpacetimeEndpoint
import NavierStokes.SpacetimeGluing
import NavierStokes.TailGaugePotential
import NavierStokes.TemporalStateCoherence
import NavierStokes.TerminalCompensation
import NavierStokes.TerminalEdgeFactor
import NavierStokes.TerminalStress
import NavierStokes.TorusInverse
import NavierStokes.TorusMeanRequestRebase
import NavierStokes.UniformCone
import NavierStokes.ViscousPropagator
import NavierStokes.WaveEdgeExtension

run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCandidateConstruction.Point"
example : @NavierStokes.ActualCandidateConstruction.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCarrierGeometry.Point"
example : @NavierStokes.ActualCarrierGeometry.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCarrierTransportBase.Point"
example : @NavierStokes.ActualCarrierTransportBase.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCoreSupport.Point"
example : @NavierStokes.ActualCoreSupport.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCurrentWaveSupport.Point"
example : @NavierStokes.ActualCurrentWaveSupport.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCycleAssembly.Point"
example : @NavierStokes.ActualCycleAssembly.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCycleCoherence.Point"
example : @NavierStokes.ActualCycleCoherence.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCycleExcluded.Point"
example : @NavierStokes.ActualCycleExcluded.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCyclePeriodicity.Point"
example : @NavierStokes.ActualCyclePeriodicity.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCyclePreservation.Point"
example : @NavierStokes.ActualCyclePreservation.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualCycleResidualBounds.Point"
example : @NavierStokes.ActualCycleResidualBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualInitialCoherence.Point"
example : @NavierStokes.ActualInitialCoherence.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualInitialMean.Point"
example : @NavierStokes.ActualInitialMean.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualInitialMeanEquation.Point"
example : @NavierStokes.ActualInitialMeanEquation.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualInitialization.Point"
example : @NavierStokes.ActualInitialization.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualIntermediateDebtBounds.Point"
example : @NavierStokes.ActualIntermediateDebtBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualMeanPhysicalData.Point"
example : @NavierStokes.ActualMeanPhysicalData.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualMeanPotentialRealization.Point"
example : @NavierStokes.ActualMeanPotentialRealization.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualParticularCycleData.Point"
example : @NavierStokes.ActualParticularCycleData.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualParticularMeanGain.Point"
example : @NavierStokes.ActualParticularMeanGain.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualPhysicalPrefixFields.Point"
example : @NavierStokes.ActualPhysicalPrefixFields.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualPolarCoverage.Point"
example : @NavierStokes.ActualPolarCoverage.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualPrimaryBounds.Point"
example : @NavierStokes.ActualPrimaryBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualPrimaryCovariance.Point"
example : @NavierStokes.ActualPrimaryCovariance.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSeedPeriodicity.Point"
example : @NavierStokes.ActualSeedPeriodicity.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedCoherence.Point"
example : @NavierStokes.ActualSignedCoherence.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedCurrentSupport.Point"
example : @NavierStokes.ActualSignedCurrentSupport.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedMeanBinding.Point"
example : @NavierStokes.ActualSignedMeanBinding.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedNativeBounds.Native"
example : @NavierStokes.ActualSignedNativeBounds.Native = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedNativeRegularity.Native"
example : @NavierStokes.ActualSignedNativeRegularity.Native = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedPhysicalBinding.Point"
example : @NavierStokes.ActualSignedPhysicalBinding.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedPhysicalCoherence.Point"
example : @NavierStokes.ActualSignedPhysicalCoherence.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedPhysicalData.Native"
example : @NavierStokes.ActualSignedPhysicalData.Native = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedPhysicalZeros.Point"
example : @NavierStokes.ActualSignedPhysicalZeros.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedPotentialCoherence.Point"
example : @NavierStokes.ActualSignedPotentialCoherence.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedStageControls.Point"
example : @NavierStokes.ActualSignedStageControls.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedUnmaskedBinding.Native"
example : @NavierStokes.ActualSignedUnmaskedBinding.Native = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualSignedUnmaskedBinding.Point"
example : @NavierStokes.ActualSignedUnmaskedBinding.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualWaveCoefficientPeriodicity.Point"
example : @NavierStokes.ActualWaveCoefficientPeriodicity.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualWaveRegularity.Point"
example : @NavierStokes.ActualWaveRegularity.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.ActualWaveRegularityData.Point"
example : @NavierStokes.ActualWaveRegularityData.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.BaseContextAssembly.Point"
example : @NavierStokes.BaseContextAssembly.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.BaseStressClasses.Point"
example : @NavierStokes.BaseStressClasses.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CartesianCopySource.Native"
example : @NavierStokes.CartesianCopySource.Native = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CommonBaseContext.Point"
example : @NavierStokes.CommonBaseContext.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CorrectionAnalyticStep.Point"
example : @NavierStokes.CorrectionAnalyticStep.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CorrectionStep.CyclePoint"
example : @NavierStokes.CorrectionStep.CyclePoint = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CrossBasedMeanComposition.Point"
example : @NavierStokes.CrossBasedMeanComposition.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CurrentSignedCurl.Point"
example : @NavierStokes.CurrentSignedCurl.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CycleMeanEquation.Point"
example : @NavierStokes.CycleMeanEquation.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.CycleStateCoherence.Point"
example : @NavierStokes.CycleStateCoherence.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.GaugeDebtIncrement.Point"
example : @NavierStokes.GaugeDebtIncrement.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.GaugeExcludedBounds.Point"
example : @NavierStokes.GaugeExcludedBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.GaugeMassPreservation.Point"
example : @NavierStokes.GaugeMassPreservation.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.GaugeMomentBalances.Point"
example : @NavierStokes.GaugeMomentBalances.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.GaugeRadialResidualBounds.Point"
example : @NavierStokes.GaugeRadialResidualBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.LocalSignedRequest.Point"
example : @NavierStokes.LocalSignedRequest.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.MeanRankUpdate.ChartPoint"
example : @NavierStokes.MeanRankUpdate.ChartPoint = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.MeanStageRegularity.Point"
example : @NavierStokes.MeanStageRegularity.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.MeanStateRegularity.Point"
example : @NavierStokes.MeanStateRegularity.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalClassBounds.CylindricalPoint"
example : @NavierStokes.PhysicalClassBounds.CylindricalPoint = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalMeanJetBounds.Point"
example : @NavierStokes.PhysicalMeanJetBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalParticularWave.Lift"
example : @NavierStokes.PhysicalParticularWave.Lift = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalResidualBridge.Lift"
example : @NavierStokes.PhysicalResidualBridge.Lift = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalResidualJetBounds.Point"
example : @NavierStokes.PhysicalResidualJetBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalResidualNaturality.Lift"
example : @NavierStokes.PhysicalResidualNaturality.Lift = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalResidualTZ.Lift"
example : @NavierStokes.PhysicalResidualTZ.Lift = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PhysicalSignedWave.Point"
example : @NavierStokes.PhysicalSignedWave.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.PositiveTimeSignedLocalization.Native"
example : @NavierStokes.PositiveTimeSignedLocalization.Native = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.RankStateBounds.Point"
example : @NavierStokes.RankStateBounds.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.SignedCrossDefectClass.Point"
example : @NavierStokes.SignedCrossDefectClass.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.SignedMeanGain.Point"
example : @NavierStokes.SignedMeanGain.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.TorusMeanRequestRebase.Point"
example : @NavierStokes.TorusMeanRequestRebase.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00001 NavierStokes.WaveStateRegularity.Point"
example : @NavierStokes.WaveStateRegularity.Point = @NavierStokes.ActualBaseResidual.Point := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualCopySliceRegularity.Plane"
example : @NavierStokes.ActualCopySliceRegularity.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualInitialCoherence.Plane"
example : @NavierStokes.ActualInitialCoherence.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualMeanPhysicalData.Plane"
example : @NavierStokes.ActualMeanPhysicalData.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualParticularControl.Plane"
example : @NavierStokes.ActualParticularControl.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualParticularRealization.Plane"
example : @NavierStokes.ActualParticularRealization.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualParticularStageControls.Plane"
example : @NavierStokes.ActualParticularStageControls.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualPeriodizedSignedRealization.Plane"
example : @NavierStokes.ActualPeriodizedSignedRealization.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualPhaseDefect.Plane"
example : @NavierStokes.ActualPhaseDefect.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualPrimaryCovariance.Plane"
example : @NavierStokes.ActualPrimaryCovariance.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualSignedGeometry.Plane"
example : @NavierStokes.ActualSignedGeometry.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualSignedPhysicalBinding.Plane"
example : @NavierStokes.ActualSignedPhysicalBinding.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualSignedPhysicalData.Plane"
example : @NavierStokes.ActualSignedPhysicalData.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ActualSignedStageControls.Plane"
example : @NavierStokes.ActualSignedStageControls.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.BaseChartJets.Inner"
example : @NavierStokes.BaseChartJets.Inner = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.BaseContextAssembly.Plane"
example : @NavierStokes.BaseContextAssembly.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.BaseStressClasses.Inner"
example : @NavierStokes.BaseStressClasses.Inner = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.CartesianCopySource.Plane"
example : @NavierStokes.CartesianCopySource.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.CommonBaseContext.Plane"
example : @NavierStokes.CommonBaseContext.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.CurrentPhysicalChartJets.Plane"
example : @NavierStokes.CurrentPhysicalChartJets.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.CycleMeanEquation.Plane"
example : @NavierStokes.CycleMeanEquation.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.CycleStateCoherence.Plane"
example : @NavierStokes.CycleStateCoherence.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.DirectAngularDiagonal.Slow"
example : @NavierStokes.DirectAngularDiagonal.Slow = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.GaugeAliasDecay.Plane"
example : @NavierStokes.GaugeAliasDecay.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.GaugeDebtIncrement.Plane"
example : @NavierStokes.GaugeDebtIncrement.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.GaugeMassPreservation.Plane"
example : @NavierStokes.GaugeMassPreservation.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.GaugeMomentBalances.Plane"
example : @NavierStokes.GaugeMomentBalances.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.GaugeRadialResidualBounds.Plane"
example : @NavierStokes.GaugeRadialResidualBounds.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.GaugeStateCoherence.Plane"
example : @NavierStokes.GaugeStateCoherence.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.HeatSwitchCone.Point"
example : @NavierStokes.HeatSwitchCone.Point = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.LocalSignedRequest.Plane"
example : @NavierStokes.LocalSignedRequest.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.MatchingDebtBounds.Point"
example : @NavierStokes.MatchingDebtBounds.Point = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.MeanStageRegularity.Plane"
example : @NavierStokes.MeanStageRegularity.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.MeanStateRegularity.Plane"
example : @NavierStokes.MeanStateRegularity.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ModulatedHistories.Point"
example : @NavierStokes.ModulatedHistories.Point = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.NominalProfile.Point"
example : @NavierStokes.NominalProfile.Point = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.OutgoingHistories.Point"
example : @NavierStokes.OutgoingHistories.Point = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ParametricEvenDescent.Plane"
example : @NavierStokes.ParametricEvenDescent.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ParametricModulation.RadialParameter"
example : @NavierStokes.ParametricModulation.RadialParameter = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ParametricRadialExtension.Plane"
example : @NavierStokes.ParametricRadialExtension.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.PartitionedCovariance.Plane"
example : @NavierStokes.PartitionedCovariance.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.PhysicalGraphBounds.Plane"
example : @NavierStokes.PhysicalGraphBounds.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.PhysicalResidualBridge.Plane"
example : @NavierStokes.PhysicalResidualBridge.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.PhysicalWaveSum.Plane"
example : @NavierStokes.PhysicalWaveSum.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.PolarCharts.Plane"
example : @NavierStokes.PolarCharts.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.PressureStream.Plane"
example : @NavierStokes.PressureStream.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.PrimaryCopyBridge.Plane"
example : @NavierStokes.PrimaryCopyBridge.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ProfileHistories.Point"
example : @NavierStokes.ProfileHistories.Point = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.RankStateBounds.Plane"
example : @NavierStokes.RankStateBounds.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.RepairConeBounds.Point"
example : @NavierStokes.RepairConeBounds.Point = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ScaledActualParticularControl.Plane"
example : @NavierStokes.ScaledActualParticularControl.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.ScaledParticularFrameJets.Plane"
example : @NavierStokes.ScaledParticularFrameJets.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.SignedMeanGain.Plane"
example : @NavierStokes.SignedMeanGain.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.SimilarityProfile.InnerPoint"
example : @NavierStokes.SimilarityProfile.InnerPoint = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.SlotGeometry.Plane"
example : @NavierStokes.SlotGeometry.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.SlowBorelBase.Inner"
example : @NavierStokes.SlowBorelBase.Inner = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.TemporalStateCoherence.Plane"
example : @NavierStokes.TemporalStateCoherence.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.TerminalEdgeFactor.EdgeParam"
example : @NavierStokes.TerminalEdgeFactor.EdgeParam = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.TorusInverse.Plane"
example : @NavierStokes.TorusInverse.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00002 NavierStokes.TorusMeanRequestRebase.Plane"
example : @NavierStokes.TorusMeanRequestRebase.Plane = @NavierStokes.ActualCarrierTransportBase.Plane := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualCarrierTransportBase.Parameter"
example : @NavierStokes.ActualCarrierTransportBase.Parameter = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualCopySliceRegularity.Parameter"
example : @NavierStokes.ActualCopySliceRegularity.Parameter = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualInitialExcluded.Slow"
example : @NavierStokes.ActualInitialExcluded.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualParticularBackground.Parameter"
example : @NavierStokes.ActualParticularBackground.Parameter = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualParticularRealization.Parameter"
example : @NavierStokes.ActualParticularRealization.Parameter = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualParticularStageControls.Parameter"
example : @NavierStokes.ActualParticularStageControls.Parameter = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualParticularStageControls.Slow"
example : @NavierStokes.ActualParticularStageControls.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualPhaseDefect.Slow"
example : @NavierStokes.ActualPhaseDefect.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualPrimaryCovariance.Slow"
example : @NavierStokes.ActualPrimaryCovariance.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualSignedGeometry.Slow"
example : @NavierStokes.ActualSignedGeometry.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualSignedNativeProfiles.Slow"
example : @NavierStokes.ActualSignedNativeProfiles.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ActualSignedPhysicalBinding.Slow"
example : @NavierStokes.ActualSignedPhysicalBinding.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.AllBandBaseJets.Slow"
example : @NavierStokes.AllBandBaseJets.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.AxisymmetricFields.ProfilePoint"
example : @NavierStokes.AxisymmetricFields.ProfilePoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.BaseChartJets.Chart"
example : @NavierStokes.BaseChartJets.Chart = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.BaseChartJets.Slow"
example : @NavierStokes.BaseChartJets.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.BaseContextAssembly.Slow"
example : @NavierStokes.BaseContextAssembly.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.BasePhaseGeometry.Slow"
example : @NavierStokes.BasePhaseGeometry.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.BaseRadialJets.Slow"
example : @NavierStokes.BaseRadialJets.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.BaseStressClasses.Chart"
example : @NavierStokes.BaseStressClasses.Chart = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.CorrectionStep.CycleSlow"
example : @NavierStokes.CorrectionStep.CycleSlow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.DirectAngularDiagonal.CylPoint"
example : @NavierStokes.DirectAngularDiagonal.CylPoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.EndpointCoordinates.Chart"
example : @NavierStokes.EndpointCoordinates.Chart = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.EndpointCoordinates.PhysicalPoint"
example : @NavierStokes.EndpointCoordinates.PhysicalPoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.FourierAlias.State"
example : @NavierStokes.FourierAlias.State = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.GaussianErrorNaturality.Parameter"
example : @NavierStokes.GaussianErrorNaturality.Parameter = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.MeanRankUpdate.ModelPoint"
example : @NavierStokes.MeanRankUpdate.ModelPoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.NativeBandExtension.Slow"
example : @NavierStokes.NativeBandExtension.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ParametricTorusInverse.Point"
example : @NavierStokes.ParametricTorusInverse.Point = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PhaseCalculus.Slow"
example : @NavierStokes.PhaseCalculus.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PhaseEstimates.Slow"
example : @NavierStokes.PhaseEstimates.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PhaseJetBounds.Slow"
example : @NavierStokes.PhaseJetBounds.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PhysicalCoordinateBounds.Point"
example : @NavierStokes.PhysicalCoordinateBounds.Point = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PhysicalGraphBounds.Slow"
example : @NavierStokes.PhysicalGraphBounds.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PhysicalParticularWave.Parameter"
example : @NavierStokes.PhysicalParticularWave.Parameter = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PositiveRepresentatives.Slow"
example : @NavierStokes.PositiveRepresentatives.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PrimaryGeometryAssembly.Slow"
example : @NavierStokes.PrimaryGeometryAssembly.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PrimaryMaterialDefect.Slow"
example : @NavierStokes.PrimaryMaterialDefect.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PrimaryRepresentatives.Slow"
example : @NavierStokes.PrimaryRepresentatives.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.PrimaryTargetBounds.Slow"
example : @NavierStokes.PrimaryTargetBounds.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ProfileSpectralCone.Slow"
example : @NavierStokes.ProfileSpectralCone.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.RadialModulation.PhasePoint"
example : @NavierStokes.RadialModulation.PhasePoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ScaledActualParticularControl.Slow"
example : @NavierStokes.ScaledActualParticularControl.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.ScaledParticularFrameJets.Slow"
example : @NavierStokes.ScaledParticularFrameJets.Slow = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.SimilarityHomogeneity.ChartPoint"
example : @NavierStokes.SimilarityHomogeneity.ChartPoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.SimilarityProfile.PhysicalPoint"
example : @NavierStokes.SimilarityProfile.PhysicalPoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.SlowBorelBase.Chart"
example : @NavierStokes.SlowBorelBase.Chart = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.SlowFirstOrderEdge.PhysicalPoint"
example : @NavierStokes.SlowFirstOrderEdge.PhysicalPoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.TailGaugePotential.Point"
example : @NavierStokes.TailGaugePotential.Point = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.TerminalStress.PhysicalPoint"
example : @NavierStokes.TerminalStress.PhysicalPoint = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00003 NavierStokes.UniformCone.ConeDatum"
example : @NavierStokes.UniformCone.ConeDatum = @NavierStokes.ActualCarrierGeometry.Slow := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualCandidateConstruction.Full"
example : @NavierStokes.ActualCandidateConstruction.Full = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualCurrentCarrierJets.FullPoint"
example : @NavierStokes.ActualCurrentCarrierJets.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualCycleResidualBounds.Cylinder"
example : @NavierStokes.ActualCycleResidualBounds.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualInitialMeanEquation.Full"
example : @NavierStokes.ActualInitialMeanEquation.Full = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualMeanPotentialRealization.Cylinder"
example : @NavierStokes.ActualMeanPotentialRealization.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualParticularStageControls.AP"
example : @NavierStokes.ActualParticularStageControls.AP = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualPeriodizedSignedRealization.Cylinder"
example : @NavierStokes.ActualPeriodizedSignedRealization.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualPhaseDefect.Cylinder"
example : @NavierStokes.ActualPhaseDefect.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualPhysicalPrefixFields.Cylinder"
example : @NavierStokes.ActualPhysicalPrefixFields.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualPolarCoverage.Cylinder"
example : @NavierStokes.ActualPolarCoverage.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualPrimaryCoherence.ChartPoint"
example : @NavierStokes.ActualPrimaryCoherence.ChartPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedCoherence.FullPoint"
example : @NavierStokes.ActualSignedCoherence.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedCurrentSupport.FullPoint"
example : @NavierStokes.ActualSignedCurrentSupport.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedGeometry.Cylinder"
example : @NavierStokes.ActualSignedGeometry.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedMeanBinding.FullPoint"
example : @NavierStokes.ActualSignedMeanBinding.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedNativeBounds.Full"
example : @NavierStokes.ActualSignedNativeBounds.Full = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedNativeRegularity.FullPoint"
example : @NavierStokes.ActualSignedNativeRegularity.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedPhysicalBinding.Cylinder"
example : @NavierStokes.ActualSignedPhysicalBinding.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedPhysicalCoherence.FullPoint"
example : @NavierStokes.ActualSignedPhysicalCoherence.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedPhysicalData.Cylinder"
example : @NavierStokes.ActualSignedPhysicalData.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedPhysicalZeros.FullPoint"
example : @NavierStokes.ActualSignedPhysicalZeros.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedPotentialCoherence.FullPoint"
example : @NavierStokes.ActualSignedPotentialCoherence.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedStageControls.FullPoint"
example : @NavierStokes.ActualSignedStageControls.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedUnmaskedBinding.Cylinder"
example : @NavierStokes.ActualSignedUnmaskedBinding.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualSignedUnmaskedBounds.Full"
example : @NavierStokes.ActualSignedUnmaskedBounds.Full = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualWaveCoefficientPeriodicity.FullPoint"
example : @NavierStokes.ActualWaveCoefficientPeriodicity.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualWaveRegularity.Cylinder"
example : @NavierStokes.ActualWaveRegularity.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.ActualWaveRegularityData.FullPoint"
example : @NavierStokes.ActualWaveRegularityData.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.CorrectionInitialization.ActualPrimary.FullPoint"
example : @NavierStokes.CorrectionInitialization.ActualPrimary.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.CurrentSignedCurl.FullPoint"
example : @NavierStokes.CurrentSignedCurl.FullPoint = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.CyclePhysicalPrefixes.Cylinder"
example : @NavierStokes.CyclePhysicalPrefixes.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.InitialNativeRegularity.Point"
example : @NavierStokes.InitialNativeRegularity.Point = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.InitialPhysicalData.Point"
example : @NavierStokes.InitialPhysicalData.Point = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.PhysicalCurlCovariance.Cylinder"
example : @NavierStokes.PhysicalCurlCovariance.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.PhysicalParticularWave.Cylinder"
example : @NavierStokes.PhysicalParticularWave.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.PhysicalResidualBridge.Cylinder"
example : @NavierStokes.PhysicalResidualBridge.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.PhysicalResidualJetBounds.Cylinder"
example : @NavierStokes.PhysicalResidualJetBounds.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.PhysicalResidualTZ.Cylinder"
example : @NavierStokes.PhysicalResidualTZ.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.PhysicalSignedWave.Cylinder"
example : @NavierStokes.PhysicalSignedWave.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00005 NavierStokes.TorusMeanRequestRebase.Cylinder"
example : @NavierStokes.TorusMeanRequestRebase.Cylinder = @NavierStokes.ActualBaseResidual.Full := rfl
run_cmd IO.println "BLOCK F00006 EulerSmoothLimit.Space"
example : @EulerSmoothLimit.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ActualBaseResidual.Space"
example : @NavierStokes.ActualBaseResidual.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ActualCopySliceRegularity.Space"
example : @NavierStokes.ActualCopySliceRegularity.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ActualPeriodizedSignedRealization.Space"
example : @NavierStokes.ActualPeriodizedSignedRealization.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ActualPrimaryDynamics.Space"
example : @NavierStokes.ActualPrimaryDynamics.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ActualSignedControl.Space"
example : @NavierStokes.ActualSignedControl.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ActualSignedDynamics.Space"
example : @NavierStokes.ActualSignedDynamics.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ActualSignedStageControls.Space"
example : @NavierStokes.ActualSignedStageControls.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.AnnularEndpoint.Space"
example : @NavierStokes.AnnularEndpoint.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.BasePhaseGeometry.Space"
example : @NavierStokes.BasePhaseGeometry.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.CurlClassBounds.RealVector"
example : @NavierStokes.CurlClassBounds.RealVector = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.JointResidualLimits.Space"
example : @NavierStokes.JointResidualLimits.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.MovingFrameODE.Space"
example : @NavierStokes.MovingFrameODE.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.OffplaneCorrectionExtensions.Space"
example : @NavierStokes.OffplaneCorrectionExtensions.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.PhaseCalculus.Vec3"
example : @NavierStokes.PhaseCalculus.Vec3 = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.PhaseEstimates.Space"
example : @NavierStokes.PhaseEstimates.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.PhaseJetBounds.Space"
example : @NavierStokes.PhaseJetBounds.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.PrimaryCopyBridge.Space"
example : @NavierStokes.PrimaryCopyBridge.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.PrimaryODE.Space"
example : @NavierStokes.PrimaryODE.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.PrimaryPulseBounds.Space"
example : @NavierStokes.PrimaryPulseBounds.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ProblemStatement.Space"
example : @NavierStokes.ProblemStatement.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.ScaledParticularFrameJets.Space"
example : @NavierStokes.ScaledParticularFrameJets.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.SignedCopyBounds.Space"
example : @NavierStokes.SignedCopyBounds.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.SignedWaveUpdate.Space"
example : @NavierStokes.SignedWaveUpdate.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.SpacetimeEndpoint.Space"
example : @NavierStokes.SpacetimeEndpoint.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokes.SpacetimeGluing.Space"
example : @NavierStokes.SpacetimeGluing.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00006 NavierStokesR3.ProblemStatement.Space"
example : @NavierStokesR3.ProblemStatement.Space = @EulerLiftedGradientSpace.Vector3 := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualCoreSupport.Index"
example : @NavierStokes.ActualCoreSupport.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualCurrentWaveSupport.Index"
example : @NavierStokes.ActualCurrentWaveSupport.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualCycleAssembly.Index"
example : @NavierStokes.ActualCycleAssembly.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualCycleParameters.Index"
example : @NavierStokes.ActualCycleParameters.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualInitialMean.Index"
example : @NavierStokes.ActualInitialMean.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualInitialization.Index"
example : @NavierStokes.ActualInitialization.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualIntermediateDebtBounds.Index"
example : @NavierStokes.ActualIntermediateDebtBounds.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualParticularCycleData.Index"
example : @NavierStokes.ActualParticularCycleData.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualParticularMeanGain.Index"
example : @NavierStokes.ActualParticularMeanGain.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualSignedCoherence.SignedLabel"
example : @NavierStokes.ActualSignedCoherence.SignedLabel = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualSignedNativeRegularity.Label"
example : @NavierStokes.ActualSignedNativeRegularity.Label = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualSignedPhysicalBinding.Label"
example : @NavierStokes.ActualSignedPhysicalBinding.Label = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualSignedPhysicalCoherence.Label"
example : @NavierStokes.ActualSignedPhysicalCoherence.Label = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualSignedStageControls.SignedLabel"
example : @NavierStokes.ActualSignedStageControls.SignedLabel = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualSignedUnmaskedBounds.Label"
example : @NavierStokes.ActualSignedUnmaskedBounds.Label = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualWaveCoefficientPeriodicity.Index"
example : @NavierStokes.ActualWaveCoefficientPeriodicity.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00007 NavierStokes.ActualWaveRegularityData.Index"
example : @NavierStokes.ActualWaveRegularityData.Index = @NavierStokes.ActualCarrierTransportBase.Index := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ActivationContinuation.StockJet"
example : @NavierStokes.ActivationContinuation.StockJet = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ActualPeriodizedSignedRealization.Vec2"
example : @NavierStokes.ActualPeriodizedSignedRealization.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ActualSignedControl.Vec2"
example : @NavierStokes.ActualSignedControl.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ActualSignedMeanBinding.Vec2"
example : @NavierStokes.ActualSignedMeanBinding.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ActualSignedPhysicalData.Vec2"
example : @NavierStokes.ActualSignedPhysicalData.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.AngularMomentReset.Coeff"
example : @NavierStokes.AngularMomentReset.Coeff = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ExtendedHeatedOutgoing.Coeff"
example : @NavierStokes.ExtendedHeatedOutgoing.Coeff = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.FiveProfileMoments.Debt"
example : @NavierStokes.FiveProfileMoments.Debt = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.FiveRowRank.Debt"
example : @NavierStokes.FiveRowRank.Debt = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.HeatSwitchCone.Coeff"
example : @NavierStokes.HeatSwitchCone.Coeff = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.HeatedOutgoing.Coeff"
example : @NavierStokes.HeatedOutgoing.Coeff = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.MatchingDebtBounds.Debt"
example : @NavierStokes.MatchingDebtBounds.Debt = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.MeanRankUpdate.Debt"
example : @NavierStokes.MeanRankUpdate.Debt = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ModulatedHistories.Debt"
example : @NavierStokes.ModulatedHistories.Debt = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.ModulatedStockBounds.StockData"
example : @NavierStokes.ModulatedStockBounds.StockData = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.NominalProfile.Debt"
example : @NavierStokes.NominalProfile.Debt = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PartitionedCovariance.Vec2"
example : @NavierStokes.PartitionedCovariance.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PeriodicIntegration.Coords"
example : @NavierStokes.PeriodicIntegration.Coords = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PhysicalResidualJetBounds.Components"
example : @NavierStokes.PhysicalResidualJetBounds.Components = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PhysicalSignedWave.Vec2"
example : @NavierStokes.PhysicalSignedWave.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PhysicalWaveSum.Position"
example : @NavierStokes.PhysicalWaveSum.Position = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PositiveOrderMoments.Debt"
example : @NavierStokes.PositiveOrderMoments.Debt = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PrimaryCovarianceBounds.Vec2"
example : @NavierStokes.PrimaryCovarianceBounds.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PrimaryFieldAssembly.Vector"
example : @NavierStokes.PrimaryFieldAssembly.Vector = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PrimaryRepresentatives.Position"
example : @NavierStokes.PrimaryRepresentatives.Position = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PrimaryTargetBounds.Vec2"
example : @NavierStokes.PrimaryTargetBounds.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.PulseCovariance.Vec2"
example : @NavierStokes.PulseCovariance.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.SignedCopyBounds.Vec2"
example : @NavierStokes.SignedCopyBounds.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.SignedCovariance.Vec2"
example : @NavierStokes.SignedCovariance.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.SignedWaveUpdate.Vec2"
example : @NavierStokes.SignedWaveUpdate.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.SlotColoring.Position"
example : @NavierStokes.SlotColoring.Position = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.SlowBorelBase.Bundle"
example : @NavierStokes.SlowBorelBase.Bundle = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.SmoothCovariance.Vec2"
example : @NavierStokes.SmoothCovariance.Vec2 = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00011 NavierStokes.TerminalCompensation.Coeff"
example : @NavierStokes.TerminalCompensation.Coeff = @NavierStokes.ActivationContinuation.FieldJet := rfl
run_cmd IO.println "BLOCK F00023 NavierStokes.CorrectionStep.ScalarField"
example : @NavierStokes.CorrectionStep.ScalarField = @NavierStokes.CorrectionState.ScalarField := rfl
run_cmd IO.println "BLOCK F00023 NavierStokes.DefectIncrementBounds.ScalarField"
example : @NavierStokes.DefectIncrementBounds.ScalarField = @NavierStokes.CorrectionState.ScalarField := rfl
run_cmd IO.println "BLOCK F00023 NavierStokes.LocalRankDefect.ScalarField"
example : @NavierStokes.LocalRankDefect.ScalarField = @NavierStokes.CorrectionState.ScalarField := rfl
run_cmd IO.println "BLOCK F00023 NavierStokes.MeanIncrementBounds.Field"
example : @NavierStokes.MeanIncrementBounds.Field = @NavierStokes.CorrectionState.ScalarField := rfl
run_cmd IO.println "BLOCK F00023 NavierStokes.SignedMeanGain.ScalarField"
example : @NavierStokes.SignedMeanGain.ScalarField = @NavierStokes.CorrectionState.ScalarField := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualCurrentCarrierJets.Label"
example : @NavierStokes.ActualCurrentCarrierJets.Label = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualCurrentParticularBounds.Label"
example : @NavierStokes.ActualCurrentParticularBounds.Label = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualCurrentParticularPhysical.Label"
example : @NavierStokes.ActualCurrentParticularPhysical.Label = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualCycleParameters.ParticularIndex"
example : @NavierStokes.ActualCycleParameters.ParticularIndex = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualParticularBackground.Label"
example : @NavierStokes.ActualParticularBackground.Label = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualParticularStageControls.Label"
example : @NavierStokes.ActualParticularStageControls.Label = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualPhaseJetBounds.SignedLabel"
example : @NavierStokes.ActualPhaseJetBounds.SignedLabel = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualPrimaryBounds.SignedLabel"
example : @NavierStokes.ActualPrimaryBounds.SignedLabel = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.ActualSignedStageControls.PulseLabel"
example : @NavierStokes.ActualSignedStageControls.PulseLabel = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.CurrentParticularLabelBounds.Label"
example : @NavierStokes.CurrentParticularLabelBounds.Label = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.CurrentPhysicalModeGerms.Label"
example : @NavierStokes.CurrentPhysicalModeGerms.Label = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00027 NavierStokes.InitialPhysicalData.SignedLabel"
example : @NavierStokes.InitialPhysicalData.SignedLabel = @NavierStokes.ActualCopySliceRegularity.Label := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedMeanBinding.Frequency"
example : @NavierStokes.ActualSignedMeanBinding.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedNativeBounds.Copy"
example : @NavierStokes.ActualSignedNativeBounds.Copy = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedNativeProfiles.Frequency"
example : @NavierStokes.ActualSignedNativeProfiles.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedPhysicalCoherence.Frequency"
example : @NavierStokes.ActualSignedPhysicalCoherence.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedPhysicalData.Frequency"
example : @NavierStokes.ActualSignedPhysicalData.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedPhysicalZeros.Frequency"
example : @NavierStokes.ActualSignedPhysicalZeros.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedStageControls.Frequency"
example : @NavierStokes.ActualSignedStageControls.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedUnmaskedBinding.Copy"
example : @NavierStokes.ActualSignedUnmaskedBinding.Copy = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualSignedUnmaskedBounds.Copy"
example : @NavierStokes.ActualSignedUnmaskedBounds.Copy = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.ActualWaveCoefficientPeriodicity.Frequency"
example : @NavierStokes.ActualWaveCoefficientPeriodicity.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.InitialNativeRegularity.Frequency"
example : @NavierStokes.InitialNativeRegularity.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.InitialPhysicalData.Frequency"
example : @NavierStokes.InitialPhysicalData.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.PrimaryCopyBridge.Frequency"
example : @NavierStokes.PrimaryCopyBridge.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00029 NavierStokes.TorusInverse.Frequency"
example : @NavierStokes.TorusInverse.Frequency = @NavierStokes.ActualPeriodizedSignedRealization.Frequency := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualCycleCoherence.Index"
example : @NavierStokes.ActualCycleCoherence.Index = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualCyclePeriodicity.Index"
example : @NavierStokes.ActualCyclePeriodicity.Index = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualCyclePreservation.Index"
example : @NavierStokes.ActualCyclePreservation.Index = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualCycleResidualBounds.Index"
example : @NavierStokes.ActualCycleResidualBounds.Index = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedCurrentSupport.Index"
example : @NavierStokes.ActualSignedCurrentSupport.Index = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedExterior.Label"
example : @NavierStokes.ActualSignedExterior.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedFamilySupport.Label"
example : @NavierStokes.ActualSignedFamilySupport.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedNativeBounds.Label"
example : @NavierStokes.ActualSignedNativeBounds.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedNativeProfiles.Label"
example : @NavierStokes.ActualSignedNativeProfiles.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedPhysicalZeros.Label"
example : @NavierStokes.ActualSignedPhysicalZeros.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedReferenceGeometry.Label"
example : @NavierStokes.ActualSignedReferenceGeometry.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedUnmaskedBinding.Label"
example : @NavierStokes.ActualSignedUnmaskedBinding.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.ActualSignedWaveData.Label"
example : @NavierStokes.ActualSignedWaveData.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00031 NavierStokes.PositiveTimeSignedLocalization.Label"
example : @NavierStokes.PositiveTimeSignedLocalization.Label = @NavierStokes.ActualCandidateConstruction.Index := rfl
run_cmd IO.println "BLOCK F00036 NavierStokes.GaugeDebtIncrement.Scalar"
example : @NavierStokes.GaugeDebtIncrement.Scalar = @NavierStokes.ActualMeanPhysicalData.Scalar := rfl
run_cmd IO.println "BLOCK F00036 NavierStokes.GaugeRadialResidualBounds.Scalar"
example : @NavierStokes.GaugeRadialResidualBounds.Scalar = @NavierStokes.ActualMeanPhysicalData.Scalar := rfl
run_cmd IO.println "BLOCK F00036 NavierStokes.MeanStageRegularity.Scalar"
example : @NavierStokes.MeanStageRegularity.Scalar = @NavierStokes.ActualMeanPhysicalData.Scalar := rfl
run_cmd IO.println "BLOCK F00036 NavierStokes.MeanStateRegularity.Scalar"
example : @NavierStokes.MeanStateRegularity.Scalar = @NavierStokes.ActualMeanPhysicalData.Scalar := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.ActualPrimaryBounds.Native"
example : @NavierStokes.ActualPrimaryBounds.Native = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.ActualPrimaryDynamics.Native"
example : @NavierStokes.ActualPrimaryDynamics.Native = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.ActualSignedDynamics.Native"
example : @NavierStokes.ActualSignedDynamics.Native = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.ActualSignedGeometry.Native"
example : @NavierStokes.ActualSignedGeometry.Native = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.ActualSignedStageControls.Native"
example : @NavierStokes.ActualSignedStageControls.Native = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.CorrectionInitialization.ActualPrimary.AbsolutePoint"
example : @NavierStokes.CorrectionInitialization.ActualPrimary.AbsolutePoint = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.NativeBandExtension.Native"
example : @NavierStokes.NativeBandExtension.Native = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.PhaseCalculus.Slot"
example : @NavierStokes.PhaseCalculus.Slot = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.PhysicalGraphBounds.Slot"
example : @NavierStokes.PhysicalGraphBounds.Slot = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.PhysicalResidualNaturality.Associated"
example : @NavierStokes.PhysicalResidualNaturality.Associated = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.PrimaryMaterialDefect.Slot"
example : @NavierStokes.PrimaryMaterialDefect.Slot = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00037 NavierStokes.WaveEdgeExtension.NativePoint"
example : @NavierStokes.WaveEdgeExtension.NativePoint = @NavierStokes.ActualParticularRealization.Associated := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.ActualSignedControl.Mat2"
example : @NavierStokes.ActualSignedControl.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.ActualSignedMeanBinding.Mat2"
example : @NavierStokes.ActualSignedMeanBinding.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.ActualSignedPhysicalData.Mat2"
example : @NavierStokes.ActualSignedPhysicalData.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.PartitionedCovariance.Mat2"
example : @NavierStokes.PartitionedCovariance.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.PhysicalSignedWave.Mat2"
example : @NavierStokes.PhysicalSignedWave.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.PrimaryCovarianceBounds.Mat2"
example : @NavierStokes.PrimaryCovarianceBounds.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.PrimaryTargetBounds.Mat2"
example : @NavierStokes.PrimaryTargetBounds.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.PulseCovariance.Mat2"
example : @NavierStokes.PulseCovariance.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.SignedCopyBounds.Mat2"
example : @NavierStokes.SignedCopyBounds.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.SignedCovariance.Mat2"
example : @NavierStokes.SignedCovariance.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.SignedWaveUpdate.Mat2"
example : @NavierStokes.SignedWaveUpdate.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00038 NavierStokes.SmoothCovariance.Mat2"
example : @NavierStokes.SmoothCovariance.Mat2 = @NavierStokes.ActualPeriodizedSignedRealization.Mat2 := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.GrowingMode.State"
example : @NavierStokes.GrowingMode.State = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.MovingFrameODE.Plane"
example : @NavierStokes.MovingFrameODE.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PhaseEstimates.Plane"
example : @NavierStokes.PhaseEstimates.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PhaseJetBounds.Plane"
example : @NavierStokes.PhaseJetBounds.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PrimaryCopyBridge.State"
example : @NavierStokes.PrimaryCopyBridge.State = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PrimaryGeometryAssembly.Plane"
example : @NavierStokes.PrimaryGeometryAssembly.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PrimaryODE.State"
example : @NavierStokes.PrimaryODE.State = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PrimaryPulseBounds.State"
example : @NavierStokes.PrimaryPulseBounds.State = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PrimaryRepresentatives.Plane"
example : @NavierStokes.PrimaryRepresentatives.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.PrimaryTargetBounds.Plane"
example : @NavierStokes.PrimaryTargetBounds.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.ProfileSpectralCone.Plane"
example : @NavierStokes.ProfileSpectralCone.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00039 NavierStokes.ViscousPropagator.Plane"
example : @NavierStokes.ViscousPropagator.Plane = @NavierStokes.BasePhaseGeometry.Plane := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.MatchingDebtBounds.Field"
example : @NavierStokes.MatchingDebtBounds.Field = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.ModulatedHistories.Field"
example : @NavierStokes.ModulatedHistories.Field = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.NominalProfile.Field"
example : @NavierStokes.NominalProfile.Field = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.OutgoingHistories.Field"
example : @NavierStokes.OutgoingHistories.Field = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.PositiveOrderMoments.JointProfile"
example : @NavierStokes.PositiveOrderMoments.JointProfile = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.ProfileHistories.Field"
example : @NavierStokes.ProfileHistories.Field = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.SimilarityProfile.InnerProfile"
example : @NavierStokes.SimilarityProfile.InnerProfile = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00049 NavierStokes.SlowStressSupport.Field"
example : @NavierStokes.SlowStressSupport.Field = @NavierStokes.GlobalSlowProfiles.Field := rfl
run_cmd IO.println "BLOCK F00054 NavierStokes.ActualSignedPhysicalCoherence.SpaceTime"
example : @NavierStokes.ActualSignedPhysicalCoherence.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00054 NavierStokes.AnnularEndpoint.SpaceTime"
example : @NavierStokes.AnnularEndpoint.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00054 NavierStokes.JointResidualLimits.SpaceTime"
example : @NavierStokes.JointResidualLimits.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00054 NavierStokes.OffplaneCorrectionExtensions.SpaceTime"
example : @NavierStokes.OffplaneCorrectionExtensions.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00054 NavierStokes.ProblemStatement.SpaceTime"
example : @NavierStokes.ProblemStatement.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00054 NavierStokes.SpacetimeEndpoint.SpaceTime"
example : @NavierStokes.SpacetimeEndpoint.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00054 NavierStokes.SpacetimeGluing.SpaceTime"
example : @NavierStokes.SpacetimeGluing.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00054 NavierStokesR3.ProblemStatement.SpaceTime"
example : @NavierStokesR3.ProblemStatement.SpaceTime = @NavierStokes.ActualBaseResidual.SpaceTime := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.ActualCurrentParticularBounds.Native"
example : @NavierStokes.ActualCurrentParticularBounds.Native = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.ActualCurrentParticularPhysical.Native"
example : @NavierStokes.ActualCurrentParticularPhysical.Native = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.ActualParticularBackground.Native"
example : @NavierStokes.ActualParticularBackground.Native = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.ActualParticularRealization.WaveSpace"
example : @NavierStokes.ActualParticularRealization.WaveSpace = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.ActualParticularStageControls.Native"
example : @NavierStokes.ActualParticularStageControls.Native = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.ActualWaveRegularity.ParticularSpace"
example : @NavierStokes.ActualWaveRegularity.ParticularSpace = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.CurrentPhysicalChartJets.Native"
example : @NavierStokes.CurrentPhysicalChartJets.Native = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.GaussianErrorNaturality.WaveSpace"
example : @NavierStokes.GaussianErrorNaturality.WaveSpace = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00055 NavierStokes.PhysicalParticularWave.WaveSpace"
example : @NavierStokes.PhysicalParticularWave.WaveSpace = @NavierStokes.ActualCurrentCarrierJets.Native := rfl
run_cmd IO.println "BLOCK F00077 NavierStokes.ActualSignedPhysicalData.LiftPoint"
example : @NavierStokes.ActualSignedPhysicalData.LiftPoint = @NavierStokes.ActualSignedNativeProfiles.LiftPoint := rfl
run_cmd IO.println "BLOCK F00077 NavierStokes.CartesianCopySource.LiftPoint"
example : @NavierStokes.CartesianCopySource.LiftPoint = @NavierStokes.ActualSignedNativeProfiles.LiftPoint := rfl
run_cmd IO.println "BLOCK F00077 NavierStokes.CurrentPhysicalChartJets.LiftPoint"
example : @NavierStokes.CurrentPhysicalChartJets.LiftPoint = @NavierStokes.ActualSignedNativeProfiles.LiftPoint := rfl
run_cmd IO.println "BLOCK F00077 NavierStokes.InitialPhysicalData.LiftPoint"
example : @NavierStokes.InitialPhysicalData.LiftPoint = @NavierStokes.ActualSignedNativeProfiles.LiftPoint := rfl
run_cmd IO.println "BLOCK F00077 NavierStokes.PhysicalGraphBounds.LiftPoint"
example : @NavierStokes.PhysicalGraphBounds.LiftPoint = @NavierStokes.ActualSignedNativeProfiles.LiftPoint := rfl
run_cmd IO.println "BLOCK F00077 NavierStokes.PhysicalWaveSum.LiftPoint"
example : @NavierStokes.PhysicalWaveSum.LiftPoint = @NavierStokes.ActualSignedNativeProfiles.LiftPoint := rfl
run_cmd IO.println "BLOCK F00077 NavierStokes.PositiveTimeCopyFamily.LiftPoint"
example : @NavierStokes.PositiveTimeCopyFamily.LiftPoint = @NavierStokes.ActualSignedNativeProfiles.LiftPoint := rfl
run_cmd IO.println "BLOCK F00078 NavierStokes.DefectIncrementBounds.Point"
example : @NavierStokes.DefectIncrementBounds.Point = @NavierStokes.CorrectionState.Lift := rfl
run_cmd IO.println "BLOCK F00078 NavierStokes.GaugeAliasDecay.Point"
example : @NavierStokes.GaugeAliasDecay.Point = @NavierStokes.CorrectionState.Lift := rfl
run_cmd IO.println "BLOCK F00078 NavierStokes.LocalRankDefect.Point"
example : @NavierStokes.LocalRankDefect.Point = @NavierStokes.CorrectionState.Lift := rfl
run_cmd IO.println "BLOCK F00078 NavierStokes.PressureStream.Lift"
example : @NavierStokes.PressureStream.Lift = @NavierStokes.CorrectionState.Lift := rfl
