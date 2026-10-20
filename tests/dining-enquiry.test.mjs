import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildDiningWhatsAppUrl, validateDiningEnquiry } from '../lib/dining-enquiry.ts';

const valid = { name: 'Mira & Arun', date: '2026-12-30', interest: 'Restaurant meal', guests: '2', notes: 'Could you share the vegetarian menu? & prices' };

test('dining draft preserves the requested details and uses the approved WhatsApp host', () => {
  assert.deepEqual(validateDiningEnquiry(valid, '2026-10-20'), {});
  const url = new URL(buildDiningWhatsAppUrl('918081709146', valid));
  assert.equal(url.hostname, 'wa.me');
  assert.equal(url.pathname, '/918081709146');
  const message = url.searchParams.get('text');
  for (const value of ['Mira & Arun', '30 Dec 2026', 'Restaurant meal', 'People in our party: 2', valid.notes]) assert.ok(message.includes(value), value);
  assert.ok(message.includes('Please share'));
});
test('dining validation rejects impossible or past dates, invalid counts and invented interests', () => {
  for (const date of ['', '2026-02-30', '2026-10-19']) assert.ok(validateDiningEnquiry({...valid,date}, '2026-10-20').date);
  for (const guests of ['0','-1','2.5','abc','100']) assert.ok(validateDiningEnquiry({...valid,guests}, '2026-10-20').guests);
  assert.ok(validateDiningEnquiry({...valid,interest:'Wedding package'}, '2026-10-20').interest);
  assert.ok(validateDiningEnquiry({...valid,notes:'a'.repeat(601)}, '2026-10-20').notes);
  assert.throws(() => buildDiningWhatsAppUrl('javascript:alert(1)', valid));
  assert.throws(() => buildDiningWhatsAppUrl('918081709146', {...valid,date:'2026-02-30'}));
});
