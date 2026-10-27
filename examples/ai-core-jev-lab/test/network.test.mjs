import test from 'node:test';import assert from 'node:assert/strict';import {liveJev} from '../src/providers.mjs';
test('live branch requires explicit flag before import',async()=>await assert.rejects(liveJev({text:'x'}),/explicit --live/));
