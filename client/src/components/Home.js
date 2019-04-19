import React from 'react'
import { Jumbotron, Container } from 'react-bootstrap'
export default function HomePage() {
  return (
    <div>
      <Jumbotron fluid>
        <Container>
          <h1 className=''>Cluster and Computing project</h1>
          <hr />
          <h2>
            Name of the project.
          </h2>
        </Container>
      </Jumbotron>
    </div>
  )
}
