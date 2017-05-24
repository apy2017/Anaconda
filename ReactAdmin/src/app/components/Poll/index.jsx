import React from 'react'
//import { Link } from 'react-router'
//import { format_date } from '../../utils'


export default ({ poll }) => (
    <div>
        <article dangerouslySetInnerHTML={{__html: poll['name']}} />
    </div>
)