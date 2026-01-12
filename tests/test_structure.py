"""
Basic structure tests for NIS2expert package.

These tests validate the package structure and basic imports
without requiring external dependencies like OpenAI API.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_package_structure():
    """Test that all expected modules exist."""
    from nis2expert import __version__
    
    assert __version__ == "0.1.0"
    
    # Test that all modules can be imported (structure-wise)
    import nis2expert
    import nis2expert.config
    import nis2expert.loaders
    import nis2expert.splitters
    import nis2expert.embeddings
    import nis2expert.vectorstore
    import nis2expert.chains
    import nis2expert.auditing
    import nis2expert.gap_analysis
    import nis2expert.scoring
    import nis2expert.reporting
    import nis2expert.utils
    
    print("✓ All modules can be imported")


def test_module_contents():
    """Test that key classes are defined."""
    # These tests check class definitions exist without instantiating them
    
    from nis2expert.loaders import NIS2DocumentLoader
    assert NIS2DocumentLoader is not None
    print("✓ NIS2DocumentLoader class exists")
    
    from nis2expert.splitters import NIS2TextSplitter, ArticleAwareSplitter
    assert NIS2TextSplitter is not None
    assert ArticleAwareSplitter is not None
    print("✓ Splitter classes exist")
    
    from nis2expert.embeddings import NIS2Embeddings, get_embeddings
    assert NIS2Embeddings is not None
    assert get_embeddings is not None
    print("✓ Embeddings classes exist")
    
    from nis2expert.vectorstore import NIS2VectorStore
    assert NIS2VectorStore is not None
    print("✓ NIS2VectorStore class exists")
    
    from nis2expert.chains import NIS2Chain, NIS2QAChain, ComplianceCheckChain, DocumentSummaryChain
    assert NIS2Chain is not None
    assert NIS2QAChain is not None
    assert ComplianceCheckChain is not None
    assert DocumentSummaryChain is not None
    print("✓ Chain classes exist")
    
    from nis2expert.auditing import AuditLogger, ComplianceAudit
    assert AuditLogger is not None
    assert ComplianceAudit is not None
    print("✓ Auditing classes exist")
    
    from nis2expert.gap_analysis import GapAnalyzer, RemediationTracker
    assert GapAnalyzer is not None
    assert RemediationTracker is not None
    print("✓ Gap analysis classes exist")
    
    from nis2expert.scoring import ComplianceScorer, RiskScorer
    assert ComplianceScorer is not None
    assert RiskScorer is not None
    print("✓ Scoring classes exist")
    
    from nis2expert.reporting import ReportGenerator, ExecutiveSummary
    assert ReportGenerator is not None
    assert ExecutiveSummary is not None
    print("✓ Reporting classes exist")
    
    from nis2expert.utils import setup_logging, ensure_directory
    assert setup_logging is not None
    assert ensure_directory is not None
    print("✓ Utility functions exist")


def test_file_structure():
    """Test that expected files exist in the project."""
    project_root = Path(__file__).parent.parent
    
    # Check essential files
    assert (project_root / "README.md").exists()
    assert (project_root / "requirements.txt").exists()
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / ".gitignore").exists()
    assert (project_root / ".env.example").exists()
    
    # Check package directory
    assert (project_root / "nis2expert" / "__init__.py").exists()
    assert (project_root / "nis2expert" / "config.py").exists()
    
    # Check module directories
    modules = [
        "loaders", "splitters", "embeddings", "vectorstore", 
        "chains", "auditing", "gap_analysis", "scoring", 
        "reporting", "utils"
    ]
    for module in modules:
        module_init = project_root / "nis2expert" / module / "__init__.py"
        assert module_init.exists(), f"Module {module} __init__.py missing"
    
    # Check docs
    assert (project_root / "docs" / "architecture.md").exists()
    
    # Check examples
    assert (project_root / "examples" / "basic_usage.py").exists()
    
    print("✓ All expected files exist")


if __name__ == "__main__":
    print("Running NIS2expert structure tests...\n")
    
    try:
        test_package_structure()
        print()
        test_module_contents()
        print()
        test_file_structure()
        print("\n" + "="*60)
        print("✓ All structure tests passed!")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
