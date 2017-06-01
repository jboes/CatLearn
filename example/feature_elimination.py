"""Script to test descriptors for the ML model."""
from __future__ import print_function
from __future__ import absolute_import

from ase.ga.data import DataConnection
from atoml.data_setup import get_unique, get_train
from atoml.fingerprint_setup import return_fpv
from atoml.feature_preprocess import normalize
from atoml.feature_elimination import FeatureScreening
from atoml.particle_fingerprint import ParticleFingerprintGenerator
from atoml.standard_fingerprint import StandardFingerprintGenerator
from atoml.predict import GaussianProcess

# Connect database generated by a GA search.
db = DataConnection('gadb.db')

# Get all relaxed candidates from the db file.
print('Getting candidates from the database')
all_cand = db.get_all_relaxed_candidates(use_extinct=False)

# Setup the test and training datasets.
testset = get_unique(atoms=all_cand, size=50, key='raw_score')
trainset = get_train(atoms=all_cand, size=50, taken=testset['taken'],
                     key='raw_score')

# Get the list of fingerprint vectors and normalize them.
print('Getting the fingerprint vectors')
fpv = ParticleFingerprintGenerator(get_nl=False, max_bonds=13)
std = StandardFingerprintGenerator()
test_fp = return_fpv(testset['atoms'], [fpv.nearestneighbour_fpv,
                                        fpv.bond_count_fpv,
                                        fpv.distribution_fpv,
                                        fpv.rdf_fpv,
                                        std.mass_fpv,
                                        std.eigenspectrum_fpv,
                                        std.distance_fpv])
train_fp = return_fpv(trainset['atoms'], [fpv.nearestneighbour_fpv,
                                          fpv.bond_count_fpv,
                                          fpv.distribution_fpv,
                                          fpv.rdf_fpv,
                                          std.mass_fpv,
                                          std.eigenspectrum_fpv,
                                          std.distance_fpv])


def do_pred(ptrain_fp, ptest_fp):
    """Function to make prediction."""
    nfp = normalize(train_matrix=ptrain_fp, test_matrix=ptest_fp)

    # Do the predictions.
    pred = gp.get_predictions(train_fp=nfp['train'],
                              test_fp=nfp['test'],
                              train_target=trainset['target'],
                              test_target=testset['target'],
                              get_validation_error=True,
                              get_training_error=True,
                              optimize_hyperparameters=False)

    # Print the error associated with the predictions.
    print('Training error:', pred['training_rmse']['average'])
    print('Model error:', pred['validation_rmse']['average'])


# Get base predictions.
print('Base Predictions')
# Set up the prediction routine.
kdict = {'k1': {'type': 'gaussian', 'width': 0.5}}
gp = GaussianProcess(kernel_dict=kdict, regularization=0.001)
do_pred(ptrain_fp=train_fp, ptest_fp=test_fp)

print('Getting descriptor correlation')
# Set up the prediction routine.
kdict = {'k1': {'type': 'gaussian', 'width': 0.5}}
gp = GaussianProcess(kernel_dict=kdict, regularization=0.001)

screen = FeatureScreening(correlation='pearson', iterative=False)
features = screen.eliminat_features(target=trainset['target'],
                                    train_features=train_fp,
                                    test_features=test_fp, size=50,
                                    step=None, order=None)

sis_test_fp = features[1]
sis_train_fp = features[0]
do_pred(ptrain_fp=sis_train_fp, ptest_fp=sis_test_fp)

screen = FeatureScreening(correlation='pearson', iterative=True)
features = screen.eliminat_features(target=trainset['target'],
                                    train_features=train_fp,
                                    test_features=test_fp, size=50,
                                    step=None, order=None)

sis_test_fp = features[1]
sis_train_fp = features[0]
do_pred(ptrain_fp=sis_train_fp, ptest_fp=sis_test_fp)

screen = FeatureScreening(correlation='spearman', iterative=False)
features = screen.eliminat_features(target=trainset['target'],
                                    train_features=train_fp,
                                    test_features=test_fp, size=50,
                                    step=None, order=None)

sis_test_fp = features[1]
sis_train_fp = features[0]
do_pred(ptrain_fp=sis_train_fp, ptest_fp=sis_test_fp)

screen = FeatureScreening(correlation='spearman', iterative=True)
features = screen.eliminat_features(target=trainset['target'],
                                    train_features=train_fp,
                                    test_features=test_fp, size=50,
                                    step=None, order=None)

sis_test_fp = features[1]
sis_train_fp = features[0]
do_pred(ptrain_fp=sis_train_fp, ptest_fp=sis_test_fp)

creen = FeatureScreening(correlation='kendall', iterative=False)
features = screen.eliminat_features(target=trainset['target'],
                                    train_features=train_fp,
                                    test_features=test_fp, size=50,
                                    step=None, order=None)

sis_test_fp = features[1]
sis_train_fp = features[0]
do_pred(ptrain_fp=sis_train_fp, ptest_fp=sis_test_fp)

screen = FeatureScreening(correlation='kendall', iterative=True)
features = screen.eliminat_features(target=trainset['target'],
                                    train_features=train_fp,
                                    test_features=test_fp, size=50,
                                    step=None, order=None)

sis_test_fp = features[1]
sis_train_fp = features[0]
do_pred(ptrain_fp=sis_train_fp, ptest_fp=sis_test_fp)
