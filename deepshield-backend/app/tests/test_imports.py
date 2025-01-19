import sys
import logging
import unittest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAIModuleImports(unittest.TestCase):
    def test_ai_module_imports(self):
        """Test that all AI modules can be imported and initialized."""
        try:
            from app.services.ai import DeepfakeDetector, ContentModerator, FaceVerifier
            from app.core.dataset_config import verify_dataset_files, DATASETS
            
            logger.info('Successfully imported AI modules')
            logger.info('Available datasets: %s', list(DATASETS.keys()))
            
            missing_files = verify_dataset_files()
            if missing_files:
                logger.warning('Missing dataset files: %s', missing_files)
            else:
                logger.info('All required dataset files are present')
            
            # Test initializing models in test mode
            deepfake = DeepfakeDetector(test_mode=True)
            content_mod = ContentModerator(test_mode=True)
            face_verify = FaceVerifier(test_mode=True)
            logger.info('Successfully initialized AI models in test mode')
            
            self.assertTrue(True, "AI modules imported and initialized successfully")
            
        except ImportError as e:
            logger.error('Failed to import AI modules: %s', e)
            self.fail(f"Import error: {e}")
        except Exception as e:
            logger.error('Error during initialization: %s', e)
            self.fail(f"Initialization error: {e}")

if __name__ == '__main__':
    unittest.main()
