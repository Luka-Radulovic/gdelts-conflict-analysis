import React, { Dispatch, SetStateAction, useState } from 'react'
import './UiOverlay.css'
import { dateFromIso, dateToIso } from './utils/dateUtils';

function UiOverlay(props: { date: Date; setDate: Dispatch<SetStateAction<Date>>; }) {
    const minDate = dateFromIso('2016-01-01')
    const maxDate = new Date()

    return (
        <div id='main'>
            Pick a date for the relations:
            <br />
            <button onClick={() => {
                props.setDate((prev) => {
                    const dateCopy = dateFromIso(dateToIso(prev))
                    dateCopy.setDate(dateCopy.getDate() - 1)
                    if (dateCopy < minDate)
                        return prev
                    return dateCopy
                })
            }}>day before</button>
            <input
                type='date'
                min={dateToIso(minDate)}
                max={dateToIso(maxDate)}
                value={dateToIso(props.date)}
                onChange={(dateot) => {
                    props.setDate(dateFromIso(dateot.target.value))
                }}></input>
            <button onClick={() => {
                props.setDate(prev => {
                    const dateCopy = dateFromIso(dateToIso(prev))
                    dateCopy.setDate(dateCopy.getDate() + 1)
                    if (dateCopy > maxDate)
                        return prev
                    return dateCopy
                })
            }}>day after</button>
        </div>
    )
}

export default UiOverlay