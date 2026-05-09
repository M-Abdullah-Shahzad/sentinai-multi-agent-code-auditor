const esprima = require('esprima');
const fs = require('fs');

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', function(chunk) {
  input += chunk;
});
process.stdin.on('end', function() {
  try {
    const tree = esprima.parseScript(input, { tolerant: true, jsx: true });
    const functions = [];
    const classes = [];

    function visit(node) {
      if (!node || typeof node !== 'object') return;
      if (node.type === 'FunctionDeclaration') {
        functions.push(node.id ? node.id.name : 'anonymous');
      }
      if (node.type === 'ClassDeclaration') {
        classes.push(node.id ? node.id.name : 'anonymous');
      }
      for (const key of Object.keys(node)) {
        const child = node[key];
        if (Array.isArray(child)) {
          child.forEach(visit);
        } else if (child && typeof child === 'object') {
          visit(child);
        }
      }
    }

    visit(tree);
    console.log(JSON.stringify({ functions, classes, ast: tree }));
  } catch (error) {
    console.error(JSON.stringify({ error: error.message }));
    process.exit(1);
  }
});
