# jack-vm-compiler

Jack Compiler
This repository contains a fully functional compiler for the Jack programming language, built in Python.
This project translates high-level, object-oriented Jack source code into intermediate VM code, which is executable on the Nand2Tetris VM Emulator.

This project is a deep dive into the principles of compiler construction, covering lexical analysis, syntax analysis (parsing), symbol table management, and code generation for a modern, object-based language.

🚀 Features
Lexical Analysis (Tokenization): Breaks down raw Jack source code into a stream of meaningful tokens, ignoring whitespace and comments.

Recursive Descent Parsing: Employs a top-down parsing strategy to analyze the syntactic structure of the token stream according to the Jack grammar.

Symbol Table Management: Implements scoped symbol tables (class and subroutine levels) to manage identifiers, their types, kinds, and indices.

VM Code Generation: Traverses the parse tree to generate the equivalent VM code, handling expressions, control flow (if-else, while), object-oriented features (constructors, methods), and OS library calls.

Full Jack Language Support: Compiles the complete Jack language specification.

🛠️ Technologies Used
Language: Python 3

Development Environment: Nand2Tetris Software Suite (specifically the VM Emulator for testing)

📁 Project Structure
The compiler is modular, with each component handling a distinct phase of the compilation process:

/
├── compile.py              # Main driver that orchestrates the compilation process
├── jack_tokenizer.py       # Handles lexical analysis (tokenizing)
├── compilation_engine.py   # Core parser and code generator
├── symbol_table.py         # Manages symbol tables for identifiers
└── vm_writer.py            # Helper module to write VM commands to the output file

compile.py: The entry point. It handles command-line arguments and manages the compilation of a single .jack file or all .jack files within a directory.

jack_tokenizer.py: Reads the input source file, cleans it by removing comments and whitespace, and exposes an API to stream tokens one by one.

compilation_engine.py: The heart of the compiler. It uses the JackTokenizer to receive tokens and implements the Jack grammar through a set of mutually recursive methods to parse the code structure. As it parses, it generates the corresponding VM code using the VMWriter.

symbol_table.py: Provides a data structure to manage symbols (variables, fields, static variables, arguments). It handles scope and assigns a unique index to each identifier.

vm_writer.py: An abstraction layer that simplifies the generation of VM code by providing dedicated methods for writing each type of VM command (push, pop, call, etc.).

⚙️ How to Run and Test
Prerequisites
Python 3 installed on your system.

The Nand2Tetris Software Suite, which includes the VM Emulator, must be downloaded. You can get it from the official Nand2Tetris website.

Compilation Steps
Clone the repository:

git clone https://github.com/mustafamagdym5/jack-vm-compiler.git
cd jack-vm-compiler

Run the compiler:
The compiler is run from the command line using python3. It accepts a single argument: the path to a .jack source file or a directory containing .jack files.

To compile a single file (e.g., Main.jack):

python3 compile.py path/to/Main.jack

This will generate a Main.vm file in the same directory.

To compile a whole project directory (e.g., Pong):

python3 compile.py path/to/Pong/

This will compile every .jack file in the Pong directory, creating a corresponding .vm file for each.

Testing the Output
Launch the VM Emulator from the Nand2Tetris Software Suite.

Click the "Load Program" button.

Navigate to the directory containing the .vm file(s) you just generated (e.g., the Pong directory).

Select the directory and click "Load". The emulator will load all VM files and prepare for execution.

You can then run the program at various speeds or step through it to observe the stack and memory operations, verifying the correctness of your compiler's output.

The Compilation Pipeline
The compiler processes a Jack program in a sequence of logical steps to transform human-readable code into machine-executable VM code.

Tokenization: The JackTokenizer scans the source .jack file character by character. It identifies and categorizes sequences of characters into tokens (e.g., keyword, symbol, identifier, integerConstant, stringConstant), discarding non-semantic elements like comments and whitespace.

Syntactic Analysis (Parsing): The CompilationEngine takes the stream of tokens and determines the grammatical structure. Using a recursive descent approach, it contains a method for every non-terminal in the Jack grammar (e.g., compileClass, compileSubroutine, compileStatements). These methods consume tokens and recursively call other methods, effectively building a parse tree in memory.

Semantic Analysis & Symbol Management: As the engine parses the code, it uses the SymbolTable to record information about identifiers. When a variable is declared, it's added to the symbol table with its name, type, and kind (scope). When a variable is used later, the symbol table is queried to retrieve its information, ensuring it has been declared and allowing the compiler to reference it correctly (e.g., pop local 0).

Code Generation: This phase is tightly integrated with parsing. As the CompilationEngine successfully recognizes a language construct (like an if statement or an arithmetic expression), it immediately calls methods in the VMWriter to emit the corresponding sequence of VM commands. For example, parsing the expression x + 1 involves generating push local 0 (for x), push constant 1, and add.

Technical Challenges & Solutions
Building this compiler involved several technical challenges:

Parsing Expressions with Precedence: The Jack grammar for expressions is simple and doesn't specify operator precedence (e.g., * before +). The solution was to strictly follow the grammar's left-to-right evaluation. A more advanced compiler might use techniques like the Shunting-yard algorithm, but for Jack, a direct recursive implementation was sufficient.

Distinguishing Method Calls: A key challenge was parsing expressions like foo.bar(). The compiler must determine if foo is a class name (a static function call) or an object instance (a method call).

Solution: This was resolved by consulting the SymbolTable. If foo is found in the symbol table as a variable, it's an object instance, and the compiler must generate a push command for that object's base address before calling the method. Otherwise, foo is treated as a class name for a static function call.

Managing Scopes with Symbol Tables: Keeping track of variables in their correct scopes (class-level static/field vs. subroutine-level argument/local) is critical.

Solution: Two separate symbol tables were maintained: one for the class scope and one for the current subroutine. The subroutine table is cleared and rebuilt for each new function or method, ensuring a clean scope.

Recursive-Descent Parser Design: The entire parser is a set of mutually recursive functions. A single mistake in the logic (e.g., not advancing a token correctly) could lead to infinite loops or incorrect parsing.

Solution: Rigorous, unit-by-unit testing was essential. Each parsing function (compileTerm, compileStatements, etc.) was tested independently to ensure it correctly consumed its tokens and handled all grammatical possibilities before being integrated into the whole.
