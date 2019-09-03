import {Hand} from './Hand';
import {Table} from './Table';

function Player () {
  return (
    <div>
      <Hand />
      <Table />
      This is the Player, containing a hand and a table
    </div>
  )
}

export default Player;