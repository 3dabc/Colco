
/*
NOTE: this is NOT functional rather it is code that NEEDS to be altered once we get the actual JSON payload structure

It is a good starting code and can easily be adjusted to fit the ACTIAL payloald structure

Basically, this file processes the JSON payload but separating each part of the JSON
    Then, we will send each part to its corresponding collection in the firebase db

Also: this assumes the sensors only collect temp, humid, lkux, and soil moistness
*/

import {db} from '@/firebase';
import {doc, collection, addDoc, setDoc} from 'firebase/firestore';

export async function processJSONPayload(payload) {
    try {
        if (!payload || !payload.Data || !payload.Data.Fields) {
            throw new Error("cant access... check payload struct")
        }

        const fields = payload.Data.Fields;

        for (const [fieldId, fieldData] of Object.entries(fields)) {
            await addDoc(collection(db, 'SensorData'), {
                fieldId: fieldId,
                ...fieldData,
                timestamp: new Date() //fake metadata needs change
            });
        }

        return {processed: true, msg: 'Sensor data send to firebase db'};
    } catch (e) {
        console.error('failed sending payload to db, check error:', e);
        return { processed: false, msg: e.message}
    }
}