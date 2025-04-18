import { TilesetImageConfig } from '../models/TilesetImageConfig';

export default function SceneInfo(sceneName) {
  const sceneInfo = {
    tutorial: {
      mapName: 'tutorial',
      zoom: 2.5,
      isSound: true,
      soundAssetKey: 'path_to_lake_land',
      volume: 0.3,
      isSoundLoop: true,
      tileImages: [
        new TilesetImageConfig('tutorial_tileset_extruded', 'tutorial_tileset'),
        new TilesetImageConfig('collision', 'collision_tiles'),
        new TilesetImageConfig('overworld', 'tiles_overworld'),
        new TilesetImageConfig('inner', 'inner'),
      ],
      isEnemyZone: true,
    },
    mainscene: {
      mapName: 'larus',
      zoom: 2.5,
      isSound: true,
      soundAssetKey: 'path_to_lake_land',
      volume: 0.54,
      isSoundLoop: true,
      tileImages: [
        new TilesetImageConfig('collision', 'collision_tiles'),
        new TilesetImageConfig('inner', 'inner'),
        new TilesetImageConfig('base', 'tiles_overworld'),
      ],
      isEnemyZone: false,
    },
    intro: {
      mapName: 'intro22',
      zoom: 6.0,
      isSound: true,
      soundAssetKey: 'path_to_lake_land',
      volume: 0.2,
      isSoundLoop: true,
      tileImages: [
        new TilesetImageConfig('collision', 'collision_tiles'),
        new TilesetImageConfig('demo_interior', 'demo_interior'),
        new TilesetImageConfig('demo_room', 'demo_room'),
        new TilesetImageConfig('teacher', 'adam_tile'),
        new TilesetImageConfig('Bob_student', 'bob_tile'),
      ],
      isEnemyZone: false,
    },
    demo48x48test: {
      mapName: 'demo48x48',
      zoom: 1.2,
      isSound: false,
      tileImages: [
        new TilesetImageConfig('interior_free_ext48x48_ext', 'interior_free_ext48x48_ext', 48, 48, 1, 2),
        new TilesetImageConfig('room_builder_ext48x48_ext', 'room_builder_ext48x48_ext', 48, 48, 1, 2),
        new TilesetImageConfig('collision48x48_ext', 'collision48x48', 48, 48, 0, 0),
      ],
      isEnemyZone: false,
    },
    demo16x16_48test: {
      mapName: 'demo16x16_48',
      zoom: 1.2,
      isSound: false,
      tileImages: [
        new TilesetImageConfig('collision', 'collision_tiles'),
        new TilesetImageConfig('Room_Builder_48x48_free_ext', 'Room_Builder_16x16_48_free_ext'),
        new TilesetImageConfig('generic_layer_1_ext', 'generic_room_16x16_48'),
      ],
      isEnemyZone: false,
    },
  };
  return sceneInfo[sceneName] || sceneInfo.mainscene;
}
