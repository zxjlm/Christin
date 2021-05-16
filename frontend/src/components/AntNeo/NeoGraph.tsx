import { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
// @ts-ignore
import Neovis from 'neovis.js/dist/neovis.js';

interface NeoGraphProps {
  width: string;
  height: string;
  containerId: string;
  backgroundColor: string;
  neo4jUri: string;
  neo4jUser: string;
  neo4jPassword: string;
}

const NeoGraph = (props: NeoGraphProps) => {
  const { width, height, containerId, backgroundColor, neo4jUri, neo4jUser, neo4jPassword } = props;

  const visRef = useRef<HTMLDivElement>(null);
  // const [nodeId, setNodeId] = useState(-1);

  useEffect(() => {
    const config = {
      container_id: containerId,
      server_url: neo4jUri,
      server_user: neo4jUser,
      server_password: neo4jPassword,
      labels: {
        Herb: {
          caption: 'English_name',
          size: 1.5,
        },
        Gene: {
          caption: 's_name',
          size: 0.5,
        },
        Mol: {
          caption: 's_name',
          size: 1.0,
        },
        TCM_symptom: {
          caption: 's_name',
          size: 0.8,
        },
        MM_symptom: {
          caption: 's_name',
          size: 0.8,
        },
        Disease: {
          caption: 's_name',
          size: 1.2,
        },
        // [NeoVis.NEOVIS_DEFAULT_CONFIG]: {
        //     "caption": "s_name",
        //     //"size": "defaultPagerank",
        //     //"community": "defaultCommunity"
        //     //"sizeCypher": "defaultSizeCypher"

        // }
      },
      relationships: {
        // RETWEETS: {
        //   caption: false,
        //   thickness: "count",
        // },
      },
      initial_cypher: 'MATCH (n:Herb) RETURN n LIMIT 25',
    };
    const vis = new Neovis(config);
    let node_id = -1;
    let node_click_event_flag = false;
    vis.render();

    vis.registerOnEvent('completed', () => {
      if (!node_click_event_flag) {
        vis['_network'].on('click', (event: { [x: string]: any[] }) => {
          if (event['nodes'][0]) {
            if (node_id === event['nodes'][0]) {
              vis.updateWithCypher(`MATCH r=(s)-->() WHERE ID(s) = ${node_id} RETURN r`);
            } else {
              // eslint-disable-next-line prefer-destructuring
              node_id = event['nodes'][0];
            }
          }
        });
        node_click_event_flag = true;
      }
    });
  }, [neo4jUri, neo4jUser, neo4jPassword, containerId]);

  return (
    <div
      id={containerId}
      ref={visRef}
      style={{
        width: `${width}`,
        height: `${height}`,
        backgroundColor: `${backgroundColor}`,
      }}
    />
  );
};

NeoGraph.defaultProps = {
  width: 600,
  height: 600,
  backgroundColor: '#d3d3d3',
};

NeoGraph.propTypes = {
  width: PropTypes.string.isRequired,
  height: PropTypes.string.isRequired,
  containerId: PropTypes.string.isRequired,
  neo4jUri: PropTypes.string.isRequired,
  neo4jUser: PropTypes.string.isRequired,
  neo4jPassword: PropTypes.string.isRequired,
  backgroundColor: PropTypes.string,
};

export { NeoGraph };
