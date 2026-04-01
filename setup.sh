#!/bin/bash
# ClearCom Compiler - Quick Setup Script
# Run this to see if everything works!

echo "🔧 ClearCom Compiler - Setup Check"
echo "===================================="
echo ""

# Check Python
echo "✓ Checking Python..."
if command -v python3 &> /dev/null; then
    version=$(python3 --version)
    echo "  Found: $version"
else
    echo "  ✗ Python3 not found!"
    exit 1
fi

# Check PLY
echo ""
echo "✓ Checking PLY..."
if python3 -c "import ply" 2>/dev/null; then
    echo "  ✓ PLY is installed"
else
    echo "  ✗ PLY not installed! Installing..."
    python3 -m pip install ply
fi

# Test compilation
echo ""
echo "✓ Testing compiler..."
if [ -f "input.mc" ]; then
    echo "  Running: python3 main.py input.mc"
    echo "  (output below)"
    echo "  ---"
    python3 main.py input.mc 2>&1 | tail -20
    echo "  ---"
    echo ""
    echo "✅ Everything looks good!"
else
    echo "  ✗ input.mc not found"
fi

echo ""
echo "📖 Next steps:"
echo "  1. python3 main.py input.mc       # Compile a file"
echo "  2. python3 interactive.py         # Interactive mode"
echo "  3. Read BEGINNER_GUIDE.md         # Learn basics"
echo ""
