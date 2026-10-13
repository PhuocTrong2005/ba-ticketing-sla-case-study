// Read-only schema validation using Ajv already installed with Newman.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '../..');
const Ajv = require(path.join(root, '.postman-tools/newman/node_modules/ajv'));
const draft4 = require(path.join(root, '.postman-tools/newman/node_modules/ajv/lib/refs/json-schema-draft-04.json'));
const ajv = new Ajv({schemaId: 'id', meta: false, allErrors: true});
ajv.addMetaSchema(draft4);
const schema = JSON.parse(fs.readFileSync(path.join(root, '.postman-tools/collection-v2.1-schema.json'), 'utf8'));
const collection = JSON.parse(fs.readFileSync(path.join(root, 'api/ticketing-sla.postman_collection.json'), 'utf8'));
const valid = ajv.validate(schema, collection);
console.log(JSON.stringify({schema: collection.info.schema, valid, errors: ajv.errors}));
process.exitCode = valid ? 0 : 1;
