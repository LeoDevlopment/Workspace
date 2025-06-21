// Made with Blockbench 4.12.4
// Exported for Minecraft version 1.17 or later with Mojang mappings
// Paste this class into your mod and generate all required imports


public class tankV4m1<T extends Entity> extends EntityModel<T> {
	// This layer location should be baked with EntityRendererProvider.Context in the entity renderer and passed into this model's constructor
	public static final ModelLayerLocation LAYER_LOCATION = new ModelLayerLocation(new ResourceLocation("modid", "tankv4m1"), "main");
	private final ModelPart trak;
	private final ModelPart body_trak;
	private final ModelPart body;
	private final ModelPart dop_el;
	private final ModelPart tower;
	private final ModelPart gun;
	private final ModelPart gun2;

	public tankV4m1(ModelPart root) {
		this.trak = root.getChild("trak");
		this.body_trak = root.getChild("body_trak");
		this.body = root.getChild("body");
		this.dop_el = root.getChild("dop_el");
		this.tower = root.getChild("tower");
		this.gun = root.getChild("gun");
		this.gun2 = root.getChild("gun2");
	}

	public static LayerDefinition createBodyLayer() {
		MeshDefinition meshdefinition = new MeshDefinition();
		PartDefinition partdefinition = meshdefinition.getRoot();

		PartDefinition trak = partdefinition.addOrReplaceChild("trak", CubeListBuilder.create().texOffs(550, 484).addBox(17.0F, -24.0F, -47.0F, 10.0F, 8.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(550, 494).addBox(17.0F, -16.4251F, 46.4215F, 10.0F, 8.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(0, 65).addBox(17.0F, -1.9399F, -24.0637F, 10.0F, 2.0F, 64.0F, new CubeDeformation(0.0F))
		.texOffs(128, 324).addBox(17.0F, -39.5564F, -31.4437F, 10.0F, 2.0F, 40.0F, new CubeDeformation(0.0F))
		.texOffs(550, 504).addBox(-27.0F, -24.0F, -47.0F, 10.0F, 8.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(468, 551).addBox(-27.0F, -16.4251F, 46.4215F, 10.0F, 8.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(0, 131).addBox(-27.0F, -1.9399F, -24.0637F, 10.0F, 2.0F, 64.0F, new CubeDeformation(0.0F))
		.texOffs(0, 327).addBox(-27.0F, -39.5564F, -31.4437F, 10.0F, 2.0F, 40.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 24.0F, 0.0F));

		PartDefinition cube_r1 = trak.addOrReplaceChild("cube_r1", CubeListBuilder.create().texOffs(512, 0).addBox(-9.0F, -28.0F, -1.0F, 10.0F, 28.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(86, 508).addBox(35.0F, -28.0F, -1.0F, 10.0F, 28.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.0F, -16.8192F, -46.4264F, -2.1817F, 0.0F, 0.0F));

		PartDefinition cube_r2 = trak.addOrReplaceChild("cube_r2", CubeListBuilder.create().texOffs(532, 60).addBox(-9.0F, -22.0F, -1.0F, 10.0F, 22.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(386, 530).addBox(35.0F, -22.0F, -1.0F, 10.0F, 22.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.0F, -23.2929F, -46.2929F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r3 = trak.addOrReplaceChild("cube_r3", CubeListBuilder.create().texOffs(538, 339).addBox(-9.0F, -12.0F, -1.0F, 10.0F, 12.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(538, 228).addBox(35.0F, -12.0F, -1.0F, 10.0F, 12.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.0F, -0.647F, 39.2291F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r4 = trak.addOrReplaceChild("cube_r4", CubeListBuilder.create().texOffs(24, 486).addBox(-9.0F, -46.0F, -1.0F, 10.0F, 46.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(0, 486).addBox(35.0F, -46.0F, -1.0F, 10.0F, 46.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.0F, -15.5591F, 47.9215F, 1.0472F, 0.0F, 0.0F));

		PartDefinition body_trak = partdefinition.addOrReplaceChild("body_trak", CubeListBuilder.create().texOffs(148, 65).addBox(25.8F, -15.9012F, -23.3878F, 1.0F, 14.0F, 63.0F, new CubeDeformation(0.0F))
		.texOffs(142, 219).addBox(17.0F, -6.9012F, -23.3878F, 1.0F, 5.0F, 63.0F, new CubeDeformation(0.0F))
		.texOffs(340, 393).addBox(17.0F, -37.6012F, -31.3878F, 1.0F, 1.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(404, 323).addBox(17.0F, -36.6012F, -30.3878F, 1.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(404, 39).addBox(17.0F, -35.6012F, -29.3878F, 1.0F, 2.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(386, 503).addBox(17.0F, -22.5012F, -44.9878F, 1.0F, 5.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(104, 566).addBox(17.0F, -15.3012F, 41.4122F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(158, 556).addBox(25.8F, -15.8652F, 39.5761F, 1.0F, 7.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(324, 348).addBox(25.8F, -37.5564F, -30.7936F, 1.0F, 6.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(334, 0).addBox(15.8F, -33.9564F, -29.1937F, 10.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(192, 0).addBox(15.8F, -7.5564F, -22.7936F, 10.0F, 1.0F, 61.0F, new CubeDeformation(0.0F))
		.texOffs(478, 265).addBox(15.8F, -22.7564F, -40.4937F, 10.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(426, 524).addBox(15.8F, -33.0564F, 7.5064F, 10.0F, 26.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(538, 242).addBox(16.8F, -15.0564F, 36.7064F, 9.0F, 5.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(322, 558).addBox(16.8F, -10.0564F, 31.7064F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(342, 558).addBox(16.8F, -9.0564F, 30.7064F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(174, 559).addBox(16.8F, -8.0564F, 29.7064F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(400, 477).addBox(25.8F, -31.7563F, -11.7936F, 1.0F, 16.0F, 20.0F, new CubeDeformation(0.0F))
		.texOffs(30, 564).addBox(25.8F, -36.7563F, 8.2064F, 1.0F, 21.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(142, 197).addBox(25.8F, -35.7563F, 9.2064F, 1.0F, 20.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(370, 565).addBox(25.8F, -34.7563F, 11.2064F, 1.0F, 19.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(34, 564).addBox(25.8F, -33.7563F, 12.2064F, 1.0F, 18.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(564, 559).addBox(25.8F, -32.7563F, 14.2064F, 1.0F, 17.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(374, 565).addBox(25.8F, -31.7563F, 16.2064F, 1.0F, 16.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(490, 565).addBox(25.8F, -30.7564F, 18.2064F, 1.0F, 15.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(116, 566).addBox(25.8F, -29.7564F, 20.2064F, 1.0F, 14.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(320, 568).addBox(25.8F, -28.7564F, 22.2064F, 1.0F, 13.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(354, 568).addBox(25.8F, -27.7564F, 24.2064F, 1.0F, 12.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(532, 569).addBox(25.8F, -25.7564F, 26.2064F, 1.0F, 10.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(120, 355).addBox(25.8F, -24.7564F, 28.2064F, 1.0F, 9.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(542, 377).addBox(25.8F, -23.7564F, 30.2064F, 1.0F, 8.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(578, 84).addBox(25.8F, -22.7564F, 32.2064F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(162, 576).addBox(25.8F, -21.7564F, 33.2064F, 1.0F, 6.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(102, 577).addBox(25.8F, -20.7564F, 35.2064F, 1.0F, 5.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(564, 185).addBox(25.8F, -19.7564F, 37.2064F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(546, 150).addBox(25.8F, -18.7564F, 38.2064F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 261).addBox(25.8F, -17.7564F, 40.2064F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(106, 538).addBox(25.8F, -16.7564F, 42.2064F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(524, 569).addBox(25.8F, -36.1063F, -31.7936F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(198, 569).addBox(25.8F, -17.1314F, -25.0187F, 1.0F, 14.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 213).addBox(25.8F, -8.8813F, 39.5814F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 302).addBox(25.8F, -8.8813F, 40.5814F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(384, 583).addBox(25.8F, -8.8813F, 41.5814F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 542).addBox(25.8F, -8.8813F, 42.5814F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(526, 585).addBox(25.8F, -8.8813F, 43.5814F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 160).addBox(25.8F, -8.8813F, 44.5814F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(528, 569).addBox(25.8F, -15.9063F, -24.2187F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(568, 266).addBox(25.8F, -17.1314F, -27.0187F, 1.0F, 13.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(360, 571).addBox(25.8F, -17.1314F, -28.0187F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(464, 573).addBox(25.8F, -17.1314F, -29.0187F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(310, 539).addBox(25.8F, -17.1314F, -31.0187F, 1.0F, 10.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(576, 122).addBox(25.8F, -17.1314F, -32.0187F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(576, 541).addBox(25.8F, -17.1314F, -33.0187F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(576, 550).addBox(25.8F, -17.1314F, -34.0187F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(84, 578).addBox(25.8F, -17.1314F, -35.0187F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(156, 576).addBox(25.8F, -17.1314F, -37.0187F, 1.0F, 6.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(24, 549).addBox(25.8F, -17.1314F, -38.0187F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(560, 210).addBox(25.8F, -17.1314F, -39.0187F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(532, 339).addBox(25.8F, -17.1314F, -41.0187F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(502, 512).addBox(25.8F, -17.1314F, -42.0187F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(0, 586).addBox(25.8F, -17.1314F, -43.0187F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(4, 586).addBox(25.8F, -17.1314F, -44.0187F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(276, 571).addBox(25.8F, -35.1063F, -32.7936F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(460, 573).addBox(25.8F, -34.1063F, -33.7936F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 530).addBox(25.8F, -33.1063F, -34.7936F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(184, 576).addBox(25.8F, -32.1063F, -35.7936F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(144, 577).addBox(25.8F, -31.1063F, -36.7936F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 92).addBox(25.8F, -30.1063F, -37.7936F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 206).addBox(25.8F, -29.1063F, -38.7936F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 281).addBox(25.8F, -28.1063F, -39.7936F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(374, 583).addBox(25.8F, -27.1063F, -40.7936F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(126, 552).addBox(25.8F, -26.1063F, -41.7936F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(66, 585).addBox(25.8F, -25.1063F, -42.7936F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 585).addBox(25.8F, -24.1063F, -43.7936F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(498, 360).addBox(25.8F, -23.1142F, -45.0108F, 1.0F, 6.0F, 21.0F, new CubeDeformation(0.0F))
		.texOffs(462, 166).addBox(25.8F, -32.1142F, -31.0108F, 1.0F, 9.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(0, 369).addBox(26.8F, -4.1262F, -7.6378F, 1.0F, 2.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(218, 514).addBox(26.8F, -3.1262F, -23.6378F, 1.0F, 1.0F, 16.0F, new CubeDeformation(0.0F))
		.texOffs(428, 579).addBox(26.8F, -10.1262F, -8.6378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(496, 565).addBox(26.8F, -10.1262F, -0.9378F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(582, 287).addBox(27.3F, -7.1262F, 0.5622F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 314).addBox(27.3F, -7.1262F, 10.5622F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 318).addBox(27.3F, -7.1262F, 20.5622F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(524, 60).addBox(27.3F, -11.1262F, 36.5622F, 1.0F, 3.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(566, 84).addBox(26.8F, -10.1262F, 9.0622F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(566, 95).addBox(26.8F, -10.1262F, 19.0622F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(464, 271).addBox(26.8F, -10.1262F, -23.6378F, 1.0F, 7.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(578, 108).addBox(26.8F, -10.1262F, -24.6378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(342, 191).addBox(26.8F, -11.1262F, -34.6378F, 1.0F, 1.0F, 27.0F, new CubeDeformation(0.0F))
		.texOffs(272, 473).addBox(26.4F, -12.1262F, -36.6378F, 1.0F, 1.0F, 30.0F, new CubeDeformation(0.0F))
		.texOffs(578, 178).addBox(26.4F, -11.1262F, -7.6378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 241).addBox(26.4F, -11.1262F, -1.9378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(522, 265).addBox(26.4F, -5.1262F, -6.7878F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(378, 550).addBox(26.4F, -5.1262F, 5.0622F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(542, 569).addBox(26.4F, -11.1262F, -0.9378F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(570, 137).addBox(26.4F, -11.1262F, 9.0622F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(570, 143).addBox(26.4F, -11.1262F, 19.0622F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(580, 12).addBox(26.4F, -5.1262F, 15.0622F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(158, 570).addBox(26.4F, -5.1262F, 25.0622F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(578, 262).addBox(26.4F, -11.1262F, 4.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 270).addBox(26.4F, -11.1262F, 8.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 302).addBox(26.4F, -11.1262F, 14.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 310).addBox(26.4F, -11.1262F, 18.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 318).addBox(26.4F, -11.1262F, 24.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(570, 573).addBox(26.4F, -15.1262F, 29.4372F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(48, 527).addBox(26.4F, -16.1262F, 29.4372F, 1.0F, 1.0F, 15.0F, new CubeDeformation(0.0F))
		.texOffs(414, 389).addBox(26.4F, -15.1262F, 30.4372F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(84, 557).addBox(26.8F, -10.1262F, -33.6378F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(518, 439).addBox(26.8F, -15.1973F, 32.4332F, 1.0F, 6.0F, 14.0F, new CubeDeformation(0.0F))
		.texOffs(580, 124).addBox(26.8F, -13.1973F, 30.4332F, 1.0F, 4.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(282, 549).addBox(26.8F, -9.1973F, 30.4332F, 1.0F, 7.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(580, 227).addBox(26.8F, -9.1973F, 39.4332F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 308).addBox(26.8F, -9.1973F, 40.4332F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(536, 583).addBox(26.8F, -9.1973F, 41.4332F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(278, 584).addBox(26.8F, -9.1973F, 42.4332F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 554).addBox(26.8F, -9.1973F, 43.4332F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(8, 586).addBox(26.8F, -9.1973F, 44.4332F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(260, 393).addBox(26.8F, -37.1814F, -30.7936F, 1.0F, 1.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(538, 353).addBox(26.8F, -23.0392F, -44.9358F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 344).addBox(26.3F, -21.0392F, -40.9358F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 222).addBox(27.3F, -21.5392F, -33.4358F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(580, 292).addBox(27.3F, -21.5392F, -37.4358F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(110, 508).addBox(26.8F, -21.0392F, -39.9358F, 1.0F, 2.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(556, 583).addBox(26.8F, -18.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(16, 584).addBox(26.8F, -20.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(450, 512).addBox(25.8F, -31.2392F, -23.9108F, 1.0F, 15.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(584, 21).addBox(26.8F, -30.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(584, 24).addBox(26.8F, -28.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(34, 584).addBox(26.8F, -29.0392F, -25.5108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(44, 584).addBox(26.8F, -19.0392F, -25.5108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(400, 39).addBox(26.3F, -31.7392F, -24.0108F, 1.0F, 16.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(524, 547).addBox(26.3F, -16.7392F, -23.4108F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F))
		.texOffs(548, 439).addBox(26.3F, -31.7392F, -23.4108F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F))
		.texOffs(152, 450).addBox(26.3F, -31.7392F, -12.7108F, 1.0F, 16.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(302, 551).addBox(26.3F, -22.5392F, -39.5358F, 1.0F, 5.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(580, 402).addBox(16.0F, -23.0392F, -44.9358F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 70).addBox(16.0F, -22.0392F, -40.9358F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 428).addBox(16.0F, -22.0392F, -41.9358F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 75).addBox(16.0F, -22.0392F, -43.9358F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(262, 585).addBox(16.0F, -21.0392F, -42.9358F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(394, 283).addBox(16.0F, -37.1814F, -30.7936F, 1.0F, 1.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(0, 410).addBox(16.0F, -36.1814F, -29.7936F, 1.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(378, 440).addBox(16.0F, -35.1814F, -28.7936F, 1.0F, 1.0F, 36.0F, new CubeDeformation(0.0F))
		.texOffs(270, 219).addBox(16.0F, -3.1262F, -23.6378F, 1.0F, 1.0F, 63.0F, new CubeDeformation(0.0F))
		.texOffs(276, 126).addBox(16.0F, -7.1262F, -22.6378F, 1.0F, 4.0F, 61.0F, new CubeDeformation(0.0F))
		.texOffs(562, 345).addBox(11.0F, -6.9546F, 33.1906F, 5.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(580, 334).addBox(16.0F, -15.1973F, 45.4332F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(354, 582).addBox(16.0F, -15.1973F, 41.4332F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(390, 570).addBox(11.0F, -15.1973F, 41.4332F, 5.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 402).addBox(16.0F, -14.1973F, 43.4332F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 65).addBox(16.0F, -14.1973F, 44.4332F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 583).addBox(16.0F, -14.1973F, 42.4332F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(148, 142).addBox(-26.8F, -15.9012F, -23.3878F, 1.0F, 14.0F, 63.0F, new CubeDeformation(0.0F))
		.texOffs(0, 259).addBox(-18.0F, -6.9012F, -23.3878F, 1.0F, 5.0F, 63.0F, new CubeDeformation(0.0F))
		.texOffs(398, 191).addBox(-18.0F, -37.6012F, -31.3878F, 1.0F, 1.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(420, 401).addBox(-18.0F, -36.6012F, -30.3878F, 1.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(404, 79).addBox(-18.0F, -35.6012F, -29.3878F, 1.0F, 2.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(568, 0).addBox(-18.0F, -22.5012F, -44.9878F, 1.0F, 5.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(566, 302).addBox(-18.0F, -15.3012F, 41.4122F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(234, 559).addBox(-26.8F, -15.8652F, 39.5761F, 1.0F, 7.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(100, 366).addBox(-26.8F, -37.5564F, -30.7936F, 1.0F, 6.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(228, 348).addBox(-25.8F, -33.9564F, -29.1937F, 10.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(0, 197).addBox(-25.8F, -7.5564F, -22.7936F, 10.0F, 1.0F, 61.0F, new CubeDeformation(0.0F))
		.texOffs(552, 541).addBox(-25.8F, -22.7564F, -40.4937F, 10.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(252, 526).addBox(-25.8F, -33.0564F, 7.5064F, 10.0F, 26.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(282, 539).addBox(-25.8F, -15.0564F, 36.7064F, 9.0F, 5.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(524, 559).addBox(-17.8F, -10.0564F, 31.7064F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(544, 559).addBox(-17.8F, -9.0564F, 30.7064F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(560, 190).addBox(-17.8F, -8.0564F, 29.7064F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(482, 30).addBox(-26.8F, -31.7563F, -11.7936F, 1.0F, 16.0F, 20.0F, new CubeDeformation(0.0F))
		.texOffs(40, 564).addBox(-26.8F, -36.7563F, 8.2064F, 1.0F, 21.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(250, 562).addBox(-26.8F, -35.7563F, 9.2064F, 1.0F, 20.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(380, 565).addBox(-26.8F, -34.7563F, 11.2064F, 1.0F, 19.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(44, 564).addBox(-26.8F, -33.7563F, 12.2064F, 1.0F, 18.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(290, 565).addBox(-26.8F, -32.7563F, 14.2064F, 1.0F, 17.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(384, 565).addBox(-26.8F, -31.7563F, 16.2064F, 1.0F, 16.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(508, 565).addBox(-26.8F, -30.7564F, 18.2064F, 1.0F, 15.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(96, 567).addBox(-26.8F, -29.7564F, 20.2064F, 1.0F, 14.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(326, 568).addBox(-26.8F, -28.7564F, 22.2064F, 1.0F, 13.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(188, 569).addBox(-26.8F, -27.7564F, 24.2064F, 1.0F, 12.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(402, 570).addBox(-26.8F, -25.7564F, 26.2064F, 1.0F, 10.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(234, 573).addBox(-26.8F, -24.7564F, 28.2064F, 1.0F, 9.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(574, 402).addBox(-26.8F, -23.7564F, 30.2064F, 1.0F, 8.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(88, 578).addBox(-26.8F, -22.7564F, 32.2064F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(576, 164).addBox(-26.8F, -21.7564F, 33.2064F, 1.0F, 6.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(108, 577).addBox(-26.8F, -20.7564F, 35.2064F, 1.0F, 5.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(188, 583).addBox(-26.8F, -19.7564F, 37.2064F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 196).addBox(-26.8F, -18.7564F, 38.2064F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 265).addBox(-26.8F, -17.7564F, 40.2064F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(584, 557).addBox(-26.8F, -16.7564F, 42.2064F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(570, 559).addBox(-26.8F, -36.1063F, -31.7936F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(202, 569).addBox(-26.8F, -17.1314F, -25.0187F, 1.0F, 14.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 581).addBox(-26.8F, -8.8813F, 39.5814F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 458).addBox(-26.8F, -8.8813F, 40.5814F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 152).addBox(-26.8F, -8.8813F, 41.5814F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(544, 584).addBox(-26.8F, -8.8813F, 42.5814F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(570, 585).addBox(-26.8F, -8.8813F, 43.5814F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 162).addBox(-26.8F, -8.8813F, 44.5814F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(126, 571).addBox(-26.8F, -15.9063F, -24.2187F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(332, 568).addBox(-26.8F, -17.1314F, -27.0187F, 1.0F, 13.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(240, 573).addBox(-26.8F, -17.1314F, -28.0187F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(308, 574).addBox(-26.8F, -17.1314F, -29.0187F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(130, 571).addBox(-26.8F, -17.1314F, -31.0187F, 1.0F, 10.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(174, 576).addBox(-26.8F, -17.1314F, -32.0187F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(136, 577).addBox(-26.8F, -17.1314F, -33.0187F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(140, 577).addBox(-26.8F, -17.1314F, -34.0187F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(92, 578).addBox(-26.8F, -17.1314F, -35.0187F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(178, 576).addBox(-26.8F, -17.1314F, -37.0187F, 1.0F, 6.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 269).addBox(-26.8F, -17.1314F, -38.0187F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(230, 583).addBox(-26.8F, -17.1314F, -39.0187F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 201).addBox(-26.8F, -17.1314F, -41.0187F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(174, 556).addBox(-26.8F, -17.1314F, -42.0187F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 35).addBox(-26.8F, -17.1314F, -43.0187F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 37).addBox(-26.8F, -17.1314F, -44.0187F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(244, 573).addBox(-26.8F, -35.1063F, -32.7936F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(408, 574).addBox(-26.8F, -34.1063F, -33.7936F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(12, 575).addBox(-26.8F, -33.1063F, -34.7936F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(434, 576).addBox(-26.8F, -32.1063F, -35.7936F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 46).addBox(-26.8F, -31.1063F, -36.7936F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 458).addBox(-26.8F, -30.1063F, -37.7936F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 28).addBox(-26.8F, -29.1063F, -38.7936F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 482).addBox(-26.8F, -28.1063F, -39.7936F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(156, 584).addBox(-26.8F, -27.1063F, -40.7936F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 470).addBox(-26.8F, -26.1063F, -41.7936F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(332, 585).addBox(-26.8F, -25.1063F, -42.7936F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 39).addBox(-26.8F, -24.1063F, -43.7936F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(334, 503).addBox(-26.8F, -23.1142F, -45.0108F, 1.0F, 6.0F, 21.0F, new CubeDeformation(0.0F))
		.texOffs(392, 554).addBox(-26.8F, -32.1142F, -31.0108F, 1.0F, 9.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(180, 387).addBox(-27.8F, -4.1262F, -7.6378F, 1.0F, 2.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(502, 515).addBox(-27.8F, -3.1262F, -23.6378F, 1.0F, 1.0F, 16.0F, new CubeDeformation(0.0F))
		.texOffs(72, 580).addBox(-27.8F, -10.1262F, -8.6378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(566, 313).addBox(-27.8F, -10.1262F, -0.9378F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(490, 582).addBox(-28.3F, -7.1262F, 0.5622F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 494).addBox(-28.3F, -7.1262F, 10.5622F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(496, 582).addBox(-28.3F, -7.1262F, 20.5622F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(576, 438).addBox(-28.3F, -11.1262F, 36.5622F, 1.0F, 3.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(566, 353).addBox(-27.8F, -10.1262F, 9.0622F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(566, 364).addBox(-27.8F, -10.1262F, 19.0622F, 1.0F, 6.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(568, 178).addBox(-27.8F, -10.1262F, -23.6378F, 1.0F, 7.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(578, 490).addBox(-27.8F, -10.1262F, -24.6378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(74, 480).addBox(-27.8F, -11.1262F, -34.6378F, 1.0F, 1.0F, 27.0F, new CubeDeformation(0.0F))
		.texOffs(474, 271).addBox(-27.4F, -12.1262F, -36.6378F, 1.0F, 1.0F, 30.0F, new CubeDeformation(0.0F))
		.texOffs(578, 530).addBox(-27.4F, -11.1262F, -7.6378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 559).addBox(-27.4F, -11.1262F, -1.9378F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(136, 571).addBox(-27.4F, -5.1262F, -6.7878F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(578, 186).addBox(-27.4F, -5.1262F, 5.0622F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(572, 149).addBox(-27.4F, -11.1262F, -0.9378F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(572, 155).addBox(-27.4F, -11.1262F, 9.0622F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(572, 375).addBox(-27.4F, -11.1262F, 19.0622F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(580, 120).addBox(-27.4F, -5.1262F, 15.0622F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(572, 381).addBox(-27.4F, -5.1262F, 25.0622F, 1.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(562, 578).addBox(-27.4F, -11.1262F, 4.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(566, 578).addBox(-27.4F, -11.1262F, 8.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 567).addBox(-27.4F, -11.1262F, 14.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 575).addBox(-27.4F, -11.1262F, 18.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(424, 579).addBox(-27.4F, -11.1262F, 24.0622F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 412).addBox(-27.4F, -15.1262F, 29.4372F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(334, 530).addBox(-27.4F, -16.1262F, 29.4372F, 1.0F, 1.0F, 15.0F, new CubeDeformation(0.0F))
		.texOffs(538, 252).addBox(-27.4F, -15.1262F, 30.4372F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(560, 200).addBox(-27.8F, -10.1262F, -33.6378F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(110, 520).addBox(-27.8F, -15.1973F, 32.4332F, 1.0F, 6.0F, 14.0F, new CubeDeformation(0.0F))
		.texOffs(580, 190).addBox(-27.8F, -13.1973F, 30.4332F, 1.0F, 4.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(448, 549).addBox(-27.8F, -9.1973F, 30.4332F, 1.0F, 7.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(582, 35).addBox(-27.8F, -9.1973F, 39.4332F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 528).addBox(-27.8F, -9.1973F, 40.4332F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(160, 584).addBox(-27.8F, -9.1973F, 41.4332F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 474).addBox(-27.8F, -9.1973F, 42.4332F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(62, 585).addBox(-27.8F, -9.1973F, 43.4332F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(40, 586).addBox(-27.8F, -9.1973F, 44.4332F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(398, 231).addBox(-27.8F, -37.1814F, -30.7936F, 1.0F, 1.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(582, 42).addBox(-27.8F, -23.0392F, -44.9358F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 522).addBox(-27.3F, -21.0392F, -40.9358F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 241).addBox(-28.3F, -21.5392F, -33.4358F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 16).addBox(-28.3F, -21.5392F, -37.4358F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(252, 514).addBox(-27.8F, -21.0392F, -39.9358F, 1.0F, 2.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(584, 157).addBox(-27.8F, -18.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(164, 584).addBox(-27.8F, -20.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(476, 512).addBox(-26.8F, -31.2392F, -23.9108F, 1.0F, 15.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(584, 171).addBox(-27.8F, -30.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(584, 174).addBox(-27.8F, -28.0392F, -26.0108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(178, 584).addBox(-27.8F, -29.0392F, -25.5108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(192, 584).addBox(-27.8F, -19.0392F, -25.5108F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(122, 566).addBox(-27.3F, -31.7392F, -24.0108F, 1.0F, 16.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(548, 547).addBox(-27.3F, -16.7392F, -23.4108F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F))
		.texOffs(0, 549).addBox(-27.3F, -31.7392F, -23.4108F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F))
		.texOffs(338, 568).addBox(-27.3F, -31.7392F, -12.7108F, 1.0F, 16.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(426, 551).addBox(-27.3F, -22.5392F, -39.5358F, 1.0F, 5.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(582, 49).addBox(-17.0F, -23.0392F, -44.9358F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(170, 584).addBox(-17.0F, -22.0392F, -40.9358F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(476, 584).addBox(-17.0F, -22.0392F, -41.9358F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(198, 584).addBox(-17.0F, -22.0392F, -43.9358F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(378, 585).addBox(-17.0F, -21.0392F, -42.9358F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(400, 126).addBox(-17.0F, -37.1814F, -30.7936F, 1.0F, 1.0F, 39.0F, new CubeDeformation(0.0F))
		.texOffs(156, 428).addBox(-17.0F, -36.1814F, -29.7936F, 1.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(0, 449).addBox(-17.0F, -35.1814F, -28.7936F, 1.0F, 1.0F, 36.0F, new CubeDeformation(0.0F))
		.texOffs(276, 62).addBox(-17.0F, -3.1262F, -23.6378F, 1.0F, 1.0F, 63.0F, new CubeDeformation(0.0F))
		.texOffs(270, 283).addBox(-17.0F, -7.1262F, -22.6378F, 1.0F, 4.0F, 61.0F, new CubeDeformation(0.0F))
		.texOffs(562, 520).addBox(-16.0F, -6.9546F, 33.1906F, 5.0F, 1.0F, 5.0F, new CubeDeformation(0.0F))
		.texOffs(582, 56).addBox(-17.0F, -15.1973F, 45.4332F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 559).addBox(-17.0F, -15.1973F, 41.4332F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(572, 387).addBox(-16.0F, -15.1973F, 41.4332F, 5.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 478).addBox(-17.0F, -14.1973F, 43.4332F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(202, 584).addBox(-17.0F, -14.1973F, 44.4332F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 206).addBox(-17.0F, -14.1973F, 42.4332F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 24.0F, 0.0F));

		PartDefinition cube_r5 = body_trak.addOrReplaceChild("cube_r5", CubeListBuilder.create().texOffs(578, 55).addBox(-9.0F, -25.975F, -1.975F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(456, 585).addBox(-9.0F, -23.975F, -4.975F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 211).addBox(-9.0F, -24.675F, -3.975F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 84).addBox(-9.0F, -25.375F, -2.975F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(472, 575).addBox(-9.0F, -26.675F, -0.975F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(148, 571).addBox(-9.0F, -27.975F, 0.025F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(410, 530).addBox(1.8F, -28.0F, -2.975F, 1.0F, 26.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(230, 569).addBox(-9.0F, -15.0F, 0.025F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(342, 577).addBox(45.6F, -25.975F, -1.975F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(148, 585).addBox(45.6F, -23.975F, -4.975F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(552, 583).addBox(45.6F, -24.675F, -3.975F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 254).addBox(45.6F, -25.375F, -2.975F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 559).addBox(45.6F, -26.675F, -0.975F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(538, 569).addBox(45.6F, -27.975F, 0.025F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(404, 362).addBox(34.8F, -28.0F, -2.975F, 1.0F, 26.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(266, 334).addBox(45.6F, -15.0F, 0.025F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.8F, -19.026F, -45.9862F, -2.1817F, 0.0F, 0.0F));

		PartDefinition cube_r6 = body_trak.addOrReplaceChild("cube_r6", CubeListBuilder.create().texOffs(564, 210).addBox(-8.0F, -10.0F, -5.875F, 5.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(84, 567).addBox(-8.0F, -9.0F, -4.875F, 5.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(342, 568).addBox(-8.0F, -8.0F, -3.875F, 5.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(206, 569).addBox(-8.0F, -7.0F, -2.875F, 5.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(564, 122).addBox(19.0F, -10.0F, -5.875F, 5.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(566, 241).addBox(19.0F, -9.0F, -4.875F, 5.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(568, 10).addBox(19.0F, -8.0F, -3.875F, 5.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(322, 550).addBox(19.0F, -7.0F, -2.875F, 5.0F, 6.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-8.0F, -3.9217F, 38.8093F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r7 = body_trak.addOrReplaceChild("cube_r7", CubeListBuilder.create().texOffs(424, 565).addBox(-9.0F, -9.0F, -2.875F, 1.0F, 10.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(468, 575).addBox(-19.8F, -9.0F, 0.125F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(242, 531).addBox(24.0F, -9.0F, -2.875F, 1.0F, 10.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(518, 574).addBox(34.8F, -9.0F, 0.125F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-8.0F, -3.6288F, 39.2738F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r8 = body_trak.addOrReplaceChild("cube_r8", CubeListBuilder.create().texOffs(378, 503).addBox(-9.0F, -45.0F, -1.275F, 1.0F, 44.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(278, 526).addBox(-19.8F, -45.0F, 0.725F, 1.0F, 44.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(442, 477).addBox(24.0F, -45.0F, -1.275F, 1.0F, 44.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(330, 504).addBox(34.8F, -45.0F, 0.725F, 1.0F, 44.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-8.0F, -13.2034F, 46.4368F, 1.0472F, 0.0F, 0.0F));

		PartDefinition cube_r9 = body_trak.addOrReplaceChild("cube_r9", CubeListBuilder.create().texOffs(394, 323).addBox(-9.0F, -20.0F, -1.125F, 1.0F, 20.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(564, 264).addBox(-19.8F, -20.0F, -1.125F, 1.0F, 20.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(128, 259).addBox(24.0F, -20.0F, -1.125F, 1.0F, 20.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(64, 564).addBox(34.8F, -20.0F, -1.125F, 1.0F, 20.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-8.0F, -22.2437F, -44.1403F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r10 = body_trak.addOrReplaceChild("cube_r10", CubeListBuilder.create().texOffs(368, 585).addBox(-9.0F, -5.0F, 3.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(258, 585).addBox(44.6F, -5.0F, 3.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.3F, -23.989F, -40.2287F, -2.3562F, 0.0F, 0.0F));

		PartDefinition cube_r11 = body_trak.addOrReplaceChild("cube_r11", CubeListBuilder.create().texOffs(364, 585).addBox(-9.0F, -5.0F, 3.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(254, 585).addBox(44.6F, -5.0F, 3.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.3F, -21.0392F, -45.1784F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r12 = body_trak.addOrReplaceChild("cube_r12", CubeListBuilder.create().texOffs(336, 585).addBox(-9.0F, -3.0F, -1.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(126, 585).addBox(45.6F, -3.0F, -1.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.8F, -2.4402F, 29.0653F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r13 = body_trak.addOrReplaceChild("cube_r13", CubeListBuilder.create().texOffs(580, 297).addBox(-9.0F, -3.0F, -1.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(580, 249).addBox(45.6F, -3.0F, -1.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.8F, -12.4402F, 31.0653F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r14 = body_trak.addOrReplaceChild("cube_r14", CubeListBuilder.create().texOffs(582, 518).addBox(-9.0F, -18.0F, 5.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 514).addBox(-9.0F, -6.5F, 5.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(508, 582).addBox(-9.0F, 4.0F, 5.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 330).addBox(45.6F, -18.0F, 5.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 326).addBox(45.6F, -6.5F, 5.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 322).addBox(45.6F, 4.0F, 5.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-18.8F, -19.1262F, 20.5622F, 1.0472F, 0.0F, 0.0F));

		PartDefinition cube_r15 = body_trak.addOrReplaceChild("cube_r15", CubeListBuilder.create().texOffs(582, 488).addBox(-9.0F, -7.0F, -2.875F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 482).addBox(-9.0F, -8.0F, -1.875F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(438, 576).addBox(-9.0F, -9.0F, -0.875F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(412, 574).addBox(-9.0F, -10.0F, 0.125F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(304, 574).addBox(-17.8F, -10.0F, 0.125F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 353).addBox(26.0F, -7.0F, -2.875F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 326).addBox(26.0F, -8.0F, -1.875F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(206, 576).addBox(26.0F, -9.0F, -0.875F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 41).addBox(26.0F, -10.0F, 0.125F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(456, 573).addBox(34.8F, -10.0F, 0.125F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-9.0F, -3.2967F, 38.9167F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r16 = body_trak.addOrReplaceChild("cube_r16", CubeListBuilder.create().texOffs(366, 530).addBox(-9.0F, -45.0F, -1.275F, 1.0F, 41.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(274, 526).addBox(-9.0F, -46.0F, -0.275F, 1.0F, 44.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(326, 504).addBox(-9.0F, -46.0F, 0.725F, 1.0F, 45.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(318, 504).addBox(-17.8F, -47.0F, 0.725F, 1.0F, 46.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(80, 527).addBox(26.0F, -45.0F, -1.275F, 1.0F, 41.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(422, 513).addBox(26.0F, -46.0F, -0.275F, 1.0F, 44.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(322, 504).addBox(26.0F, -46.0F, 0.725F, 1.0F, 45.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(266, 287).addBox(34.8F, -47.0F, 0.725F, 1.0F, 46.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-9.0F, -13.3693F, 46.3672F, 1.0472F, 0.0F, 0.0F));

		PartDefinition cube_r17 = body_trak.addOrReplaceChild("cube_r17", CubeListBuilder.create().texOffs(316, 565).addBox(-9.0F, -20.0F, 1.875F, 1.0F, 19.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(564, 164).addBox(-9.0F, -20.0F, 0.875F, 1.0F, 20.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(484, 561).addBox(-9.0F, -20.0F, -1.125F, 1.0F, 21.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(22, 564).addBox(-17.8F, -20.0F, -1.125F, 1.0F, 21.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(312, 565).addBox(26.0F, -20.0F, 1.875F, 1.0F, 19.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(68, 564).addBox(26.0F, -20.0F, 0.875F, 1.0F, 20.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(16, 561).addBox(26.0F, -20.0F, -1.125F, 1.0F, 21.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(70, 486).addBox(34.8F, -20.0F, -1.125F, 1.0F, 21.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-9.0F, -22.6187F, -44.0153F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r18 = body_trak.addOrReplaceChild("cube_r18", CubeListBuilder.create().texOffs(260, 562).addBox(-9.0F, -26.0F, -3.975F, 1.0F, 22.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(26, 564).addBox(-9.0F, -26.0F, -2.975F, 1.0F, 21.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(72, 555).addBox(-9.0F, -27.0F, -1.975F, 1.0F, 24.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(76, 543).addBox(-9.0F, -28.0F, -0.975F, 1.0F, 26.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(124, 327).addBox(-9.0F, -28.0F, 0.025F, 1.0F, 27.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(120, 327).addBox(-17.8F, -28.0F, 0.025F, 1.0F, 27.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(256, 562).addBox(26.0F, -26.0F, -3.975F, 1.0F, 22.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(564, 0).addBox(26.0F, -26.0F, -2.975F, 1.0F, 21.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(362, 546).addBox(26.0F, -27.0F, -1.975F, 1.0F, 24.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(414, 362).addBox(26.0F, -28.0F, -0.975F, 1.0F, 26.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(262, 287).addBox(26.0F, -28.0F, 0.025F, 1.0F, 27.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(138, 259).addBox(34.8F, -28.0F, 0.025F, 1.0F, 27.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-9.0F, -18.801F, -45.7362F, -2.1817F, 0.0F, 0.0F));

		PartDefinition cube_r19 = body_trak.addOrReplaceChild("cube_r19", CubeListBuilder.create().texOffs(130, 480).addBox(-8.0F, -7.0F, -0.35F, 10.0F, 16.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(156, 411).addBox(33.6F, -7.0F, -0.35F, 10.0F, 16.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-17.8F, -28.816F, -33.9533F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r20 = body_trak.addOrReplaceChild("cube_r20", CubeListBuilder.create().texOffs(562, 514).addBox(-8.0F, -5.0F, -0.35F, 9.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(540, 190).addBox(34.6F, -5.0F, -0.35F, 9.0F, 5.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-17.8F, -7.016F, 37.7467F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r21 = body_trak.addOrReplaceChild("cube_r21", CubeListBuilder.create().texOffs(556, 79).addBox(-8.0F, -27.0F, -4.35F, 10.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(556, 459).addBox(-8.0F, -29.0F, -3.35F, 10.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(550, 390).addBox(-8.0F, -31.0F, -2.35F, 10.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(538, 196).addBox(-8.0F, -35.0F, -1.35F, 10.0F, 18.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(80, 369).addBox(-8.0F, -38.0F, -0.35F, 9.0F, 38.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(500, 265).addBox(33.6F, -27.0F, -4.35F, 10.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(556, 70).addBox(33.6F, -29.0F, -3.35F, 10.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(550, 377).addBox(33.6F, -31.0F, -2.35F, 10.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(84, 538).addBox(33.6F, -35.0F, -1.35F, 10.0F, 18.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(100, 327).addBox(34.6F, -38.0F, -0.35F, 9.0F, 38.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-17.8F, -14.4934F, 41.3813F, 1.0472F, 0.0F, 0.0F));

		PartDefinition cube_r22 = body_trak.addOrReplaceChild("cube_r22", CubeListBuilder.create().texOffs(502, 532).addBox(-8.0F, -21.0F, -0.35F, 10.0F, 21.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(48, 486).addBox(33.6F, -21.0F, -0.35F, 10.0F, 21.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-17.8F, -6.843F, -22.5929F, 0.9599F, 0.0F, 0.0F));

		PartDefinition body = partdefinition.addOrReplaceChild("body", CubeListBuilder.create().texOffs(0, 0).addBox(-16.0F, -7.7F, -30.1F, 32.0F, 1.0F, 64.0F, new CubeDeformation(0.0F))
		.texOffs(78, 411).addBox(15.0F, -8.7F, -30.1F, 1.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(576, 172).addBox(15.0F, -22.4F, -42.5F, 1.0F, 3.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(582, 365).addBox(15.0F, -19.4F, -42.5F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(452, 471).addBox(15.0F, -22.7F, 7.9F, 1.0F, 15.0F, 26.0F, new CubeDeformation(0.0F))
		.texOffs(80, 569).addBox(15.0F, -36.7F, 7.9F, 1.0F, 14.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(126, 556).addBox(15.0F, -22.7F, 33.9F, 1.0F, 8.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(578, 412).addBox(15.0F, -14.7F, 33.9F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 552).addBox(15.0F, -14.7F, 34.9F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 412).addBox(15.0F, -14.7F, 35.9F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(102, 584).addBox(15.0F, -14.7F, 36.9F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 446).addBox(15.0F, -14.7F, 37.9F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(316, 585).addBox(15.0F, -14.7F, 38.9F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 29).addBox(15.0F, -14.7F, 39.9F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(128, 287).addBox(-16.0F, -40.1407F, -26.943F, 32.0F, 2.0F, 35.0F, new CubeDeformation(0.0F))
		.texOffs(584, 80).addBox(15.0F, -34.1407F, -28.943F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(30, 586).addBox(15.0F, -35.1407F, -27.943F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(234, 433).addBox(15.0F, -38.1407F, -26.943F, 1.0F, 5.0F, 35.0F, new CubeDeformation(0.0F))
		.texOffs(478, 256).addBox(-16.0F, -22.4782F, 40.6782F, 32.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(276, 191).addBox(8.0F, -23.4782F, 16.6782F, 8.0F, 1.0F, 25.0F, new CubeDeformation(0.0F))
		.texOffs(240, 62).addBox(-8.0F, -23.4782F, 40.6782F, 16.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(554, 569).addBox(-8.0F, -35.4782F, 17.6782F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(174, 532).addBox(-8.0F, -35.9782F, 15.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 483).addBox(-8.0F, -36.2782F, 14.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(218, 576).addBox(-8.0F, -36.5782F, 13.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(262, 315).addBox(-8.0F, -36.7782F, 12.6782F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 538).addBox(-8.0F, -37.0782F, 11.6782F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 359).addBox(-8.0F, -37.3782F, 10.6782F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(76, 584).addBox(-8.0F, -37.6032F, 9.6782F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(266, 585).addBox(-8.0F, -37.8782F, 8.6782F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(12, 586).addBox(-8.0F, -37.9782F, 7.6782F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(558, 569).addBox(-8.0F, -35.7032F, 16.6782F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(482, 66).addBox(-8.0F, -23.4032F, 16.0782F, 1.0F, 1.0F, 24.0F, new CubeDeformation(0.0F))
		.texOffs(482, 91).addBox(7.0F, -23.4032F, 16.0782F, 1.0F, 1.0F, 24.0F, new CubeDeformation(0.0F))
		.texOffs(364, 572).addBox(-8.0F, -35.1782F, 18.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(572, 438).addBox(-8.0F, -34.9782F, 19.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(152, 571).addBox(-8.0F, -34.7782F, 20.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(448, 573).addBox(-8.0F, -34.3782F, 21.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 53).addBox(-8.0F, -34.1782F, 22.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(416, 574).addBox(-8.0F, -33.8782F, 23.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 266).addBox(-8.0F, -33.5782F, 24.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(548, 575).addBox(-8.0F, -33.3782F, 25.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 570).addBox(-8.0F, -33.0782F, 26.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 424).addBox(-8.0F, -32.7782F, 27.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(0, 575).addBox(-8.0F, -32.5782F, 28.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(54, 576).addBox(-8.0F, -32.2782F, 29.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(210, 576).addBox(-8.0F, -31.9782F, 30.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(576, 210).addBox(-8.0F, -31.7032F, 31.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(214, 576).addBox(-8.0F, -31.4532F, 32.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(346, 577).addBox(-8.0F, -31.1532F, 33.6782F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(350, 577).addBox(-8.0F, -30.9032F, 34.6782F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 353).addBox(-8.0F, -29.9032F, 35.6782F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(394, 582).addBox(-8.0F, -27.9032F, 36.6782F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 438).addBox(-8.0F, -25.9032F, 37.6782F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(22, 586).addBox(-8.0F, -23.9032F, 38.6782F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 27).addBox(7.0F, -23.9032F, 38.6782F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 442).addBox(7.0F, -25.9032F, 37.6782F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(402, 582).addBox(7.0F, -27.9032F, 36.6782F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 361).addBox(7.0F, -29.9032F, 35.6782F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 37).addBox(7.0F, -30.9032F, 34.6782F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 28).addBox(7.0F, -31.1532F, 33.6782F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(390, 576).addBox(7.0F, -31.4532F, 32.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(576, 252).addBox(7.0F, -31.7032F, 31.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(226, 576).addBox(7.0F, -31.9782F, 30.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(58, 576).addBox(7.0F, -32.2782F, 29.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(8, 575).addBox(7.0F, -32.5782F, 28.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(514, 574).addBox(7.0F, -32.7782F, 27.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(4, 575).addBox(7.0F, -33.0782F, 26.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(50, 576).addBox(7.0F, -33.3782F, 25.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(300, 574).addBox(7.0F, -33.5782F, 24.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(420, 574).addBox(7.0F, -33.8782F, 23.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(296, 574).addBox(7.0F, -34.1782F, 22.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(452, 573).addBox(7.0F, -34.3782F, 21.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(272, 571).addBox(7.0F, -34.7782F, 20.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(572, 546).addBox(7.0F, -34.9782F, 19.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(572, 470).addBox(7.0F, -35.1782F, 18.6782F, 1.0F, 12.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(170, 570).addBox(7.0F, -35.4782F, 17.6782F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(76, 570).addBox(7.0F, -35.7032F, 16.6782F, 1.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(26, 586).addBox(7.0F, -37.9782F, 7.6782F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(312, 585).addBox(7.0F, -37.8782F, 8.6782F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(80, 584).addBox(7.0F, -37.6032F, 9.6782F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(398, 582).addBox(7.0F, -37.3782F, 10.6782F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 545).addBox(7.0F, -37.0782F, 11.6782F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(532, 110).addBox(7.0F, -36.7782F, 12.6782F, 1.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(222, 576).addBox(7.0F, -36.5782F, 13.6782F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 494).addBox(7.0F, -36.2782F, 14.6782F, 1.0F, 10.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(358, 546).addBox(7.0F, -35.9782F, 15.6782F, 1.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(334, 477).addBox(-16.0F, -23.4782F, 16.6782F, 8.0F, 1.0F, 25.0F, new CubeDeformation(0.0F))
		.texOffs(480, 147).addBox(-16.0F, -22.8772F, -43.2064F, 32.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(142, 556).addBox(-16.0F, -22.7F, 33.9F, 1.0F, 8.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(586, 33).addBox(-16.0F, -14.7F, 39.9F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(328, 585).addBox(-16.0F, -14.7F, 38.9F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 450).addBox(-16.0F, -14.7F, 37.9F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(152, 584).addBox(-16.0F, -14.7F, 36.9F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 422).addBox(-16.0F, -14.7F, 35.9F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(532, 581).addBox(-16.0F, -14.7F, 34.9F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 420).addBox(-16.0F, -14.7F, 33.9F, 1.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(218, 473).addBox(-16.0F, -22.7F, 7.9F, 1.0F, 15.0F, 26.0F, new CubeDeformation(0.0F))
		.texOffs(194, 569).addBox(-16.0F, -36.7F, 7.9F, 1.0F, 14.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(478, 166).addBox(-15.0F, -36.7F, 7.9F, 30.0F, 29.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(306, 433).addBox(-16.0F, -38.1407F, -26.943F, 1.0F, 5.0F, 35.0F, new CubeDeformation(0.0F))
		.texOffs(420, 362).addBox(-16.0F, -8.7F, -30.1F, 1.0F, 1.0F, 38.0F, new CubeDeformation(0.0F))
		.texOffs(582, 418).addBox(-16.0F, -19.4F, -42.5F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(394, 576).addBox(-16.0F, -22.4F, -42.5F, 1.0F, 3.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(584, 134).addBox(-16.0F, -34.1407F, -28.943F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(586, 31).addBox(-16.0F, -35.1407F, -27.943F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(408, 560).addBox(4.0F, -37.0F, -42.0F, 7.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(180, 518).addBox(4.0F, -37.0F, -41.0F, 7.0F, 1.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(24, 555).addBox(11.0F, -37.0F, -37.0F, 4.0F, 1.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(48, 555).addBox(0.0F, -37.0F, -37.0F, 4.0F, 1.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(242, 545).addBox(0.0F, -37.0F, -38.0F, 4.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 246).addBox(1.0F, -37.0F, -39.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 512).addBox(2.0F, -37.0F, -40.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(92, 586).addBox(3.0F, -37.0F, -41.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 512).addBox(11.0F, -37.0F, -38.0F, 4.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 275).addBox(11.0F, -37.0F, -39.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 526).addBox(11.0F, -37.0F, -40.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 100).addBox(11.0F, -37.0F, -41.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 24.0F, 0.0F));

		PartDefinition cube_r23 = body.addOrReplaceChild("cube_r23", CubeListBuilder.create().texOffs(468, 561).addBox(-4.0F, -37.0F, -1.0F, 7.0F, 13.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(13.1213F, 0.0F, -38.4645F, 0.0F, -0.7854F, 0.0F));

		PartDefinition cube_r24 = body.addOrReplaceChild("cube_r24", CubeListBuilder.create().texOffs(0, 561).addBox(-3.0F, -37.0F, -1.0F, 7.0F, 13.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(1.8787F, 0.0F, -38.4645F, 0.0F, 0.7854F, 0.0F));

		PartDefinition cube_r25 = body.addOrReplaceChild("cube_r25", CubeListBuilder.create().texOffs(556, 56).addBox(4.0F, -37.0F, -52.0F, 8.0F, 13.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-36.0502F, 0.0F, -41.0502F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r26 = body.addOrReplaceChild("cube_r26", CubeListBuilder.create().texOffs(556, 42).addBox(4.0F, -37.0F, -36.0F, 8.0F, 13.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-35.9498F, 0.0F, -41.0502F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r27 = body.addOrReplaceChild("cube_r27", CubeListBuilder.create().texOffs(398, 271).addBox(-19.0F, -11.0F, 0.0F, 32.0F, 11.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(3.0F, -7.4071F, 33.1929F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r28 = body.addOrReplaceChild("cube_r28", CubeListBuilder.create().texOffs(286, 565).addBox(12.0F, -30.2F, 11.0F, 1.0F, 20.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(268, 562).addBox(12.0F, -31.2F, 10.0F, 1.0F, 22.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(282, 565).addBox(43.0F, -30.2F, 11.0F, 1.0F, 20.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(264, 562).addBox(43.0F, -31.2F, 10.0F, 1.0F, 22.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(334, 473).addBox(15.0F, -12.0F, 9.0F, 11.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(250, 553).addBox(15.0F, -32.0F, 9.0F, 11.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(228, 324).addBox(26.0F, -32.0F, 9.0F, 18.0F, 23.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(370, 530).addBox(12.0F, -32.0F, 9.0F, 3.0F, 23.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-28.0F, -22.8772F, -55.9344F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r29 = body.addOrReplaceChild("cube_r29", CubeListBuilder.create().texOffs(514, 554).addBox(12.0F, -24.0F, 10.0F, 1.0F, 16.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(324, 585).addBox(12.0F, -6.0F, 13.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 149).addBox(12.0F, -7.0F, 12.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(578, 116).addBox(12.0F, -8.0F, 11.0F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(106, 584).addBox(43.0F, -7.0F, 12.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(320, 585).addBox(43.0F, -6.0F, 13.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 100).addBox(43.0F, -8.0F, 11.0F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(218, 366).addBox(43.0F, -24.0F, 10.0F, 1.0F, 16.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(334, 39).addBox(12.0F, -24.0F, 9.0F, 32.0F, 16.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-28.0F, 5.261F, -28.709F, 0.9599F, 0.0F, 0.0F));

		PartDefinition cube_r30 = body.addOrReplaceChild("cube_r30", CubeListBuilder.create().texOffs(584, 387).addBox(12.0F, 7.0043F, -5.4798F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(574, 65).addBox(12.0F, 6.0043F, -6.8798F, 1.0F, 1.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(450, 565).addBox(12.0F, 5.0043F, -8.5798F, 1.0F, 1.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(214, 559).addBox(12.0F, 4.0043F, -10.1798F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(226, 547).addBox(12.0F, 3.0043F, -11.7798F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F))
		.texOffs(536, 110).addBox(12.0F, 2.0043F, -13.2798F, 1.0F, 1.0F, 13.0F, new CubeDeformation(0.0F))
		.texOffs(210, 531).addBox(12.0F, 1.0043F, -14.7298F, 1.0F, 1.0F, 15.0F, new CubeDeformation(0.0F))
		.texOffs(180, 498).addBox(35.0F, 0.0043F, -17.9798F, 1.0F, 2.0F, 18.0F, new CubeDeformation(0.0F))
		.texOffs(180, 366).addBox(20.0F, 0.0043F, -17.9798F, 1.0F, 2.0F, 18.0F, new CubeDeformation(0.0F))
		.texOffs(498, 406).addBox(12.0F, 0.0043F, -17.9798F, 8.0F, 1.0F, 18.0F, new CubeDeformation(0.0F))
		.texOffs(584, 384).addBox(43.0F, 7.0043F, -5.4798F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(536, 138).addBox(43.0F, 6.0043F, -6.8798F, 1.0F, 1.0F, 4.0F, new CubeDeformation(0.0F))
		.texOffs(434, 565).addBox(43.0F, 5.0043F, -8.5798F, 1.0F, 1.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(194, 559).addBox(43.0F, 4.0043F, -10.1798F, 1.0F, 1.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(202, 547).addBox(43.0F, 3.0043F, -11.7798F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F))
		.texOffs(536, 15).addBox(43.0F, 2.0043F, -13.2798F, 1.0F, 1.0F, 13.0F, new CubeDeformation(0.0F))
		.texOffs(178, 531).addBox(43.0F, 1.0043F, -14.7298F, 1.0F, 1.0F, 15.0F, new CubeDeformation(0.0F))
		.texOffs(498, 387).addBox(36.0F, 0.0043F, -17.9798F, 8.0F, 1.0F, 18.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-28.0F, -23.4782F, 17.6782F, -1.0036F, 0.0F, 0.0F));

		PartDefinition cube_r31 = body.addOrReplaceChild("cube_r31", CubeListBuilder.create().texOffs(430, 30).addBox(0.0F, -0.9957F, -0.9798F, 10.0F, 1.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(298, 387).addBox(0.0F, -0.9957F, 26.0202F, 10.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(152, 467).addBox(-3.0F, -0.9957F, -0.9798F, 3.0F, 1.0F, 30.0F, new CubeDeformation(0.0F))
		.texOffs(452, 440).addBox(10.0F, -0.9957F, -0.9798F, 3.0F, 1.0F, 30.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-5.0F, -37.9361F, 8.3958F, -0.2618F, 0.0F, 0.0F));

		PartDefinition cube_r32 = body.addOrReplaceChild("cube_r32", CubeListBuilder.create().texOffs(504, 576).addBox(-35.0F, -9.0F, -1.0F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(442, 576).addBox(-50.0F, -9.0F, -1.0F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(518, 155).addBox(-50.0F, -9.0F, 0.0F, 16.0F, 10.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(42.0F, -23.0926F, 40.3188F, 0.5236F, 0.0F, 0.0F));

		PartDefinition dop_el = partdefinition.addOrReplaceChild("dop_el", CubeListBuilder.create().texOffs(536, 293).addBox(-10.5F, -29.7F, -39.2F, 6.0F, 1.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(492, 551).addBox(-9.5F, -31.7F, -36.2F, 4.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(548, 451).addBox(-10.5F, -32.7F, -39.2F, 6.0F, 1.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(426, 513).addBox(-10.5F, -31.7F, -39.2F, 1.0F, 2.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(386, 513).addBox(7.9934F, -28.4F, 23.5071F, 6.0F, 5.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(552, 425).addBox(-9.0066F, -26.4F, 20.5071F, 1.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(584, 227).addBox(-9.0066F, -30.4F, 29.5071F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(234, 584).addBox(-9.0066F, -30.4F, 20.5071F, 1.0F, 4.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(560, 324).addBox(-8.5066F, -30.4F, 21.5071F, 1.0F, 4.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(552, 530).addBox(-9.0066F, -31.4F, 20.5071F, 1.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(582, 534).addBox(11.1934F, -26.9F, 21.5071F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(514, 585).addBox(10.1934F, -26.9F, 22.5071F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 466).addBox(10.1934F, -26.9F, 35.5071F, 2.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(296, 565).addBox(-5.5F, -31.7F, -39.2F, 1.0F, 2.0F, 7.0F, new CubeDeformation(0.0F))
		.texOffs(580, 234).addBox(-13.0F, -19.7071F, -44.4929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(578, 502).addBox(-13.0F, -17.2929F, -44.4929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(584, 216).addBox(-13.0F, -19.0F, -45.2F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 237).addBox(11.0F, -19.0F, -45.2F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 409).addBox(11.0F, -17.2929F, -44.4929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(580, 341).addBox(11.0F, -19.7071F, -44.4929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(584, 254).addBox(11.0F, -19.0F, 42.7F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 108).addBox(11.0F, -17.2929F, 40.9929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 97).addBox(11.0F, -19.7071F, 40.9929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 94).addBox(-13.0F, -19.7071F, 40.9929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(248, 584).addBox(-13.0F, -19.0F, 42.7F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 91).addBox(-13.0F, -17.2929F, 40.9929F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(382, 56).addBox(3.0F, -40.0F, -30.0F, 8.0F, 3.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(584, 538).addBox(9.0F, -40.0F, -31.0F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(540, 584).addBox(4.0F, -40.0F, -31.0F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(576, 132).addBox(5.0F, -38.0F, -31.0F, 4.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(576, 220).addBox(5.0F, -40.0F, -31.0F, 4.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(562, 29).addBox(4.0F, -36.0F, -42.5F, 7.0F, 11.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 104).addBox(4.5F, -35.5F, -43.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 116).addBox(9.5F, -35.5F, -43.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 124).addBox(9.5F, -26.5F, -43.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 118).addBox(4.5F, -26.5F, -43.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(562, 228).addBox(27.8F, -16.0F, -3.0F, 1.0F, 1.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(586, 126).addBox(26.8F, -16.0F, -3.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 128).addBox(26.8F, -16.0F, 4.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(136, 586).addBox(26.8F, -24.0F, 4.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(562, 293).addBox(27.8F, -24.0F, -3.0F, 1.0F, 1.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(586, 132).addBox(26.8F, -24.0F, -3.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(144, 586).addBox(26.8F, -32.0F, 4.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(562, 336).addBox(27.8F, -32.0F, -3.0F, 1.0F, 1.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(140, 586).addBox(26.8F, -32.0F, -3.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 24.0F, 0.0F));

		PartDefinition cube_r33 = dop_el.addOrReplaceChild("cube_r33", CubeListBuilder.create().texOffs(584, 390).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 432).addBox(23.0F, -1.0F, 0.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-12.0F, -16.2929F, 42.9929F, 0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r34 = dop_el.addOrReplaceChild("cube_r34", CubeListBuilder.create().texOffs(584, 406).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 454).addBox(23.0F, -1.0F, 0.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-12.0F, -18.2929F, 42.9929F, 0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r35 = dop_el.addOrReplaceChild("cube_r35", CubeListBuilder.create().texOffs(584, 106).addBox(-1.0F, -1.0F, -1.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(566, 375).addBox(-25.0F, -1.0F, -1.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(12.0F, -16.2929F, -44.4929F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r36 = dop_el.addOrReplaceChild("cube_r36", CubeListBuilder.create().texOffs(584, 232).addBox(-1.0F, -1.0F, -1.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(420, 558).addBox(-25.0F, -1.0F, -1.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(12.0F, -18.2929F, -44.4929F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r37 = dop_el.addOrReplaceChild("cube_r37", CubeListBuilder.create().texOffs(474, 302).addBox(-2.4F, 1.6F, -1.0F, 10.0F, 1.0F, 19.0F, new CubeDeformation(0.0F))
		.texOffs(574, 505).addBox(-2.9F, 0.1F, -4.5F, 2.0F, 2.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(378, 433).addBox(-3.9F, 1.1F, -3.5F, 13.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(574, 451).addBox(6.1F, 0.1F, -4.5F, 2.0F, 2.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(562, 239).addBox(-2.4F, 1.1F, -2.0F, 10.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(562, 237).addBox(-2.4F, 1.1F, 18.0F, 10.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(506, 493).addBox(-3.4F, 1.1F, -2.0F, 1.0F, 1.0F, 21.0F, new CubeDeformation(0.0F))
		.texOffs(506, 471).addBox(7.6F, 1.1F, -2.0F, 1.0F, 1.0F, 21.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-2.6066F, -38.9F, 16.5071F, -0.2618F, 0.0F, 0.0F));

		PartDefinition cube_r38 = dop_el.addOrReplaceChild("cube_r38", CubeListBuilder.create().texOffs(128, 283).addBox(13.8F, -26.3F, 15.6F, 3.0F, 2.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(7.0423F, -0.6F, 15.3651F, 0.0F, -0.5236F, 0.0F));

		PartDefinition cube_r39 = dop_el.addOrReplaceChild("cube_r39", CubeListBuilder.create().texOffs(218, 467).addBox(9.4F, -26.3F, 12.6F, 6.0F, 2.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(6.8055F, -0.6F, 2.3527F, 0.0F, -0.6109F, 0.0F));

		PartDefinition cube_r40 = dop_el.addOrReplaceChild("cube_r40", CubeListBuilder.create().texOffs(52, 543).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-27.0066F, -3.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r41 = dop_el.addOrReplaceChild("cube_r41", CubeListBuilder.create().texOffs(130, 544).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-27.0066F, -4.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r42 = dop_el.addOrReplaceChild("cube_r42", CubeListBuilder.create().texOffs(154, 544).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-27.0066F, -5.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r43 = dop_el.addOrReplaceChild("cube_r43", CubeListBuilder.create().texOffs(544, 252).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-27.0066F, -6.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r44 = dop_el.addOrReplaceChild("cube_r44", CubeListBuilder.create().texOffs(546, 138).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-27.0066F, -7.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r45 = dop_el.addOrReplaceChild("cube_r45", CubeListBuilder.create().texOffs(334, 546).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-27.0066F, -8.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r46 = dop_el.addOrReplaceChild("cube_r46", CubeListBuilder.create().texOffs(178, 547).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-27.0066F, -2.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r47 = dop_el.addOrReplaceChild("cube_r47", CubeListBuilder.create().texOffs(540, 166).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(26.9934F, -8.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r48 = dop_el.addOrReplaceChild("cube_r48", CubeListBuilder.create().texOffs(106, 540).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(26.9934F, -7.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r49 = dop_el.addOrReplaceChild("cube_r49", CubeListBuilder.create().texOffs(28, 543).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(26.9934F, -2.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r50 = dop_el.addOrReplaceChild("cube_r50", CubeListBuilder.create().texOffs(542, 365).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(26.9934F, -3.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r51 = dop_el.addOrReplaceChild("cube_r51", CubeListBuilder.create().texOffs(542, 353).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(26.9934F, -4.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r52 = dop_el.addOrReplaceChild("cube_r52", CubeListBuilder.create().texOffs(540, 178).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(26.9934F, -5.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r53 = dop_el.addOrReplaceChild("cube_r53", CubeListBuilder.create().texOffs(476, 539).addBox(0.0F, -1.0F, -18.4F, 1.0F, 1.0F, 11.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(26.9934F, -6.9F, -1.2429F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r54 = dop_el.addOrReplaceChild("cube_r54", CubeListBuilder.create().texOffs(578, 428).addBox(-4.5F, -13.4F, -0.3F, 2.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(578, 369).addBox(-12.5F, -13.4F, -0.3F, 2.0F, 5.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 53).addBox(-3.0F, -5.0F, 0.2F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(54, 586).addBox(-13.0F, -5.0F, 0.2F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(564, 223).addBox(-11.5F, -18.0F, 0.7F, 8.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(484, 584).addBox(-11.0F, -18.6F, 0.2F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(464, 585).addBox(-9.0F, -18.6F, 0.2F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(480, 584).addBox(-5.0F, -18.6F, 0.2F, 1.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(460, 585).addBox(-7.0F, -18.6F, 0.2F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 51).addBox(-13.0F, -15.9F, 0.2F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 49).addBox(-3.0F, -15.9F, 0.2F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 45).addBox(-4.0F, -13.9F, -0.8F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 47).addBox(-4.0F, -8.9F, -0.8F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 43).addBox(-12.0F, -8.9F, -0.8F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 41).addBox(-12.0F, -13.9F, -0.8F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(556, 468).addBox(-12.5F, -14.4F, -0.3F, 10.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(552, 436).addBox(-12.5F, -8.4F, -0.3F, 10.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, -23.0F, -44.8F, -0.7854F, 0.0F, 0.0F));

		PartDefinition cube_r55 = dop_el.addOrReplaceChild("cube_r55", CubeListBuilder.create().texOffs(406, 433).addBox(-10.5F, -9.4F, 0.5F, 6.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(568, 281).addBox(-10.5F, -16.4F, 0.5F, 6.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(568, 252).addBox(-4.5F, -16.4F, 0.5F, 3.0F, 13.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(568, 164).addBox(-13.5F, -16.4F, 0.5F, 3.0F, 13.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, -23.0F, -44.5F, -0.7854F, 0.0F, 0.0F));

		PartDefinition tower = partdefinition.addOrReplaceChild("tower", CubeListBuilder.create().texOffs(282, 526).addBox(-7.7381F, -11.0F, -17.2215F, 16.0F, 11.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(400, 166).addBox(-10.7381F, -11.0F, 13.7785F, 22.0F, 10.0F, 9.0F, new CubeDeformation(0.0F))
		.texOffs(192, 62).addBox(-10.895F, -12.0F, 13.1578F, 22.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(334, 56).addBox(-10.895F, -1.0F, 13.1578F, 22.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(140, 532).addBox(-7.2736F, -11.0F, 24.314F, 15.0F, 10.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(524, 30).addBox(-8.2736F, -11.0F, 22.314F, 17.0F, 10.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(334, 59).addBox(-10.895F, -1.0F, 13.1578F, 22.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, -16.0F, -9.0F));

		PartDefinition cube_r56 = tower.addOrReplaceChild("cube_r56", CubeListBuilder.create().texOffs(464, 182).addBox(-7.0F, -10.0F, -2.0F, 6.0F, 7.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(580, 8).addBox(-5.0F, -4.0F, -2.5F, 2.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(552, 150).addBox(-8.0F, -12.0F, -1.0F, 8.0F, 12.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-15.531F, 0.0F, 8.7938F, 0.0F, 2.3562F, 0.0F));

		PartDefinition cube_r57 = tower.addOrReplaceChild("cube_r57", CubeListBuilder.create().texOffs(336, 217).addBox(0.0F, -1.0F, 26.5F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(468, 549).addBox(0.0F, -1.0F, 25.5F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(566, 108).addBox(0.0F, -1.0F, 24.5F, 5.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(482, 360).addBox(0.0F, -1.0F, 23.5F, 7.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(564, 135).addBox(0.0F, -1.0F, 22.5F, 9.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(506, 116).addBox(0.0F, -1.0F, 21.5F, 11.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(378, 437).addBox(0.0F, -1.0F, 20.5F, 13.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(306, 217).addBox(0.0F, -1.0F, 19.5F, 14.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-12.7619F, -11.0038F, -2.4119F, 1.5708F, 1.4835F, 1.5708F));

		PartDefinition cube_r58 = tower.addOrReplaceChild("cube_r58", CubeListBuilder.create().texOffs(584, 505).addBox(-2.0F, -1.0F, 26.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(302, 549).addBox(-3.0F, -1.0F, 25.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(552, 164).addBox(-5.0F, -1.0F, 24.0F, 5.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(218, 471).addBox(-7.0F, -1.0F, 23.0F, 7.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(562, 528).addBox(-9.0F, -1.0F, 22.0F, 9.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(482, 116).addBox(-11.0F, -1.0F, 21.0F, 11.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(378, 435).addBox(-13.0F, -1.0F, 20.0F, 13.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(276, 217).addBox(-14.0F, -1.0F, 19.0F, 14.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(498, 425).addBox(-14.0F, -1.0F, 6.0F, 14.0F, 1.0F, 13.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(12.7619F, -11.0038F, -2.4119F, 1.5708F, -1.4835F, -1.5708F));

		PartDefinition cube_r59 = tower.addOrReplaceChild("cube_r59", CubeListBuilder.create().texOffs(574, 510).addBox(8.0F, -12.0F, -17.0F, 5.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(4.7381F, 11.0F, 5.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r60 = tower.addOrReplaceChild("cube_r60", CubeListBuilder.create().texOffs(536, 530).addBox(8.0F, -12.0F, -17.0F, 7.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(5.7381F, 11.0F, 5.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r61 = tower.addOrReplaceChild("cube_r61", CubeListBuilder.create().texOffs(566, 106).addBox(8.0F, -12.0F, -17.0F, 8.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(6.7381F, 11.0F, 5.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r62 = tower.addOrReplaceChild("cube_r62", CubeListBuilder.create().texOffs(562, 526).addBox(8.0F, -12.0F, -17.0F, 10.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(7.7381F, 11.0F, 5.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r63 = tower.addOrReplaceChild("cube_r63", CubeListBuilder.create().texOffs(234, 431).addBox(8.0F, -12.0F, -17.0F, 12.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(8.7381F, 11.0F, 5.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r64 = tower.addOrReplaceChild("cube_r64", CubeListBuilder.create().texOffs(586, 57).addBox(8.0F, -12.0F, -17.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(2.7381F, 11.0F, 5.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r65 = tower.addOrReplaceChild("cube_r65", CubeListBuilder.create().texOffs(580, 130).addBox(8.0F, -12.0F, -17.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(3.7381F, 11.0F, 5.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r66 = tower.addOrReplaceChild("cube_r66", CubeListBuilder.create().texOffs(586, 55).addBox(-9.0F, -12.0F, -17.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-2.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r67 = tower.addOrReplaceChild("cube_r67", CubeListBuilder.create().texOffs(578, 104).addBox(-11.0F, -12.0F, -17.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-3.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r68 = tower.addOrReplaceChild("cube_r68", CubeListBuilder.create().texOffs(574, 456).addBox(-13.0F, -12.0F, -17.0F, 5.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-4.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r69 = tower.addOrReplaceChild("cube_r69", CubeListBuilder.create().texOffs(426, 522).addBox(-15.0F, -12.0F, -17.0F, 7.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-5.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r70 = tower.addOrReplaceChild("cube_r70", CubeListBuilder.create().texOffs(564, 225).addBox(-16.0F, -12.0F, -17.0F, 8.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-6.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r71 = tower.addOrReplaceChild("cube_r71", CubeListBuilder.create().texOffs(562, 351).addBox(-18.0F, -12.0F, -17.0F, 10.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-7.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r72 = tower.addOrReplaceChild("cube_r72", CubeListBuilder.create().texOffs(298, 391).addBox(-20.0F, -12.0F, -17.0F, 12.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-8.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r73 = tower.addOrReplaceChild("cube_r73", CubeListBuilder.create().texOffs(482, 344).addBox(-21.0F, -12.0F, -31.0F, 13.0F, 1.0F, 15.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-23.2381F, 11.0F, 5.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r74 = tower.addOrReplaceChild("cube_r74", CubeListBuilder.create().texOffs(430, 0).addBox(-22.0F, -12.0F, -28.0F, 12.0F, 1.0F, 29.0F, new CubeDeformation(0.0F))
		.texOffs(74, 450).addBox(-21.0F, -23.0F, -28.0F, 10.0F, 1.0F, 29.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-13.2381F, 11.0F, 19.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r75 = tower.addOrReplaceChild("cube_r75", CubeListBuilder.create().texOffs(586, 185).addBox(14.0F, -12.0F, -24.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(184, 586).addBox(14.0F, -23.0F, -24.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(36.7381F, 11.0F, 24.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r76 = tower.addOrReplaceChild("cube_r76", CubeListBuilder.create().texOffs(584, 550).addBox(13.0F, -12.0F, -24.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 548).addBox(13.0F, -23.0F, -24.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(35.7381F, 11.0F, 24.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r77 = tower.addOrReplaceChild("cube_r77", CubeListBuilder.create().texOffs(328, 583).addBox(12.0F, -12.0F, -24.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(320, 583).addBox(12.0F, -23.0F, -24.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(34.7381F, 11.0F, 24.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition cube_r78 = tower.addOrReplaceChild("cube_r78", CubeListBuilder.create().texOffs(586, 187).addBox(-15.0F, -12.0F, -24.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(174, 586).addBox(-15.0F, -23.0F, -24.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-36.2381F, 11.0F, 24.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r79 = tower.addOrReplaceChild("cube_r79", CubeListBuilder.create().texOffs(584, 552).addBox(-15.0F, -12.0F, -24.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 546).addBox(-15.0F, -23.0F, -24.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-35.2381F, 11.0F, 24.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r80 = tower.addOrReplaceChild("cube_r80", CubeListBuilder.create().texOffs(522, 583).addBox(-15.0F, -12.0F, -24.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 464).addBox(-15.0F, -23.0F, -24.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-34.2381F, 11.0F, 24.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r81 = tower.addOrReplaceChild("cube_r81", CubeListBuilder.create().texOffs(130, 498).addBox(-15.0F, -12.0F, -24.0F, 4.0F, 1.0F, 21.0F, new CubeDeformation(0.0F))
		.texOffs(482, 322).addBox(-15.0F, -23.0F, -24.0F, 4.0F, 1.0F, 21.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-13.2381F, 11.0F, 24.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r82 = tower.addOrReplaceChild("cube_r82", CubeListBuilder.create().texOffs(532, 313).addBox(-18.0F, -12.0F, -29.0F, 7.0F, 1.0F, 10.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-32.2381F, -1.0F, 18.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r83 = tower.addOrReplaceChild("cube_r83", CubeListBuilder.create().texOffs(584, 334).addBox(-13.0F, -13.0F, -28.0F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-33.2381F, -0.5F, 12.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r84 = tower.addOrReplaceChild("cube_r84", CubeListBuilder.create().texOffs(584, 337).addBox(-13.0F, -13.0F, -28.0F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-38.2381F, -0.5F, 12.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r85 = tower.addOrReplaceChild("cube_r85", CubeListBuilder.create().texOffs(578, 77).addBox(0.6208F, -0.7334F, 2.1303F, 1.0F, 5.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(578, 70).addBox(-2.3792F, -0.7334F, 2.1303F, 1.0F, 5.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(564, 22).addBox(-2.8792F, -1.7334F, 1.6303F, 5.0F, 1.0F, 5.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(19.7619F, -10.0F, -3.5285F, 1.8326F, -0.7854F, -1.5708F));

		PartDefinition cube_r86 = tower.addOrReplaceChild("cube_r86", CubeListBuilder.create().texOffs(576, 476).addBox(-11.5F, -14.0F, -28.0F, 2.0F, 4.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(496, 576).addBox(-11.5F, -13.0F, -30.6F, 2.0F, 4.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(576, 470).addBox(-14.0F, -13.0F, -30.6F, 2.0F, 4.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(576, 444).addBox(-14.0F, -14.0F, -28.0F, 2.0F, 4.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-12.2381F, -13.0F, 9.4715F, 1.5708F, -0.7854F, -1.5708F));

		PartDefinition cube_r87 = tower.addOrReplaceChild("cube_r87", CubeListBuilder.create().texOffs(218, 569).addBox(-13.0F, -12.0F, -32.0F, 1.0F, 2.0F, 5.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-23.2381F, -13.0F, 9.4715F, 1.5708F, -0.7854F, -1.5708F));

		PartDefinition cube_r88 = tower.addOrReplaceChild("cube_r88", CubeListBuilder.create().texOffs(578, 498).addBox(-13.0F, -12.0F, -31.0F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(522, 585).addBox(-13.0F, -12.0F, -28.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-23.2381F, -1.0F, 4.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r89 = tower.addOrReplaceChild("cube_r89", CubeListBuilder.create().texOffs(518, 585).addBox(-13.0F, -13.0F, -28.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-19.2381F, 0.0F, 4.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r90 = tower.addOrReplaceChild("cube_r90", CubeListBuilder.create().texOffs(290, 584).addBox(-13.0F, -13.0F, -28.0F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-21.2381F, -0.5F, 12.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r91 = tower.addOrReplaceChild("cube_r91", CubeListBuilder.create().texOffs(272, 584).addBox(-13.0F, -13.0F, -28.0F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-16.2381F, -0.5F, 12.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r92 = tower.addOrReplaceChild("cube_r92", CubeListBuilder.create().texOffs(532, 302).addBox(-18.0F, -12.0F, -28.0F, 7.0F, 1.0F, 10.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-14.2381F, -1.0F, 18.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r93 = tower.addOrReplaceChild("cube_r93", CubeListBuilder.create().texOffs(478, 226).addBox(-12.0F, -12.0F, -28.0F, 1.0F, 1.0F, 29.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-13.2381F, 0.0F, 20.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r94 = tower.addOrReplaceChild("cube_r94", CubeListBuilder.create().texOffs(478, 196).addBox(-12.0F, -12.0F, -28.0F, 1.0F, 1.0F, 29.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-13.2381F, 0.0F, 9.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r95 = tower.addOrReplaceChild("cube_r95", CubeListBuilder.create().texOffs(358, 473).addBox(4.0F, -1.0F, -1.0F, 8.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-6.6775F, -11.4981F, 16.4414F, 0.0F, 2.3562F, 0.0F));

		PartDefinition cube_r96 = tower.addOrReplaceChild("cube_r96", CubeListBuilder.create().texOffs(80, 408).addBox(-12.0F, -1.0F, -1.0F, 8.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(7.1775F, -11.4981F, 16.4414F, 0.0F, -2.3562F, 0.0F));

		PartDefinition cube_r97 = tower.addOrReplaceChild("cube_r97", CubeListBuilder.create().texOffs(438, 122).addBox(-12.0F, -1.0F, -1.0F, 11.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(15.3699F, -11.4981F, 9.6632F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r98 = tower.addOrReplaceChild("cube_r98", CubeListBuilder.create().texOffs(272, 504).addBox(-3.0F, -1.0F, -20.0F, 2.0F, 1.0F, 21.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-9.2131F, -11.4981F, 15.32F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r99 = tower.addOrReplaceChild("cube_r99", CubeListBuilder.create().texOffs(438, 119).addBox(-12.0F, -1.0F, -1.0F, 11.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-14.8699F, -11.4981F, 9.6632F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r100 = tower.addOrReplaceChild("cube_r100", CubeListBuilder.create().texOffs(438, 188).addBox(-12.0F, -10.0F, 6.0F, 12.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-3.2173F, -5.8787F, -2.4991F, 0.0F, -1.5708F, -0.7854F));

		PartDefinition cube_r101 = tower.addOrReplaceChild("cube_r101", CubeListBuilder.create().texOffs(404, 119).addBox(-12.0F, -8.0F, 0.0F, 12.0F, 1.0F, 5.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-9.531F, -0.7071F, -2.4991F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r102 = tower.addOrReplaceChild("cube_r102", CubeListBuilder.create().texOffs(582, 348).addBox(-12.0F, -5.0F, 6.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-8.2381F, 6.3137F, -8.8422F, -1.5708F, -0.7854F, 1.5708F));

		PartDefinition cube_r103 = tower.addOrReplaceChild("cube_r103", CubeListBuilder.create().texOffs(586, 102).addBox(-11.0F, -5.0F, 6.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(120, 583).addBox(-12.0F, -8.0F, 6.0F, 2.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(448, 539).addBox(-10.0F, -8.0F, 2.0F, 9.0F, 5.0F, 5.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-8.2381F, 0.0F, -2.4991F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r104 = tower.addOrReplaceChild("cube_r104", CubeListBuilder.create().texOffs(130, 583).addBox(-15.0F, -5.0F, 2.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-7.2381F, -5.0F, 1.5009F, 0.0F, -1.5708F, -0.7854F));

		PartDefinition cube_r105 = tower.addOrReplaceChild("cube_r105", CubeListBuilder.create().texOffs(536, 265).addBox(-12.0F, -12.0F, -1.0F, 12.0F, 12.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-15.2381F, 0.0F, 9.5009F, 0.0F, -1.5708F, 0.0F));

		PartDefinition cube_r106 = tower.addOrReplaceChild("cube_r106", CubeListBuilder.create().texOffs(260, 390).addBox(-17.0F, -1.0F, -1.0F, 17.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(15.9394F, -11.0038F, -1.9236F, 0.1498F, -1.0406F, -0.1732F));

		PartDefinition cube_r107 = tower.addOrReplaceChild("cube_r107", CubeListBuilder.create().texOffs(438, 185).addBox(1.0F, -1.0F, -1.0F, 11.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(518, 459).addBox(-5.0F, 0.0F, -1.0F, 17.0F, 10.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(9.8959F, -10.0F, -12.3914F, 0.0F, -1.0472F, 0.0F));

		PartDefinition cube_r108 = tower.addOrReplaceChild("cube_r108", CubeListBuilder.create().texOffs(400, 188).addBox(-17.0F, -1.5F, -0.6F, 17.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(15.9157F, -11.0038F, -1.9236F, 0.1498F, -1.0406F, -0.1732F));

		PartDefinition cube_r109 = tower.addOrReplaceChild("cube_r109", CubeListBuilder.create().texOffs(400, 185).addBox(0.0F, -1.5F, -0.6F, 17.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(260, 387).addBox(0.0F, -1.0F, -1.0F, 17.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-15.4157F, -11.0038F, -1.9236F, 0.1498F, 1.0406F, 0.1732F));

		PartDefinition cube_r110 = tower.addOrReplaceChild("cube_r110", CubeListBuilder.create().texOffs(234, 428).addBox(-12.0F, -1.0F, -1.0F, 11.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(140, 520).addBox(-12.0F, 0.0F, -1.0F, 17.0F, 10.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-9.3721F, -10.0F, -12.3914F, 0.0F, 1.0472F, 0.0F));

		PartDefinition cube_r111 = tower.addOrReplaceChild("cube_r111", CubeListBuilder.create().texOffs(564, 110).addBox(-5.0F, -10.0F, -1.0F, 5.0F, 10.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-10.031F, -1.0F, 22.0714F, 0.0F, 2.3562F, 0.0F));

		PartDefinition cube_r112 = tower.addOrReplaceChild("cube_r112", CubeListBuilder.create().texOffs(50, 564).addBox(0.0F, -10.0F, -1.0F, 5.0F, 10.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(10.5548F, -1.0F, 22.0714F, 0.0F, -2.3562F, 0.0F));

		PartDefinition cube_r113 = tower.addOrReplaceChild("cube_r113", CubeListBuilder.create().texOffs(106, 552).addBox(0.0F, -12.0F, -1.0F, 8.0F, 12.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(16.0548F, 0.0F, 8.7938F, 0.0F, -2.3562F, 0.0F));

		PartDefinition cube_r114 = tower.addOrReplaceChild("cube_r114", CubeListBuilder.create().texOffs(536, 124).addBox(0.0F, -12.0F, -1.0F, 12.0F, 12.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(15.7619F, 0.0F, 9.5009F, 0.0F, 1.5708F, 0.0F));

		PartDefinition gun = partdefinition.addOrReplaceChild("gun", CubeListBuilder.create().texOffs(480, 155).addBox(-8.0F, -50.0F, -28.0F, 17.0F, 9.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(476, 575).addBox(-7.9F, -49.5F, -28.5F, 2.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(542, 575).addBox(6.9F, -49.5F, -28.5F, 2.0F, 8.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(524, 42).addBox(-1.5F, -48.5F, -39.5F, 4.0F, 6.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(532, 84).addBox(-2.0F, -49.2F, -39.5F, 5.0F, 1.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(532, 97).addBox(-2.0F, -42.8F, -39.5F, 5.0F, 1.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(536, 279).addBox(-3.5F, -46.5F, -39.5F, 2.0F, 2.0F, 12.0F, new CubeDeformation(0.0F))
		.texOffs(538, 215).addBox(2.5F, -46.5F, -39.5F, 2.0F, 2.0F, 11.0F, new CubeDeformation(0.0F))
		.texOffs(584, 257).addBox(1.5F, -46.5F, -28.5F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(536, 143).addBox(2.9F, -46.5F, -28.5F, 4.0F, 2.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 24.0F, 0.0F));

		PartDefinition cube_r115 = gun.addOrReplaceChild("cube_r115", CubeListBuilder.create().texOffs(0, 534).addBox(-1.0F, -3.5F, -12.0F, 2.0F, 3.0F, 12.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(3.8439F, -45.5947F, -27.5F, 0.0F, 0.0F, -0.48F));

		PartDefinition cube_r116 = gun.addOrReplaceChild("cube_r116", CubeListBuilder.create().texOffs(536, 0).addBox(-1.0F, 0.5F, -12.0F, 2.0F, 3.0F, 12.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(3.8439F, -45.4053F, -27.5F, 0.0F, 0.0F, 0.48F));

		PartDefinition cube_r117 = gun.addOrReplaceChild("cube_r117", CubeListBuilder.create().texOffs(524, 532).addBox(-1.0F, 0.5F, -12.0F, 2.0F, 3.0F, 12.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-2.8439F, -45.4053F, -27.5F, 0.0F, 0.0F, -0.48F));

		PartDefinition cube_r118 = gun.addOrReplaceChild("cube_r118", CubeListBuilder.create().texOffs(532, 324).addBox(-1.0F, -3.5F, -12.0F, 2.0F, 3.0F, 12.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-2.8439F, -45.5947F, -27.5F, 0.0F, 0.0F, 0.48F));

		PartDefinition cube_r119 = gun.addOrReplaceChild("cube_r119", CubeListBuilder.create().texOffs(584, 369).addBox(1.0F, -1.0F, -2.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(584, 372).addBox(1.0F, -1.0F, -6.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 573).addBox(0.0F, -2.0F, -6.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 577).addBox(0.0F, -2.0F, -2.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.5F, -41.975F, -79.0F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r120 = gun.addOrReplaceChild("cube_r120", CubeListBuilder.create().texOffs(584, 350).addBox(1.0F, -3.0F, -2.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(358, 584).addBox(1.0F, -3.0F, -6.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 569).addBox(2.0F, -3.0F, -2.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 565).addBox(2.0F, -3.0F, -6.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(572, 399).addBox(-2.0F, -3.0F, -8.0F, 5.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 164).addBox(2.0F, -2.0F, -8.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(434, 573).addBox(-2.0F, 1.0F, -8.0F, 5.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 178).addBox(-2.0F, -2.0F, -8.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(572, 393).addBox(-2.0F, -3.0F, -4.0F, 5.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 137).addBox(2.0F, -2.0F, -4.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(572, 396).addBox(-2.0F, 1.0F, -4.0F, 5.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 142).addBox(-2.0F, -2.0F, -4.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(114, 582).addBox(-2.0F, -2.0F, 0.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 111).addBox(2.0F, -2.0F, 0.0F, 1.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(572, 161).addBox(-2.0F, -3.0F, 0.0F, 5.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(568, 19).addBox(-2.0F, 1.0F, 0.0F, 5.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(48, 508).addBox(-2.0F, -3.0F, 26.0F, 5.0F, 5.0F, 14.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.5F, -44.8F, -79.0F, 0.0F, 0.0F, -0.7854F));

		PartDefinition cube_r121 = gun.addOrReplaceChild("cube_r121", CubeListBuilder.create().texOffs(96, 583).addBox(1.0F, -1.0F, -40.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 581).addBox(-2.0F, -1.0F, -40.0F, 1.0F, 2.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(574, 435).addBox(-2.0F, 1.0F, -40.0F, 4.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(574, 278).addBox(-2.0F, -2.0F, -40.0F, 4.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(480, 119).addBox(-2.0F, -2.0F, -28.0F, 4.0F, 4.0F, 24.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.5F, -45.5F, -49.0F, 0.0F, 0.0F, -0.7854F));

		PartDefinition gun2 = partdefinition.addOrReplaceChild("gun2", CubeListBuilder.create().texOffs(564, 285).addBox(-1.0F, -26.0F, -53.0F, 3.0F, 1.0F, 6.0F, new CubeDeformation(0.0F))
		.texOffs(536, 515).addBox(-1.0F, -24.3F, -57.0F, 3.0F, 5.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(550, 403).addBox(0.7071F, -25.2929F, -57.0F, 2.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(464, 30).addBox(1.7071F, -24.2929F, -55.0F, 1.0F, 1.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(550, 471).addBox(1.7071F, -23.2929F, -57.0F, 1.0F, 3.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(370, 554).addBox(-1.7071F, -21.2929F, -57.0F, 1.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(492, 554).addBox(-1.7071F, -23.2929F, -57.0F, 1.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(580, 0).addBox(-1.7071F, -22.2929F, -50.0F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(580, 4).addBox(-1.7071F, -22.2929F, -57.0F, 1.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
		.texOffs(28, 534).addBox(-1.7071F, -24.2929F, -55.0F, 1.0F, 1.0F, 8.0F, new CubeDeformation(0.0F))
		.texOffs(550, 414).addBox(-1.7071F, -25.2929F, -57.0F, 2.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
		.texOffs(130, 540).addBox(-1.0F, -26.0F, -57.0F, 3.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(582, 63).addBox(-1.0F, -23.8F, -58.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 147).addBox(-1.0F, -21.8F, -58.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 59).addBox(-1.0F, -22.8F, -58.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 61).addBox(1.0F, -22.8F, -58.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 89).addBox(-1.0F, -22.8F, -60.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(88, 586).addBox(1.0F, -22.8F, -60.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 183).addBox(-1.0F, -23.8F, -60.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(582, 169).addBox(-1.0F, -21.8F, -60.0F, 3.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 83).addBox(1.0F, -23.8F, -59.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(84, 586).addBox(-1.0F, -23.8F, -59.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 87).addBox(-1.0F, -21.8F, -59.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(586, 85).addBox(1.0F, -21.8F, -59.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 375).addBox(0.0F, -26.0F, -55.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(58, 586).addBox(0.0F, -25.2F, -58.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
		.texOffs(584, 507).addBox(-2.3F, -22.3F, -51.0F, 2.0F, 1.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offset(7.0F, 16.0F, 7.0F));

		PartDefinition cube_r122 = gun2.addOrReplaceChild("cube_r122", CubeListBuilder.create().texOffs(584, 381).addBox(0.0F, -1.0F, -55.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
		.texOffs(174, 569).addBox(0.0F, -1.0F, -51.0F, 1.0F, 1.0F, 6.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-1.7071F, -25.2929F, -2.0F, 0.0F, 0.0F, 0.7854F));

		PartDefinition cube_r123 = gun2.addOrReplaceChild("cube_r123", CubeListBuilder.create().texOffs(464, 119).addBox(0.0F, -1.0F, -51.0F, 1.0F, 1.0F, 6.0F, new CubeDeformation(0.0F))
		.texOffs(584, 378).addBox(0.0F, -1.0F, -55.0F, 1.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(1.2929F, -25.2929F, -2.0F, 0.0F, 0.0F, 0.7854F));

		return LayerDefinition.create(meshdefinition, 1024, 1024);
	}

	@Override
	public void setupAnim(Entity entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {

	}

	@Override
	public void renderToBuffer(PoseStack poseStack, VertexConsumer vertexConsumer, int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {
		trak.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
		body_trak.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
		body.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
		dop_el.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
		tower.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
		gun.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
		gun2.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
	}
}