import React, { Component } from 'react'
import MapWithAMarker from './MapComponent'
export default class MapPage extends Component {
  render() {
    return (
      <div>
        <MapWithAMarker
          containerElement={<div style={{ height: `500px` }} />}
          mapElement={<div style={{ height: `100%` }} />}
        />
      </div>
    )
  }
}
