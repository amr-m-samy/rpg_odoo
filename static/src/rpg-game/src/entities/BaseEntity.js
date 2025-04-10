export const BaseEntity = {
  /**
   * A Unique ID to identify the Entity.
   * @type { string }
   * @default
   * null
   */
  id: null,
  /**
   * Controls if the entity is atacking.
   * @type { boolean }
   * @default
   * False
   */
  isAtacking: false,
  /**
   * Controls if the player can atack.
   * @type { boolean }
   * @default
   * False
   */
  canAtack: false,
  /**
   * Controls if the player can move.
   * @type { boolean }
   * @default
   * True
   */
  canMove: true,
  /**
   * Controls if the entity can take damage.
   * @type { boolean }
   * @default
   * False
   */
  canTakeDamage: false,
  /**
   * This variable controls when the atack hitbox will appear.
   * @type { boolean }
   * @default
   * False
   */
  showHitBox: false,
  /**
   * The perception range of the entity. Usualy the field of view. For enemies it should be used to atack the player onde it's inside the perception radius.
   * @type { number }
   * @default
   * 75.0
   */
  perceptionRange: 75.0,
};
