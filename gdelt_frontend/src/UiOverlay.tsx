import React, { Dispatch, SetStateAction, useState } from 'react'
import './UiOverlay.css'
import { dateFromIso, dateToIso } from './utils/dateUtils';
import { getCountriesByIso3Code } from './countryOperations';

function UiOverlay(props: { date: Date; setDate: Dispatch<SetStateAction<Date>>; countryCodeA: string; countryCodeB: string }) {
    const minDate = dateFromIso('2016-01-01')
    const maxDate = new Date()

    const countriesByIso3Code = getCountriesByIso3Code()

    return (
        // {props.countryCodeA &&
        <div id='main'>
            Pick a date for the relations:
            <br />
            <div id='date-navigation'>
                <button id='button-minus' onClick={() => {
                    props.setDate((prev) => {
                        const dateCopy = dateFromIso(dateToIso(prev))
                        dateCopy.setDate(dateCopy.getDate() - 1)
                        if (dateCopy < minDate)
                            return prev
                        return dateCopy
                    })
                }}>&lt;&lt;</button>
                <input
                    type='date'
                    min={dateToIso(minDate)}
                    max={dateToIso(maxDate)}
                    value={dateToIso(props.date)}
                    onChange={(dateot) => {
                        props.setDate(dateFromIso(dateot.target.value))
                    }}></input>
                <button id='button-plus' onClick={() => {
                    props.setDate(prev => {
                        const dateCopy = dateFromIso(dateToIso(prev))
                        dateCopy.setDate(dateCopy.getDate() + 1)
                        if (dateCopy > maxDate)
                            return prev
                        return dateCopy
                    })
                }}>&gt;&gt;</button>
            </div>
            <div className='d-flex justify-content-around'>
                <div className='d-flex flex-column align-items-center'>
                    <div>{countriesByIso3Code.get(props.countryCodeA)?.properties.ADMIN}</div>
                    <img className='flag' src={'https://flagicons.lipis.dev/flags/4x3/' + countriesByIso3Code.get(props.countryCodeA)?.properties.ISO_A2.toLowerCase() + '.svg'} alt="" />
                </div>
                <div className='d-flex flex-column align-items-center'>
                    <div>{countriesByIso3Code.get(props.countryCodeB)?.properties.ADMIN}</div>
                    <img className='flag' src={'https://flagicons.lipis.dev/flags/4x3/' + countriesByIso3Code.get(props.countryCodeB)?.properties.ISO_A2.toLowerCase() + '.svg'} alt="" />
                </div>
            </div>
        </div>
    )
}

export default UiOverlay